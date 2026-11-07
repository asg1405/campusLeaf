import hashlib
import html
import io
import logging
import time
from typing import Any, Dict, List, Optional

import requests
import streamlit as st
from PIL import Image, UnidentifiedImageError
from streamlit.components.v1 import html as components_html

from data.species import MCE_SPECIES, MCE_CAMPUS_CENTER, SAMPLE_LEAVES
from services.plant_identifier import MODEL_PATH, identify_plant
from services.campus_repository import (
    campus_lookup,
    CampusConfigurationError,
    CampusDatabaseError,
)
from services.supabase_client import get_supabase_client
from ui.navbar import is_model_connected, go_tab

logger = logging.getLogger(__name__)

MAX_BYTES = 5 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
LEAFLET_CSS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
LEAFLET_JS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"


def _defaults():
    st.session_state.setdefault("id_mode", "upload")
    st.session_state.setdefault("id_image", None)
    st.session_state.setdefault("id_result", None)
    st.session_state.setdefault("id_campus", None)
    st.session_state.setdefault("id_error", None)
    st.session_state.setdefault("id_source", None)
    st.session_state.setdefault("id_file_id", None)
    st.session_state.setdefault("id_latency", 0.0)


def _reset_identify():
    for key in ("id_image", "id_result", "id_campus", "id_error", "id_source", "id_latency"):
        st.session_state[key] = None


def _match_species(scientific_name: str) -> Optional[Dict[str, Any]]:
    target = (scientific_name or "").strip().lower()
    for sp in MCE_SPECIES:
        if sp["scientific_name"].strip().lower() == target:
            return sp
    return None


def _plant_coords(plant_id: str) -> List[Dict[str, Any]]:
    try:
        supabase = get_supabase_client()
        res = (
            supabase.table("campus_locations")
            .select("location_name, latitude, longitude, description")
            .eq("plant_id", plant_id)
            .execute()
        )
        pins = []
        for row in res.data or []:
            try:
                lat = float(row.get("latitude")) if row.get("latitude") is not None else None
                lng = float(row.get("longitude")) if row.get("longitude") is not None else None
            except (TypeError, ValueError):
                lat, lng = None, None
            if lat is not None and lng is not None:
                pins.append({
                    "name": row.get("location_name", ""),
                    "lat": lat,
                    "lng": lng,
                    "desc": row.get("description") or "",
                    "demo": False,
                })
        return pins
    except Exception as e:
        logger.debug("Coordinate lookup failed: %s", type(e).__name__)
        return []


def _mini_map_html(pins: List[Dict[str, Any]], lat: float, lng: float) -> str:
    """Build a self-contained Leaflet mini-map HTML snippet for the given pins."""
    markers = []
    for p in pins:
        name = html.escape(str(p.get("name", "")))
        desc = html.escape(str(p.get("desc") or ""))
        lat_p = float(p["lat"])
        lng_p = float(p["lng"])
        markers.append(
            f'    L.marker([{lat_p}, {lng_p}], {{title: "{name}"}})'
            f'.addTo(map).bindPopup("<b>{name}</b><br>{desc}");'
        )
    markers_js = "\n".join(markers)
    return f"""<!doctype html>
<html>
<head>
  <link rel="stylesheet" href="{LEAFLET_CSS}"/>
  <style>
    html, body, #map {{ height: 100%; margin: 0; background: #F9FAF7; font-family: inherit; }}
  </style>
</head>
<body>
  <div id="map"></div>
  <script src="{LEAFLET_JS}"></script>
  <script>
    const map = L.map('map', {{zoomControl: true}}).setView([{float(lat)}, {float(lng)}], 17);
    L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }}).addTo(map);
{markers_js}
  </script>
</body>
</html>"""


