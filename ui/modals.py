import logging
from pathlib import Path

import streamlit as st

from data.species import CAMPUS_ZONES
from services.plant_identifier import IMAGE_SIZE, MIN_CONFIDENCE, MODEL_PATH, PLANT_CLASSES
from services.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


def _model_file_size() -> str:
    try:
        size_mb = MODEL_PATH.stat().st_size / (1024 * 1024)
        return f"{size_mb:.1f} MB"
    except OSError:
        return "—"


@st.dialog("Machine Learning Model Engine Status", width="large")
def render_model_dialog():
    connected = MODEL_PATH.is_file()
    if connected:
        st.markdown(
            '<div class="cl-banner-ok"><strong>TRAINED MOBILENETV2 CHECKPOINT CONNECTED</strong><br>'
            f'<span style="font-size:12px;">Live neural forward passes are running on '
            f"{MODEL_PATH.name}.</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="cl-banner-demo"><strong>DEMO MODE ACTIVE — CHECKPOINT PENDING</strong><br>'
            '<span style="font-size:12px;">The trained checkpoint file was not found in '
            "the models directory.</span></div>",
            unsafe_allow_html=True,
        )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'**Architecture**\n\nMobileNetV2')
        st.markdown(f'**Model File**\n\n{MODEL_PATH.name} ({_model_file_size()})')
    with c2:
        st.markdown(f'**Input Tensor**\n\n{IMAGE_SIZE[0]} × {IMAGE_SIZE[1]} × 3')
        st.markdown(f'**Output Classes**\n\n{len(PLANT_CLASSES)} campus species')
    with c3:
        st.markdown(f'**Target Cutoff (τ)**\n\n≥ {MIN_CONFIDENCE:.2f}')
        st.markdown('**Classes**\n\n' + ", ".join(sorted(PLANT_CLASSES)))
    if st.button("Close", key="model_dlg_close", type="primary"):
        st.session_state["show_model_dialog"] = False
        st.rerun()


@st.dialog("Record Field GPS Point", width="large")
def render_field_dialog():
    st.markdown(
        '<p style="font-size:.85rem;color:rgba(27,67,50,.7);">MCE Botanical Field Survey Tool — '
        "log a ground-truth GPS point for a catalogued campus plant.</p>",
        unsafe_allow_html=True,
    )
    try:
        supabase = get_supabase_client()
        plants = supabase.table("plants").select("id, common_name, scientific_name").execute().data or []
    except Exception as e:
        logger.debug("Field dialog plant fetch failed: %s", type(e).__name__)
        plants = []
    if not plants:
        st.warning("Could not load catalogued plants. Check Supabase connectivity.")
        if st.button("Close", key="field_dlg_close_empty", type="secondary"):
            st.session_state["show_field_dialog"] = False
            st.rerun()
        return

    labels = [f'{p.get("common_name", "?")} ({p.get("scientific_name", "?")})' for p in plants]
    choice = st.selectbox("Botanical Species", options=labels, key="field_species")
    zone = st.selectbox("Campus Zone", options=CAMPUS_ZONES, key="field_zone")
    lat = st.number_input("Latitude (°N)", value=12.9815, format="%.6f", key="field_lat")
    lng = st.number_input("Longitude (°E)", value=76.0965, format="%.6f", key="field_lng")
    desc = st.text_input("Field Location Landmark Notes",
                         placeholder="e.g. Next to CSBS entrance steps, east corner", key="field_desc")

    b1, b2 = st.columns([3, 1])
    with b1:
        if st.button("Register Campus Plant Pin", key="field_submit", type="primary", use_container_width=True):
            plant_id = plants[labels.index(choice)].get("id")
            try:
                supabase = get_supabase_client()
                supabase.table("campus_locations").insert({
                    "plant_id": plant_id,
                    "location_name": desc.strip() or f"Near {zone}",
                    "latitude": float(lat),
                    "longitude": float(lng),
                    "description": desc.strip() or f"Field record • {zone}",
                }).execute()
                st.success("Field GPS point recorded successfully in the database!")
            except Exception as e:
                logger.warning("Field GPS insert failed: %s", type(e).__name__)
                st.error(
                    "Could not save this pin with the current database credentials "
                    "(writes are restricted). No record was created or modified."
                )
    with b2:
        if st.button("Cancel", key="field_cancel", type="secondary", use_container_width=True):
            st.session_state["show_field_dialog"] = False
            st.rerun()
