import streamlit as st
import textwrap

def inject_styles():
    st.markdown(textwrap.dedent("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap');

            :root {
                --ink: #1B4332;
                --mid: #2D6A4F;
                --green: #40916C;
                --light: #74C69D;
                --pale: #D8F3DC;
                --bg: #F9FAF7;
                --muted: #E9F0E8;
                --amber-bg: #FEF3C7;
                --amber-bd: #F59E0B;
                --amber-tx: #92400E;
                --red-bg: #FEF2F2;
                --red-bd: #F87171;
                --red-tx: #991B1B;
                --font: 'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
            }

            .stApp {
                background-color: var(--bg);
                color: var(--ink);
                font-family: var(--font);
            }
            .stMarkdown, .stMarkdown p, .stText, div[data-testid="stMarkdownContainer"] {
                font-family: var(--font);
                color: var(--ink) !important;
            }

            /* Buttons: primary = dark green, secondary = light */
            button[data-testid="stBaseButton-primary"] {
                background-color: var(--ink) !important;
                color: #fff !important;
                border: none !important;
                border-radius: 14px !important;
                font-family: var(--font) !important;
                font-weight: 800 !important;
                box-shadow: 0 6px 14px rgba(27,67,50,.20) !important;
            }
            button[data-testid="stBaseButton-primary"]:hover {
                background-color: var(--mid) !important;
                color: #fff !important;
            }
            button[data-testid="stBaseButton-secondary"] {
                background-color: #fff !important;
                color: var(--ink) !important;
                border: 1px solid rgba(27,67,50,.15) !important;
                border-radius: 14px !important;
                font-family: var(--font) !important;
                font-weight: 700 !important;
            }
            button[data-testid="stBaseButton-secondary"]:hover {
                background-color: var(--muted) !important;
                border-color: var(--green) !important;
                color: var(--ink) !important;
            }
            button[data-testid="stBaseButton-tertiary"] {
                color: var(--mid) !important;
                font-family: var(--font) !important;
                font-weight: 700 !important;
            }

            /* Tab bar buttons */
            div[data-testid="stButtonGroup"] button {
                font-family: var(--font) !important;
                color: var(--ink) !important;
            }

            /* Inputs */
            .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput > div > div > input {
                font-family: var(--font) !important;
                border-radius: 12px !important;
            }
            .stFileUploader > div > div {
                background-color: #fff !important;
                border: 2px dashed rgba(27,67,50,.20) !important;
                border-radius: 16px !important;
            }
            .stCameraInput {
                background-color: #fff;
                border: 2px dashed rgba(27,67,50,.20);
                border-radius: 16px;
                padding: 1rem;
            }

            /* CampusLeaf component classes */
            .cl-brand-badge {
                width: 40px; height: 40px; border-radius: 12px;
                background: var(--ink); color: #fff;
                display: inline-flex; align-items: center; justify-content: center;
                box-shadow: 0 6px 14px rgba(27,67,50,.20);
                font-size: 22px; font-weight: 800;
            }
            .cl-hero {
                background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 55%, #1B4332 100%);
                border-radius: 32px; color: #fff;
                padding: 3rem 2.5rem;
                border: 1px solid rgba(27,67,50,.2);
                box-shadow: 0 20px 45px rgba(27,67,50,.18);
                position: relative; overflow: hidden;
            }
            .cl-hero h1 { color: #fff !important; font-weight: 800; }
            .cl-hero .accent { color: var(--light); font-style: italic; }
            .cl-card {
                background: #fff; border: 1px solid rgba(27,67,50,.10);
                border-radius: 24px; padding: 1.5rem;
                box-shadow: 0 10px 24px rgba(0,0,0,.05);
            }
            .cl-pill {
                display: inline-block; padding: .2rem .7rem; border-radius: 999px;
                font-size: 11px; font-weight: 800;
            }
            .cl-pill-green { background: var(--green); color: #fff; border: 1px solid var(--green); }
            .cl-pill-mint { background: var(--pale); color: var(--ink); border: 1px solid var(--light); }
            .cl-pill-amber { background: var(--amber-bg); color: #fff; border: 1px solid var(--amber-bd); }
            .cl-banner-demo {
                background: var(--amber-bg); border: 1px solid rgba(245,158,11,.4);
                color: var(--amber-tx); border-radius: 16px; padding: 1rem;
            }
            .cl-banner-ok {
                background: var(--pale); border: 1px solid var(--light);
                color: var(--ink); border-radius: 16px; padding: 1rem;
            }
            .cl-banner-err {
                background: var(--red-bg); border: 1px solid rgba(248,113,113,.4);
                color: var(--red-tx); border-radius: 16px; padding: 1rem;
            }
            .cl-confbar { background: var(--muted); border-radius: 999px; height: 8px; overflow: hidden; }
            .cl-confbar > div { background: var(--mid); height: 100%; border-radius: 999px; }
            .cl-footer {
                background: rgba(255,255,255,.7); border-top: 1px solid rgba(27,67,50,.10);
                padding: 1.5rem 0; margin-top: 3rem; font-size: 12px; color: rgba(27,67,50,.60);
            }
            .cl-metric { font-size: 1.7rem; font-weight: 800; color: var(--light); }
            .cl-img { border-radius: 16px; width: 100%; object-fit: cover; }

            /* Hide Streamlit chrome */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """), unsafe_allow_html=True)
