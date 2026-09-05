import streamlit as st
import logging
from ui.styles import inject_styles, render_top_bar
from ui.upload import render_upload_screen, render_image_selected_screen
from ui.identification import render_identifying_screen
from ui.specimen_card import render_found_screen, render_not_catalogued_screen, render_error_screen
from services.plant_identifier import identify_plant
from services.campus_repository import campus_lookup, CampusConfigurationError, CampusDatabaseError

logger = logging.getLogger(__name__)

# Must be the first Streamlit command
st.set_page_config(
    page_title="Campus Plant ID",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def init_session_state():
    if 'app_state' not in st.session_state:
        st.session_state['app_state'] = 'IDLE' # IDLE, IMAGE_SELECTED, IDENTIFYING, FOUND, NOT_CATALOGUED, ERROR
    if 'uploaded_image' not in st.session_state:
        st.session_state['uploaded_image'] = None
    if 'ml_result' not in st.session_state:
        st.session_state['ml_result'] = None
    if 'campus_result' not in st.session_state:
        st.session_state['campus_result'] = None
    if 'error_message' not in st.session_state:
        st.session_state['error_message'] = None

def main():
    init_session_state()
    inject_styles()
    
    # Map app_state to a friendly top-bar status
    status_mapping = {
        'IDLE': 'READY',
        'IMAGE_SELECTED': 'READY',
        'IDENTIFYING': 'IDENTIFYING',
        'FOUND': 'FOUND',
        'NOT_CATALOGUED': 'NOT FOUND',
        'ERROR': 'ERROR'
    }
    current_status = status_mapping.get(st.session_state['app_state'], 'READY')
    render_top_bar(status=current_status)

    state = st.session_state['app_state']

    if state == 'IDLE':
        render_upload_screen()
        
    elif state == 'IMAGE_SELECTED':
        render_image_selected_screen()
        
    elif state == 'IDENTIFYING':
        # Render the UI with the scanning animation
        placeholder = st.empty()
        with placeholder.container():
            render_identifying_screen()
        
        # Perform the identification and database query
        try:
            image = st.session_state['uploaded_image']
            plant_prediction = identify_plant(image)
            
            if plant_prediction:
                st.session_state['ml_result'] = plant_prediction
                campus_record = campus_lookup(plant_prediction['scientific_name'])
                
                if campus_record:
                    st.session_state['campus_result'] = campus_record
                    st.session_state['app_state'] = 'FOUND'
                else:
                    st.session_state['app_state'] = 'NOT_CATALOGUED'
            else:
                st.session_state['error_message'] = "Couldn't identify the plant image."
                st.session_state['app_state'] = 'ERROR'

        except CampusConfigurationError as ce:
            logger.warning("Configuration error: %s", ce)
            st.session_state['error_message'] = (
                "Database configuration required. Please ensure SUPABASE_URL and SUPABASE_KEY "
                "are configured in your environment or .env file."
            )
            st.session_state['app_state'] = 'ERROR'
                
        except CampusDatabaseError as de:
            logger.error("Database connection failure: %s", de)
            st.session_state['error_message'] = (
                "Unable to connect to the campus botanical database. Please check your network "
                "or try again in a moment."
            )
            st.session_state['app_state'] = 'ERROR'

        except Exception as e:
            logger.error("Unexpected error during identification: %s", type(e).__name__)
            st.session_state['error_message'] = "An unexpected error occurred during processing."
            st.session_state['app_state'] = 'ERROR'
            
        # Rerun to show the results screen
        st.rerun()
        
    elif state == 'FOUND':
        render_found_screen()
        
    elif state == 'NOT_CATALOGUED':
        render_not_catalogued_screen()
        
    elif state == 'ERROR':
        error_msg = st.session_state.get('error_message')
        render_error_screen(custom_message=error_msg)

if __name__ == "__main__":
    main()