def _run_inference(pil_image: Image.Image, source: str):
    _reset_identify()
    st.session_state["id_image"] = pil_image
    st.session_state["id_source"] = source
    started = time.perf_counter()
    try:
        with st.spinner("Executing MobileNetV2 forward pass..."):
            prediction = identify_plant(pil_image)
        elapsed = time.perf_counter() - started
        st.session_state["id_latency"] = elapsed
        if prediction is None:
            st.session_state["id_error"] = (
                "The model could not identify this image with enough confidence. "
                "Please upload a clearer leaf photograph."
            )
            return
        st.session_state["id_result"] = prediction
        try:
            st.session_state["id_campus"] = campus_lookup(prediction["scientific_name"])
        except CampusConfigurationError:
            st.session_state["id_error"] = (
                "Database configuration required. Please ensure SUPABASE_URL and SUPABASE_KEY "
                "are configured in your environment or .env file."
            )
        except CampusDatabaseError:
            st.session_state["id_error"] = (
                "Unable to connect to the campus botanical database. Please check your network "
                "or try again in a moment."
            )
    except Exception as e:
        logger.error("Unexpected error during identification: %s", type(e).__name__)
        st.session_state["id_error"] = "An unexpected error occurred during processing."


def _content_key(raw: bytes) -> str:
    return hashlib.md5(raw).hexdigest()


def _process_new_input(raw: bytes, source: str):
    key = _content_key(raw)
    if key == st.session_state.get("id_file_id"):
        return
    _validate_and_store(raw, source)
    st.session_state["id_file_id"] = key
    st.rerun()


def _validate_and_store(raw: bytes, source: str) -> bool:
    if len(raw) > MAX_BYTES:
        st.session_state["id_error"] = "Image size exceeds 5 MB payload limit. Please select a smaller image."
        return False
    try:
        pil_image = Image.open(io.BytesIO(raw))
        pil_image.load()
    except (UnidentifiedImageError, OSError, ValueError):
        st.session_state["id_error"] = "Unsupported image format. CampusLeaf accepts only JPEG, PNG, or WebP."
        return False
    _run_inference(pil_image, source)
    return True


def _consume_pending_sample():
    sample = st.session_state.pop("pending_sample", None)
    if not sample:
        return
    try:
        resp = requests.get(sample["image_url"], timeout=20)
        resp.raise_for_status()
        _validate_and_store(resp.content, "sample")
    except Exception as e:
        logger.warning("Sample fetch failed: %s", type(e).__name__)
        st.session_state["id_error"] = "Could not load the sample image. Please check connectivity and try again."


