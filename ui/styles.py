import streamlit as st
import textwrap

def inject_styles():
    st.markdown(textwrap.dedent("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,100..900;1,9..144,100..900&family=IBM+Plex+Mono:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&family=IBM+Plex+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap');

            :root {
                --paper: #F6F2E8;
                --ink: #1F2A1D;
                --moss: #2E4A2A;
                --leaf: #7BAA5D;
                --bark: #6B5D4F;
                --purple: #6D4C9F;
                --clay: #B65D2A;
                --card-white: #FFFDF6;
                
                --font-serif: 'Fraunces', serif;
                --font-sans: 'IBM Plex Sans', sans-serif;
                --font-mono: 'IBM Plex Mono', monospace;
            }

            /* Global Background & Text */
            .stApp {
                background-color: var(--paper);
                color: var(--ink);
                font-family: var(--font-sans);
            }
            
            /* Typography Overrides */
            h1, h2, h3, h4, h5, h6, .hero-title {
                font-family: var(--font-serif) !important;
                color: var(--ink) !important;
            }

            .stMarkdown p {
                font-family: var(--font-sans);
                color: var(--ink);
                font-size: 1.05rem;
                line-height: 1.6;
            }

            .stButton > button {
                background-color: var(--moss) !important;
                color: var(--paper) !important;
                border: none !important;
                border-radius: 4px !important;
                padding: 0.75rem 1.5rem !important;
                font-family: var(--font-sans) !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                transition: background-color 0.2s ease, transform 0.1s ease;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .stButton > button:hover {
                background-color: var(--leaf) !important;
                color: var(--card-white) !important;
            }

            .stButton > button:active {
                transform: translateY(2px);
            }
            
            .stButton > button:focus {
                outline: 2px solid var(--purple) !important;
                outline-offset: 2px !important;
                box-shadow: none !important;
            }

            /* File Uploader Customization */
            .stFileUploader > div > div {
                background-color: var(--card-white) !important;
                border: 2px dashed var(--bark) !important;
                border-radius: 8px !important;
                padding: 2rem !important;
            }
            .stFileUploader > div > div:hover {
                border-color: var(--moss) !important;
            }
            
            .stFileUploader p {
                font-family: var(--font-sans) !important;
                color: var(--bark) !important;
            }
            
            /* Camera input */
            .stCameraInput {
                background-color: var(--card-white);
                border: 2px dashed var(--bark);
                border-radius: 8px;
                padding: 1rem;
            }

            /* Custom Components */
            .hero-title {
                font-size: 4rem;
                line-height: 1.1;
                margin-bottom: 0.5rem;
                margin-top: 1rem;
                font-weight: 700;
            }
            
            .hero-subtitle {
                font-size: 1.25rem;
                color: var(--bark);
                margin-bottom: 2rem;
            }
            
            .top-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid var(--bark);
                padding-bottom: 0.5rem;
                margin-bottom: 1rem;
                font-family: var(--font-mono);
                font-size: 0.85rem;
                text-transform: uppercase;
                color: var(--bark);
            }

            /* Mobile-first responsiveness */
            @media (max-width: 768px) {
                .hero-title {
                    font-size: 3rem;
                }
                .stApp {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
            }
            
            /* Specimen Card */
            .specimen-card {
                background-color: var(--card-white);
                border: 1px solid var(--bark);
                padding: 2rem;
                box-shadow: 2px 4px 12px rgba(0,0,0,0.05);
                position: relative;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
            
            .specimen-title {
                font-family: var(--font-serif);
                font-size: 2.5rem;
                color: var(--ink);
                margin: 0;
            }
            
            .specimen-sci-name {
                font-family: var(--font-mono);
                font-size: 1.1rem;
                font-style: italic;
                color: var(--bark);
                margin-bottom: 1.5rem;
                border-bottom: 1px solid var(--bark);
                padding-bottom: 1rem;
                display: inline-block;
            }
            
            .specimen-confidence {
                font-family: var(--font-mono);
                font-size: 0.85rem;
                color: var(--moss);
                background-color: rgba(123, 170, 93, 0.1);
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                display: inline-block;
                margin-left: 1rem;
                vertical-align: middle;
            }
            
            .specimen-section-title {
                font-family: var(--font-sans);
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: var(--moss);
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }
            
            .specimen-text {
                color: var(--ink);
                line-height: 1.5;
            }
            
            .specimen-list {
                list-style-type: none;
                padding-left: 0;
                margin-top: 0.5rem;
            }
            
            .specimen-list li {
                position: relative;
                padding-left: 1.25rem;
                margin-bottom: 0.25rem;
                color: var(--ink);
            }
            
            .specimen-list li::before {
                content: "•";
                color: var(--leaf);
                position: absolute;
                left: 0;
            }
            
            .specimen-grid {
                display: grid;
                grid-template-columns: 100px 1fr;
                gap: 0.5rem 1rem;
                font-family: var(--font-mono);
                font-size: 0.9rem;
            }
            
            .specimen-grid-label {
                color: var(--bark);
            }
            
            .specimen-grid-value {
                color: var(--ink);
            }

            /* Archival Stamps */
            .stamp-confirmed {
                position: absolute;
                bottom: 2rem;
                right: 2rem;
                border: 2px solid var(--moss);
                color: var(--moss);
                font-family: var(--font-mono);
                font-size: 1rem;
                font-weight: 700;
                text-align: center;
                padding: 0.5rem 1rem;
                transform: rotate(-5deg);
                opacity: 0.8;
                border-radius: 2px;
                background-color: transparent;
                pointer-events: none;
                z-index: 10;
            }
            
            .stamp-clay {
                border-color: var(--clay);
                color: var(--clay);
                transform: rotate(3deg);
            }

            /* Scanning Animation */
            .scanner-container {
                position: relative;
                display: inline-block;
                width: 100%;
                max-width: 500px;
                margin: 0 auto;
                border: 1px solid var(--bark);
                padding: 0.5rem;
                background-color: var(--card-white);
            }
            
            .scanner-image {
                width: 100%;
                display: block;
                opacity: 0.8;
            }
            
            .scanner-line {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 3px;
                background-color: var(--purple);
                box-shadow: 0 0 10px var(--purple);
                animation: scan 2s linear infinite;
                z-index: 5;
            }
            
            @keyframes scan {
                0% { top: 0; }
                50% { top: 100%; }
                100% { top: 0; }
            }
            
            @media (prefers-reduced-motion: reduce) {
                .scanner-line {
                    animation: pulse 2s ease-in-out infinite;
                    top: 50%;
                    height: 100%;
                    background-color: rgba(109, 76, 159, 0.2);
                    box-shadow: none;
                }
                
                @keyframes pulse {
                    0% { opacity: 0.3; }
                    50% { opacity: 0.8; }
                    100% { opacity: 0.3; }
                }
            }
            
            .identifying-text {
                font-family: var(--font-mono);
                color: var(--purple);
                text-align: center;
                margin-top: 1rem;
                font-weight: 600;
                letter-spacing: 1px;
            }
            
            .clay-alert {
                background-color: rgba(182, 93, 42, 0.1);
                border-left: 4px solid var(--clay);
                padding: 1rem;
                margin: 1rem 0;
                font-family: var(--font-sans);
                color: var(--ink);
            }
            
            /* Status Indicators */
            .status-indicator {
                font-family: var(--font-mono);
                font-size: 0.85rem;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                background-color: var(--card-white);
                border: 1px solid var(--bark);
                display: inline-block;
                margin-bottom: 1rem;
            }
            
            .status-ready { color: var(--moss); }
            .status-identifying { color: var(--purple); border-color: var(--purple); }
            .status-found { color: var(--moss); border-color: var(--moss); }
            .status-not-found { color: var(--clay); border-color: var(--clay); }
            
            /* General image styling */
            .uploaded-image-preview {
                border: 4px solid var(--card-white);
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                max-width: 100%;
                display: block;
                margin: 1rem auto;
            }
            
            /* Hide Streamlit components */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """), unsafe_allow_html=True)

def render_top_bar(status="READY"):
    status_class = f"status-{status.lower().replace(' ', '-')}"
    st.markdown(textwrap.dedent(f"""
        <div class="top-bar">
            <div>CAMPUS PLANT ID</div>
            <div class="{status_class}">● {status}</div>
        </div>
    """), unsafe_allow_html=True)
