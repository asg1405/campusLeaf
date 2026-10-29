import streamlit as st
from ui.styles import inject_styles
from ui.navbar import render_navbar, render_footer
from ui.home import render_home
from ui.identify import render_identify
from ui.catalog import render_catalog
from ui.map_view import render_map
from ui.about import render_about
from ui.modals import render_field_dialog, render_model_dialog

st.set_page_config(
    page_title="CampusLeaf — MCE Flora Identification",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def init_state():
    st.session_state.setdefault("tab", "Home")
    st.session_state.setdefault("pending_sample", None)
    st.session_state.setdefault("map_focus_species", None)
    st.session_state.setdefault("show_field_dialog", False)
    st.session_state.setdefault("show_model_dialog", False)


def main():
    init_state()
    inject_styles()
    render_navbar()

    if st.session_state.get("show_model_dialog"):
        render_model_dialog()
    if st.session_state.get("show_field_dialog"):
        render_field_dialog()

    tab = st.session_state.get("tab", "Home")
    if tab == "Home":
        render_home()
    elif tab == "Identify":
        render_identify()
    elif tab == "Flora Catalog":
        render_catalog()
    elif tab == "Campus Map":
        render_map()
    else:
        render_home()

    render_footer()


if __name__ == "__main__":
    main()
