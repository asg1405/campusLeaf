import streamlit as st


def render_about():
    st.markdown(
        '<div class="cl-hero"><span class="cl-pill" style="background:#2D6A4F;color:#D8F3DC;'
        'border:1px solid #40916C;font-size:11px;">ACADEMIC FINAL YEAR MAJOR PROJECT</span>'
        '<h1 style="font-size:1.9rem;margin:1rem 0 .5rem;">CampusLeaf</h1>'
        '<p style="color:rgba(216,243,220,.9);font-size:.9rem;">Malnad College of Engineering, Hassan</p>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h3 style="font-weight:800;font-size:1.4rem;margin-top:2rem;">Authors</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="cl-card"><strong>Project Guide:</strong> Dr. Hemanth T S<br>'
        '<strong>Student Researchers:</strong> Samarth H Bharadwaj, Avinash Subhas Gundanavar, '
        'Abdur Rahman, Sushanth Gowda S, Poornachandra P B</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h3 style="font-weight:800;font-size:1.4rem;margin-top:1.5rem;">Project Overview</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="cl-card" style="background:#E9F0E8;">'
        'CampusLeaf is an AI-powered flora identification and biodiversity mapping system '
        'for Malnad College of Engineering campus.</div>',
        unsafe_allow_html=True,
    )