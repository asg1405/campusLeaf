import os
import logging
from typing import Optional, Tuple
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load .env if present in root or working directory
load_dotenv()

_supabase_client = None
_client_init_error: Optional[str] = None

def get_supabase_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Safely retrieves Supabase URL and Key from Streamlit secrets or environment variables.
    Never logs or exposes credentials.
    """
    url = None
    key = None

    # Check Streamlit secrets if running inside Streamlit
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "SUPABASE_URL" in st.secrets:
                url = st.secrets["SUPABASE_URL"]
            if "SUPABASE_KEY" in st.secrets:
                key = st.secrets["SUPABASE_KEY"]
    except Exception:
        pass

    # Fall back to environment variables (e.g. from .env file or system env)
    if not url:
        url = os.environ.get("SUPABASE_URL")
    if not key:
        key = os.environ.get("SUPABASE_KEY")

    # Clean leading/trailing quotes or whitespaces
    if url:
        url = url.strip().strip("'\"")
    if key:
        key = key.strip().strip("'\"")

    return url, key

def get_supabase_client():
    """
    Returns a configured Supabase client instance or None.
    Caches the instance once initialized.
    Raises RuntimeError if credentials are missing or client creation fails.
    """
    global _supabase_client, _client_init_error

    if _supabase_client is not None:
        return _supabase_client

    url, key = get_supabase_credentials()

    if not url or not key:
        _client_init_error = (
            "Supabase credentials not configured. Please set SUPABASE_URL and SUPABASE_KEY "
            "in your environment, .env file, or .streamlit/secrets.toml."
        )
        raise RuntimeError(_client_init_error)

    try:
        from supabase import create_client, ClientOptions
        _supabase_client = create_client(url, key)
        _client_init_error = None
        return _supabase_client
    except Exception as e:
        logger.error("Failed to initialize Supabase client: %s", type(e).__name__)
        _client_init_error = f"Failed to connect to Supabase: {type(e).__name__}"
        raise RuntimeError(_client_init_error) from e
