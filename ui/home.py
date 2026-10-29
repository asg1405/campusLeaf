from ui.navbar import go_tab
import streamlit as st
from data.species import HERO_IMAGE_URL, HERO_METRICS, SAMPLE_LEAVES, WORKFLOW_STEPS


def render_home():
    st.markdown(
        '<div style="text-align:center;margin:2.2rem 0 1rem;">'
        '<span class="cl-pill cl-pill-green">ENGINEERED FOR MCE ACADEMIC COMMUNITY</span>'
        '<h3 style="font-weight:800;font-size:1.6rem;margin:.5rem 0;">How CampusLeaf Works</h3>'
        '<p style="font-size:.85rem;color:rgba(27,67,50,.7);">A specialized 4-tier architecture '
        "isolating presentation, application routing, deep learning inference, and persistence.</p></div>",
        unsafe_allow_html=True,
    )
    wcols = st.columns(len(WORKFLOW_STEPS))
    for col, step in zip(wcols, WORKFLOW_STEPS):
        with col:
            st.markdown(
                f'<div class="cl-card"><div class="cl-pill cl-pill-green">{step["n"]}</div>'
                f'<h4 style="font-weight:800;margin:.6rem 0 .3rem;">{step["title"]}</h4>'
                f'<p style="font-size:12px;color:rgba(27,67,50,.7);">{step["body"]}</p></div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="cl-card" style="background:#E9F0E8;margin-top:1.5rem;">'
        '<div style="font-size:11px;font-weight:800;letter-spacing:1px;color:#40916C;">'
        "INTERACTIVE DEMO SHOWCASE • 4 TRAINED SPECIES</div>"
        '<h3 style="font-weight:800;font-size:1.4rem;">Try the 4 Trained Species Leaves</h3>'
        '<p style="font-size:.85rem;color:rgba(27,67,50,.7);">Select any trained specimen '
        "to run neural identification with its botanical taxonomy and campus pin.</p></div>",
        unsafe_allow_html=True,
    )
    scols = st.columns(len(SAMPLE_LEAVES))
    for col, sample in zip(scols, SAMPLE_LEAVES):
        with col:
            st.image(sample["image_url"], use_container_width=True)
            st.markdown(
                f'<strong style="font-size:13px;">{sample["name"].split(" (")[0]}</strong><br>'
                f'<em style="font-size:11px;color:#40916C;">{sample["scientific_name"]}</em><br>'
                f'<span class="cl-pill cl-pill-green" style="font-size:10px;">{sample["family"]}</span>',
                unsafe_allow_html=True,
            )
            if st.button("Identify →", key=f'home_sample_{sample["id"]}', type="secondary", use_container_width=True):
                st.session_state["pending_sample"] = sample
                go_tab("Identify")