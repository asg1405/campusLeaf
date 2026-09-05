import streamlit as st
from PIL import Image

def render_upload_screen():
    st.markdown('<div class="hero-title">Identify.<br>Learn.<br>Preserve.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Take or upload a photo of a plant on campus.</div>', unsafe_allow_html=True)

    # Use tabs for Upload vs Camera
    tab1, tab2 = st.tabs(["Upload Photo", "Take Photo"])
    
    with tab1:
        uploaded_file = st.file_uploader("Select a plant image", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
    with tab2:
        camera_file = st.camera_input("Take a plant photo", label_visibility="collapsed")

    selected_file = uploaded_file or camera_file

    if selected_file is not None:
        try:
            image = Image.open(selected_file)
            st.session_state['uploaded_image'] = image
            st.session_state['app_state'] = 'IMAGE_SELECTED'
            st.rerun()
        except Exception as e:
            st.error("Error opening image. Please try another file.")

def render_image_selected_screen():
    if 'uploaded_image' not in st.session_state:
        st.session_state['app_state'] = 'IDLE'
        st.rerun()
        
    image = st.session_state['uploaded_image']
    
    # Display preview
    st.image(image, use_container_width=True, caption="PHOTO READY")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("IDENTIFY PLANT →", use_container_width=True):
            st.session_state['app_state'] = 'IDENTIFYING'
            st.rerun()
            
    with col2:
        if st.button("REPLACE IMAGE", use_container_width=True):
            st.session_state['uploaded_image'] = None
            st.session_state['app_state'] = 'IDLE'
            st.rerun()