def render_identify():
    _defaults()
    _consume_pending_sample()

    st.markdown(
        '<div style="text-align:center;max-width:640px;margin:0 auto;">'
        '<span class="cl-pill cl-pill-green">MOBILENETV2 INFERENCE PIPELINE</span>'
        '<h2 style="font-weight:800;font-size:1.8rem;">Plant Species Identification</h2>'
        '<p style="font-size:.85rem;color:rgba(27,67,50,.7);">Upload a leaf image or capture '
        "directly with your camera. The model identifies across 4 trained campus tree species "
    "(Pongam, Malabar Plum, Jackfruit, False Ashoka).</p></div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([5, 7], gap="large")
    with left:
        t1, t2 = st.columns(2)
        with t1:
            if st.button("Upload Image", key="id_tab_upload",
                         type="primary" if st.session_state["id_mode"] == "upload" else "secondary",
                         use_container_width=True):
                st.session_state["id_mode"] = "upload"
                st.rerun()
        with t2:
            if st.button("Use Camera", key="id_tab_camera",
                         type="primary" if st.session_state["id_mode"] == "camera" else "secondary",
                         use_container_width=True):
                st.session_state["id_mode"] = "camera"
                st.rerun()

        if st.session_state.get("id_error"):
            st.markdown(
                f'<div class="cl-banner-err"><strong>Identification Notice</strong><br>'
                f'{html.escape(st.session_state["id_error"])}</div>',
                unsafe_allow_html=True,
            )
            if st.button("Dismiss", key="id_dismiss_err", type="tertiary"):
                st.session_state["id_error"] = None
                st.rerun()

        if st.session_state["id_mode"] == "camera":
            shot = st.camera_input("Capture a leaf photo", label_visibility="collapsed", key="id_camera")
            if shot is not None:
                _process_new_input(shot.getvalue(), "camera")
        else:
            uploaded = st.file_uploader(
                "Select a leaf image", type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed", key="id_uploader",
            )
            if uploaded is not None:
                _process_new_input(uploaded.getvalue(), "upload")

        if st.session_state.get("id_image") is not None:
            st.image(st.session_state["id_image"], caption="Specimen preview", use_container_width=True)
            b1, b2 = st.columns([3, 1])
            with b1:
                if st.button("Identify Plant", key="id_submit", type="primary", use_container_width=True):
                    _run_inference(st.session_state["id_image"], st.session_state.get("id_source") or "upload")
                    st.rerun()
            with b2:
                if st.button("Reset", key="id_reset", type="secondary", use_container_width=True):
                    _reset_identify()
                    st.rerun()

        st.markdown('<div style="font-size:11px;font-weight:800;letter-spacing:1px;margin-top:1rem;">'
                    "TEST THE 4 TRAINED SPECIES</div>", unsafe_allow_html=True)
        for sample in SAMPLE_LEAVES:
            if st.button(
                f'{sample["name"].split(" (")[0]} • {sample["family"]}',
                key=f'id_sample_{sample["id"]}', type="secondary", use_container_width=True,
            ):
                st.session_state["pending_sample"] = sample
                st.rerun()

    with right:
        if st.session_state.get("id_result"):
            _render_result()
        elif st.session_state.get("id_image") is not None:
            st.markdown(
                '<div class="cl-card" style="text-align:center;">'
                '<h3 style="font-weight:800;">Specimen Ready for Analysis</h3>'
                '<p style="font-size:.85rem;color:rgba(27,67,50,.7);">Your leaf image is loaded. '
                "Press Identify Plant to execute the MobileNetV2 forward pass across the 4 trained species.</p></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="cl-card" style="text-align:center;">'
                '<h3 style="font-weight:800;">MobileNetV2 Botanical Classifier</h3>'
                '<p style="font-size:.85rem;color:rgba(27,67,50,.7);">Upload an image on the left, '
                "capture via camera, or pick a trained sample below for instant identification.</p></div>",
                unsafe_allow_html=True,
            )
            steps = [("Step 1", "Input Leaf Photo"), ("Step 2", "Neural Inference"), ("Step 3", "Campus Pin")]
            sc = st.columns(3)
            for col, (k, v) in zip(sc, steps):
                with col:
                    st.markdown(
                        f'<div class="cl-card" style="text-align:center;font-size:12px;">'
                        f'<strong style="color:#40916C;">{k}</strong><br><strong>{v}</strong></div>',
                        unsafe_allow_html=True,
                    )


def _render_result():
    result = st.session_state.get("id_result") or {}
    campus = st.session_state.get("id_campus")
    latency = st.session_state.get("id_latency", 0.0) or 0.0
    conf_pct = round(float(result.get("confidence", 0.0)) * 100, 1)

    if is_model_connected():
        st.markdown(
            '<div class="cl-banner-ok"><strong>AI PREDICTION — MOBILENETV2 ACTIVE</strong><br>'
            f'<span style="font-size:12px;">Evaluated with the local MobileNetV2 model '
            f"in {latency:.2f}s CPU latency.</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="cl-banner-demo"><strong>MODEL FILE NOT FOUND</strong><br>'
            '<span style="font-size:12px;">The trained checkpoint is missing from '
            "the models directory.</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="cl-card"><span class="cl-pill cl-pill-green">Rank 1 Prediction</span> '
        f'<span class="cl-pill cl-pill-green">Family: {html.escape(str(result.get("family", "")))}</span>'
        f'<h3 style="font-weight:800;font-size:1.7rem;margin:.5rem 0 0;">'
        f'{html.escape(str(result.get("common_name", "Unknown")))}</h3>'
        f'<p style="font-style:italic;color:#40916C;">'
        f'{html.escape(str(result.get("scientific_name", "Unknown")))}</p>'
        '<div style="background:#F9FAF7;border:1px solid rgba(27,67,50,.1);border-radius:16px;padding:.8rem;">'
        '<div style="display:flex;justify-content:space-between;align-items:baseline;">'
        '<span style="font-size:10px;font-weight:800;letter-spacing:1px;color:rgba(27,67,50,.6);">'
        "CONFIDENCE SCORE</span>"
        f'<strong style="font-size:1.5rem;">{conf_pct}%</strong></div>'
        f'<div class="cl-confbar"><div style="width:{min(100.0, conf_pct)}%;"></div></div>'
        "</div></div>",
        unsafe_allow_html=True,
    )

    synopsis = (campus or {}).get("description") or result.get("description", "")
    st.markdown(
        '<div class="cl-card"><div style="font-size:11px;font-weight:800;letter-spacing:1px;'
        'color:rgba(27,67,50,.6);">BOTANICAL & ECOLOGICAL SYNOPSIS</div>'
        f'<p style="font-size:.9rem;">{html.escape(str(synopsis))}</p></div>',
        unsafe_allow_html=True,
    )
    uses = (campus or {}).get("uses") or result.get("uses") or []
    facts = (campus or {}).get("facts") or []
    if uses:
        chips = " ".join(
            f'<span class="cl-pill cl-pill-green">{html.escape(str(u))}</span>' for u in uses
        )
        st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)
    for fact in facts:
        st.markdown(
            f'<div class="cl-card" style="padding:.7rem 1rem;font-size:12px;">'
            f"{html.escape(str(fact))}</div>",
            unsafe_allow_html=True,
        )

    if campus:
        names = "<br>".join(html.escape(str(loc)) for loc in campus.get("locations", [])) or "—"
        st.markdown(
            '<div class="cl-card"><div style="font-size:11px;font-weight:800;letter-spacing:1px;'
            'color:rgba(27,67,50,.7);">LOCATION ON CAMPUS</div>'
            f'<div style="font-size:.85rem;">{names}</div></div>',
            unsafe_allow_html=True,
        )
        pins = _plant_coords(str(campus.get("id", "")))
        if pins:
            for pin in pins:
                pin["name"] = pin["name"] or str(campus.get("common_name", ""))
            center = pins[0]
            components_html(_mini_map_html(pins, center["lat"], center["lng"]), height=300)
    else:
        st.markdown(
            '<div class="cl-banner-demo"><strong>NOT IN CAMPUS DATABASE</strong><br>'
            "<span>This plant was identified, but it is not currently recorded "
            "in the campus database.</span></div>",
            unsafe_allow_html=True,
        )
        species = _match_species(str(result.get("scientific_name", "")))
        if species:
            pin = [{
                "name": f'{species["common_name"]} (demo location)',
                "lat": species["latitude"], "lng": species["longitude"],
                "desc": species["location_description"], "demo": True,
            }]
            components_html(_mini_map_html(pin, species["latitude"], species["longitude"]), height=300)
            st.markdown(
                '<span class="cl-pill cl-pill-amber">DEMO COORDS</span>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<p style="font-size:11px;color:rgba(27,67,50,.6);">Top-1 prediction only — '
        "the on-device classifier returns the single best match above the confidence cutoff.</p>",
        unsafe_allow_html=True,
    )
    if st.button("Open Full Campus Map →", key="id_open_map", type="secondary"):
        species = _match_species(str(result.get("scientific_name", "")))
        if species:
            st.session_state["map_focus_species"] = species["species_id"]
        go_tab("Campus Map")
