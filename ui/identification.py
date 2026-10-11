import streamlit as st
import textwrap
import time
import base64
from io import BytesIO
from PIL import Image

def image_to_base64(image):
    buffered = BytesIO()
    # Convert image to RGB if it's RGBA to save as JPEG
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha = image.convert('RGBA').split()[-1]
        bg = Image.new("RGB", image.size, (255, 255, 255) + (255,))
        bg.paste(image, mask=alpha)
        image = bg
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def render_identifying_screen():
    image = st.session_state.get('uploaded_image')
    
    if image is None:
        st.session_state['app_state'] = 'IDLE'
        st.rerun()

    img_b64 = image_to_base64(image)
    
    # We display the scanning animation using HTML/CSS
    st.markdown(textwrap.dedent(f"""
        <div class="scanner-container">
            <img class="scanner-image" src="data:image/jpeg;base64,{img_b64}" />
            <div class="scanner-line"></div>
        </div>
        <div class="identifying-text">IDENTIFYING PLANT…</div>
        <div style="text-align: center; color: var(--bark); font-family: var(--font-sans); margin-top: 0.5rem;">Analyzing visual features</div>
    """), unsafe_allow_html=True)
    
    # Notice we don't actually call the service directly in the render method if it blocks,
    # but Streamlit reruns from top to bottom. Since we want the animation to render first, 
    # we need a placeholder or just let the app.py call the service immediately.
    # Actually, if we call it in app.py after rendering this component, the UI might freeze 
    # while the sleep happens. Streamlit runs synchronously. 
    # To show the UI before the sleep, we can use `st.spinner` or a trick: 
    # But Streamlit generally updates the browser when the script finishes. 
    # A common workaround is calling `st.empty()` or just accepting Streamlit's loading indicator.
    # We will let `app.py` handle the logic, we just render the UI here.
