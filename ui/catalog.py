from ui.navbar import go_tab
import html
import logging
from typing import Any, Dict, List

import streamlit as st

from data.species import MCE_SPECIES
from services.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


def _live_plants() -> List[Dict[str, Any]]:
    """Read-only fetch of the Supabase plants table for the live-records section."""
    try:
        supabase = get_supabase_client()
        res = supabase.table("plants").select("common_name, scientific_name, family, description, uses, facts").execute()
        return res.data or []
    except Exception as e:
        logger.debug("Live catalog fetch failed: %s", type(e).__name__)
        return []


def _live_locations() -> Dict[str, List[str]]:
    try:
        supabase = get_supabase_client()
        plants = supabase.table("plants").select("id, scientific_name").execute().data or []
        id_to_sci = {p.get("id"): p.get("scientific_name", "") for p in plants}
        locs = supabase.table("campus_locations").select("plant_id, location_name").execute().data or []
        out: Dict[str, List[str]] = {}
        for row in locs:
            sci = id_to_sci.get(row.get("plant_id"), "")
            if row.get("location_name"):
                out.setdefault(sci, []).append(row["location_name"])
        return out
    except Exception as e:
        logger.debug("Live locations fetch failed: %s", type(e).__name__)
        return {}


@st.dialog("Botanical Taxonomy Details", width="large")
def _species_dialog(species: Dict[str, Any]):
    st.image(species["image_url"], use_container_width=True)
    st.markdown(f'### {species["common_name"]}')
    st.markdown(f'*{species["scientific_name"]} ({species["kannada_name"]})*')
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'**Leaf Morphology**\n\n{species["leaf_morphology"]}')
        st.markdown(f'**Campus Zone & Habitat**\n\n{species["campus_zone"]} • {species["habitat"]}')
    with c2:
        st.markdown(f'**Flowering Season**\n\n{species["flowering_season"]}')
        st.markdown(f'**Ecological Role**\n\n{species["ecological_significance"]}')
    st.info(f'Location on campus: {species["location_description"]} (demo coordinates)')
    if st.button("Focus on Map", key=f'dlg_map_{species["id"]}', type="primary"):
        st.session_state["map_focus_species"] = species["species_id"]
        go_tab("Campus Map")


def render_catalog():
    st.markdown(
        '<div style="text-align:center;max-width:640px;margin:0 auto;">'
        '<span class="cl-pill cl-pill-green">MCE HERBARIUM &amp; BIODIVERSITY INDEX</span>'
        '<h2 style="font-weight:800;font-size:1.8rem;">Campus Flora Botanical Catalogue</h2>'
        '<p style="font-size:.85rem;color:rgba(27,67,50,.7);">Search and explore the 4 trained '
        "campus tree species (Pongam, Malabar Plum, Jackfruit, False Ashoka).</p></div>",
        unsafe_allow_html=True,
    )

    families = sorted({sp["family"] for sp in MCE_SPECIES})
    s_col, f_col = st.columns([2, 1])
    with s_col:
        query = st.text_input("Search", placeholder="Search by name, family, Kannada...",
                              label_visibility="collapsed", key="cat_search")
    with f_col:
        family = st.selectbox("Family", options=["All Botanical Families"] + families,
                              label_visibility="collapsed", key="cat_family")

    q = (query or "").lower().strip()
    filtered = []
    for sp in MCE_SPECIES:
        if family != "All Botanical Families" and sp["family"] != family:
            continue
        hay = " ".join([sp["common_name"], sp["scientific_name"], sp["family"],
                        sp["kannada_name"], sp["description"], sp["campus_zone"]]).lower()
        if q and q not in hay:
            continue
        filtered.append(sp)

    st.markdown(
        f'<p style="font-size:12px;color:rgba(27,67,50,.6);">Showing '
        f'<strong>{len(filtered)}</strong> of {len(MCE_SPECIES)} species</p>',
        unsafe_allow_html=True,
    )

    cards = st.columns(3)
    for i, sp in enumerate(filtered):
        with cards[i % 3]:
            st.image(sp["image_url"], use_container_width=True)
            st.markdown(
                f'<span class="cl-pill cl-pill-green">Class #{sp["species_id"]}</span> '
                f'<span class="cl-pill cl-pill-mint">{html.escape(sp["family"])}</span>'
                f'<h4 style="font-weight:800;margin:.4rem 0 0;">{html.escape(sp["common_name"])}</h4>'
                f'<p style="font-size:12px;font-style:italic;color:#40916C;">'
                f'{html.escape(sp["scientific_name"])}</p>'
                f'<p style="font-size:12px;color:rgba(27,67,50,.75);">'
                f'{html.escape(sp["description"][:160])}...</p>'
                f'<p style="font-size:11px;color:rgba(27,67,50,.8);"><strong>Location:</strong> '
                f'{html.escape(sp["location_description"])} <em>(demo)</em></p>',
                unsafe_allow_html=True,
            )
            b1, b2 = st.columns(2)
            with b1:
                if st.button("View on Map", key=f'cat_map_{sp["id"]}', type="secondary", use_container_width=True):
                    st.session_state["map_focus_species"] = sp["species_id"]
                    go_tab("Campus Map")
            with b2:
                if st.button("Taxonomy", key=f'cat_tax_{sp["id"]}', type="secondary", use_container_width=True):
                    _species_dialog(sp)

    st.markdown("---")
    st.markdown(
        '<h3 style="font-weight:800;">Live Campus Database (Supabase)</h3>'
        '<p style="font-size:.85rem;color:rgba(27,67,50,.7);">Records currently catalogued '
        "in the campus database.</p>",
        unsafe_allow_html=True,
    )
    live = _live_plants()
    loc_map = _live_locations()
    if not live:
        st.warning("Could not load live records. Check Supabase connectivity.")
    else:
        for plant in live:
            locs = loc_map.get(plant.get("scientific_name", ""), [])
            loc_txt = ", ".join(locs) if locs else "No mapped locations yet"
            with st.expander(f'{plant.get("common_name", "?")} — *{plant.get("scientific_name", "?")}*'):
                st.markdown(f'**Family:** {plant.get("family", "")}')
                st.markdown(plant.get("description", "") or "")
                uses = plant.get("uses") or []
                if uses:
                    st.markdown("**Uses:** " + ", ".join(str(u) for u in uses))
                st.markdown(f'**Campus locations:** {loc_txt}')
