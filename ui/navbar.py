import streamlit as st
from pathlib import Path

TABS = ["Home", "Identify", "Flora Catalog", "Campus Map"]

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "campus_plant_id_mobilenetv2.keras"
)


def is_model_connected() -> bool:
    try:
        return MODEL_PATH.is_file()
    except OSError:
        return False


def go_tab(name: str):
    """Programmatic tab navigation (plain session key, no widget state)."""
    st.session_state["tab"] = name
    st.rerun()


def render_navbar():
    brand_col = st.columns([5], vertical_alignment="center")[0]
    with brand_col:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:12px;">'
            '<div class="cl-brand-badge">'
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D8F3DC" '
            'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>'
            '<path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg></div>'
            '<div><div style="font-weight:800;font-size:20px;letter-spacing:-0.5px;">'
            'CampusLeaf<span style="color:#74C69D;">.</span>'
            ' <span class="cl-pill cl-pill-green" style="font-size:10px;">MCE Hassan</span>'
            "</div>"
            '<div style="font-size:12px;color:rgba(27,67,50,.6);font-weight:500;">'
            "AI Flora Identification &amp; Biodiversity Mapping</div></div></div>",
            unsafe_allow_html=True,
        )
    current = st.session_state.get("tab", "Home")
    if current not in TABS:
        current = "Home"
    tab_cols = st.columns(len(TABS))
    for col, name in zip(tab_cols, TABS):
        with col:
            if name == current:
                st.markdown(
                    f'<div style="background:#1B4332;color:#fff;font-weight:700;'
                    'font-size:13px;text-align:center;border-radius:12px;padding:.55rem 0;">'
                    f"{name}</div>",
                    unsafe_allow_html=True,
                )
            elif st.button(name, key=f"navtab_{name}", type="secondary", use_container_width=True):
                go_tab(name)


def render_footer():
    st.markdown(
        '<div class="cl-footer"><div style="display:flex;justify-content:space-between;'
        "flex-wrap:wrap;gap:8px;max-width:1100px;margin:0 auto;padding:0 1rem;\">"
        "<div><strong>CampusLeaf<span>.</span></strong> • "
        "AI Flora Identification &amp; Biodiversity Mapping System</div>"
        "<div>Department of CSBS • Malnad College of Engineering, Hassan (VTU Autonomous)</div>"
        "</div></div>",
        unsafe_allow_html=True,
    )
