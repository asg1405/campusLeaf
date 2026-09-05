import streamlit as st

def render_found_screen():
    plant_data = st.session_state.get('ml_result', {})
    campus_data = st.session_state.get('campus_result', {})
    
    st.markdown(f"""
        <div class="specimen-card">
            <h1 class="specimen-title">{campus_data.get('common_name', 'Unknown')}</h1>
            <div>
                <span class="specimen-sci-name">{campus_data.get('scientific_name', 'Unknown')}</span>
                <span class="specimen-confidence">{int(plant_data.get('confidence', 0) * 100)}% confidence</span>
            </div>
            
            <div class="specimen-section-title">Description</div>
            <div class="specimen-text">{campus_data.get('description', '')}</div>
            
            <div class="specimen-section-title">Uses</div>
            <ul class="specimen-list">
                {"".join(f"<li>{use}</li>" for use in campus_data.get('uses', []))}
            </ul>
            
            <div class="specimen-section-title">Facts</div>
            <div class="specimen-grid">
                {"".join(f'<div class="specimen-grid-label">{fact.split(":")[0] if ":" in fact else "Fact"}</div><div class="specimen-grid-value">{fact.split(":")[1].strip() if ":" in fact else fact}</div>' for fact in campus_data.get('facts', []))}
            </div>
            
            <div class="specimen-section-title">Found on Campus</div>
            <ul class="specimen-list">
                {"".join(f"<li>📍 {loc}</li>" for loc in campus_data.get('locations', []))}
            </ul>
            
            <div class="stamp-confirmed">
                CAMPUS SPECIMEN<br>
                · CONFIRMED ·
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("TRY ANOTHER PHOTO", use_container_width=True):
        st.session_state['app_state'] = 'IDLE'
        st.session_state['uploaded_image'] = None
        st.rerun()

def render_not_catalogued_screen():
    plant_data = st.session_state.get('ml_result', {})
    
    st.markdown(f"""
        <div class="specimen-card">
            <h1 class="specimen-title">{plant_data.get('common_name', 'Unknown')}</h1>
            <div>
                <span class="specimen-sci-name">{plant_data.get('scientific_name', 'Unknown')}</span>
                <span class="specimen-confidence">{int(plant_data.get('confidence', 0) * 100)}% confidence</span>
            </div>
            
            <div class="clay-alert" style="margin-top: 2rem;">
                <strong>NOT IN CAMPUS DATABASE</strong><br>
                This plant was identified, but it is not currently in the campus database.
            </div>
            
            <div class="stamp-confirmed stamp-clay">
                NOT<br>
                CATALOGUED
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("TRY ANOTHER PHOTO", use_container_width=True):
        st.session_state['app_state'] = 'IDLE'
        st.session_state['uploaded_image'] = None
        st.rerun()

def render_error_screen(custom_message=None):
    error_text = custom_message or "Couldn't reach the identification service.<br>Check your connection and try again."
    st.markdown(f"""
        <div class="specimen-card" style="text-align: center; padding: 3rem 2rem;">
            <div style="color: var(--clay); font-size: 3rem; margin-bottom: 1rem;">⚠</div>
            <div class="specimen-section-title" style="color: var(--clay); font-size: 1.2rem; margin-top: 0;">SERVICE NOTICE</div>
            <p class="specimen-text" style="margin-bottom: 2rem;">{error_text}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("RETRY", use_container_width=True):
            st.session_state['app_state'] = 'IDENTIFYING'
            st.rerun()
    with col2:
        if st.button("TRY ANOTHER PHOTO", use_container_width=True):
            st.session_state['app_state'] = 'IDLE'
            st.session_state['uploaded_image'] = None
            st.session_state['error_message'] = None
            st.rerun()

