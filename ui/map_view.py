from ui.navbar import go_tab
import html
import json
import logging
from typing import Any, Dict, List

import streamlit as st
import streamlit.components.v1 as components

from data.species import MCE_CAMPUS_CENTER, MCE_SPECIES
from services.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

LEAFLET_CSS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
LEAFLET_JS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"


def _supabase_pins() -> List[Dict[str, Any]]:
    """Read-only pins from Supabase campus_locations that carry coordinates."""
    pins: List[Dict[str, Any]] = []
    try:
        supabase = get_supabase_client()
        plants = supabase.table("plants").select("id, common_name, scientific_name, family").execute().data or []
        by_id = {p.get("id"): p for p in plants}
        locs = supabase.table("campus_locations").select(
            "plant_id, location_name, latitude, longitude, description").execute().data or []
        for row in locs:
            try:
                lat = float(row.get("latitude")) if row.get("latitude") is not None else None
                lng = float(row.get("longitude")) if row.get("longitude") is not None else None
            except (TypeError, ValueError):
                lat, lng = None, None
            if lat is None or lng is None:
                continue
            plant = by_id.get(row.get("plant_id"), {})
            pins.append({
                "common": plant.get("common_name", "Campus plant"),
                "sci": plant.get("scientific_name", ""),
                "family": plant.get("family", ""),
                "zone": "",
                "loc": row.get("location_name", ""),
                "desc": row.get("description") or "",
                "lat": lat, "lng": lng,
                "demo": False, "img": "",
            })
    except Exception as e:
        logger.debug("Supabase pins fetch failed: %s", type(e).__name__)
    return pins


def _demo_pins() -> List[Dict[str, Any]]:
    return [{
        "common": sp["common_name"], "sci": sp["scientific_name"], "family": sp["family"],
        "zone": sp["campus_zone"], "loc": sp["location_description"],
        "desc": sp["habitat"], "lat": sp["latitude"], "lng": sp["longitude"],
        "demo": True, "img": sp["image_url"], "species_id": sp["species_id"],
    } for sp in MCE_SPECIES]


def _safe_js(s: Any) -> str:
    """Makes a string safe to embed in the Leaflet JS literal (no backslashes/quotes/newlines)."""
    return str(s or "").replace("\\", "/").replace("'", "’").replace('"', "”").replace("\n", " ").replace("\r", " ")


def _map_html(pins: List[Dict[str, Any]], focus: Dict[str, Any] | None) -> str:
    safe = [{**p, "common": _safe_js(p.get("common", "")), "sci": _safe_js(p.get("sci", "")),
             "family": _safe_js(p.get("family", "")), "zone": _safe_js(p.get("zone", "")),
             "loc": _safe_js(p.get("loc", "")), "desc": _safe_js(p.get("desc", "")),
             "img": _safe_js(p.get("img", ""))} for p in pins]
    data = json.dumps(safe)
    focus_js = json.dumps(focus) if focus else "null"
    page = '''<link rel="stylesheet" href="__CSS__"/>
<div id="clmap" style="width:100%;height:560px;border-radius:24px;"></div>
<script src="__JS__"></script>
<script>
var map = L.map('clmap', {center: [__LAT__, __LNG__], zoom: 17});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19, attribution: 'OSM contributors | MCE CampusLeaf'}).addTo(map);
function pinIcon(color, size) {
  return L.divIcon({className: 'cl-pin', html: '<div style="background-color:' + color + ';color:white;width:' + size + 'px;height:' + size + 'px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:3px solid white;box-shadow:0 4px 10px rgba(27,67,50,0.35);"><svg width="' + Math.round(size*0.55) + '" height="' + Math.round(size*0.55) + '" viewBox="0 0 24 24" fill="none" stroke="#D8F3DC" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg></div>', iconSize: [size, size], iconAnchor: [size/2, size/2]});
}
var pins = __PINS__;
var focus = __FOCUS__;
pins.forEach(function(p) {
  var color = p.demo ? '#B45309' : '#2D6A4F';
  var m = L.marker([p.lat, p.lng], {icon: pinIcon(color, 34)}).addTo(map);
  var demoTag = p.demo ? '<div style="font-size:10px;font-weight:bold;color:#92400E;background:#FEF3C7;display:inline-block;padding:1px 6px;border-radius:6px;margin-top:4px;">DEMO COORDS</div>' : '';
  var img = p.img ? '<img src="' + p.img + '" style="width:100%;height:90px;object-fit:cover;border-radius:8px;margin-bottom:6px;"/>' : '';
  m.bindPopup('<div style="font-family:sans-serif;min-width:180px;max-width:240px;">' + img + '<div style="font-size:11px;font-weight:bold;color:#15803d;">' + p.family + '</div>' + '<div style="font-size:14px;font-weight:bold;">' + p.common + '</div>' + '<div style="font-size:12px;font-style:italic;color:#57534e;">' + p.sci + '</div>' + '<div style="font-size:11px;margin-top:4px;background:#f5f5f4;padding:4px 6px;border-radius:6px;">' + p.loc + '</div>' + demoTag + '</div>');
  if (focus && p.species_id === focus.species_id) {
    map.setView([p.lat, p.lng], 18); m.openPopup();
  }
});
var locateBtn = L.control({position: 'topleft'});
locateBtn.onAdd = function() {
  var b = L.DomUtil.create('button', '');
  b.innerHTML = 'My Location';
  b.style.cssText = 'background:#fff;border:1px solid rgba(27,67,50,.2);border-radius:8px;padding:6px 10px;font-size:12px;font-weight:bold;color:#1B4332;cursor:pointer;';
  b.onclick = function() {
    if (!navigator.geolocation) { alert('Geolocation is not supported by your browser.'); return; }
    navigator.geolocation.getCurrentPosition(function(pos) {
      var lat = pos.coords.latitude, lng = pos.coords.longitude;
      map.setView([lat, lng], 18);
      L.marker([lat, lng]).addTo(map).bindPopup('Your Current Location').openPopup();
    }, function() {
      alert('Could not retrieve GPS coordinates.');
    }, {enableHighAccuracy: true, timeout: 10000});
  };
  return b;
};
locateBtn.addTo(map);
setTimeout(function(){ map.invalidateSize(); }, 300);
</script>'''
    return (page.replace("__CSS__", LEAFLET_CSS).replace("__JS__", LEAFLET_JS)
                .replace("__LAT__", str(MCE_CAMPUS_CENTER["lat"]))
                .replace("__LNG__", str(MCE_CAMPUS_CENTER["lng"]))
                .replace("__PINS__", data).replace("__FOCUS__", focus_js))


def render_map():
    st.markdown(
        '<div style="text-align:center;max-width:640px;margin:0 auto;">'
        '<span class="cl-pill cl-pill-green">GEOSPATIAL BIODIVERSITY MAPPING</span>'
        '<h2 style="font-weight:800;font-size:1.8rem;">MCE Campus Flora Map</h2>'
        '<p style="font-size:.85rem;color:rgba(27,67,50,.7);">Interactive visualization of '
        "campus tree locations. Amber pins use representative demo coordinates.</p></div>",
        unsafe_allow_html=True,
    )

    pins = _supabase_pins() + _demo_pins()
    families = sorted({p["family"] for p in pins if p.get("family")})
    zones = sorted({p["zone"] for p in pins if p.get("zone")})

    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        query = st.text_input("Search plants", placeholder="Search plant on map...",
                              label_visibility="collapsed", key="map_search")
    with f2:
        family = st.selectbox("Family", ["All Families"] + families,
                              label_visibility="collapsed", key="map_family")
    with f3:
        zone = st.selectbox("Zone", ["All Campus Zones"] + zones,
                            label_visibility="collapsed", key="map_zone")

    q = (query or "").lower().strip()
    filtered = [p for p in pins
                if (family == "All Families" or p.get("family") == family)
                and (zone == "All Campus Zones" or p.get("zone") == zone)
                and (not q or q in f'{p.get("common","")} {p.get("sci","")} {p.get("loc","")}'.lower())]

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Center Campus", key="map_center", type="secondary", use_container_width=True):
            st.session_state["map_focus_species"] = None
            st.rerun()
    with b2:
        if st.button("Record Field GPS", key="map_gps", type="primary", use_container_width=True):
            st.session_state["show_field_dialog"] = True
            st.rerun()
    with b3:
        st.markdown(
            f'<p style="font-size:12px;color:rgba(27,67,50,.6);padding-top:.6rem;">'
            f"{len(filtered)} pins shown</p>",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="cl-banner-demo" style="font-size:12px;"><strong>Demo Coordinates Protocol:</strong> '
        "Amber markers use representative MCE coordinates marked as DEMO DATA. Use “Record Field GPS” "
        "during botanical fieldwork to log ground-truth GPS coordinates.</div>",
        unsafe_allow_html=True,
    )

    focus = None
    focus_id = st.session_state.pop("map_focus_species", None)
    if focus_id is not None:
        focus = {"species_id": focus_id}

    left, right = st.columns([3, 1])
    with left:
        components.html(_map_html(filtered, focus), height=600)
    with right:
        st.markdown(
            '<div style="font-size:11px;font-weight:800;letter-spacing:1px;">PIN DETAILS</div>',
            unsafe_allow_html=True,
        )
        options = [f'{p["common"]} — {p["loc"][:30]}' for p in filtered]
        if not options:
            st.info("No pins match the current filters.")
        else:
            choice = st.selectbox("Pin", options=options, label_visibility="collapsed", key="map_pin_pick")
            pin = filtered[options.index(choice)]
            st.markdown(f'**{html.escape(pin["common"])}**')
            st.markdown(f'*{html.escape(pin["sci"])}*')
            st.markdown(f'Family: {html.escape(pin.get("family",""))}')
            if pin.get("zone"):
                st.markdown(f'Zone: {html.escape(pin["zone"])}')
            st.markdown(f'Location: {html.escape(pin.get("loc",""))}')
            st.markdown(f'GPS: {pin["lat"]:.5f}° N, {pin["lng"]:.5f}° E')
            if pin.get("demo"):
                st.markdown('<span class="cl-pill cl-pill-amber">DEMO COORDS</span>', unsafe_allow_html=True)
            if st.button("View in Catalog", key="map_to_catalog", type="secondary", use_container_width=True):
                go_tab("Flora Catalog")
