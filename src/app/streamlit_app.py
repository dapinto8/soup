import streamlit as st
from pathlib import Path
from .components import sidebar
from config import DEFAULT_MODEL

APP_DIR = Path(__file__).parent

def init_session_state() -> None:
    """Initialize the session state."""

    # Model selection
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = DEFAULT_MODEL

    
    if "selected_collection" not in st.session_state:
        st.session_state.selected_collection = None
    if "show_create_collection_modal" not in st.session_state:
        st.session_state.show_create_collection_modal = False


def app() -> None:
    """Main application entry point."""

    # Initialize state
    init_session_state()

    # Define pages
    pages = [
        st.Page(str(APP_DIR / "pages/1_home.py"), title="Home", icon="🏠"),
        st.Page(str(APP_DIR / "pages/2_Chat.py"), title="Chat", icon="💬"),
        st.Page(str(APP_DIR / "pages/3_Upload.py"), title="Upload", icon="📄"),
    ]

    # Sidebar
    sidebar("🍜 Soup RAG", pages)

    nav = st.navigation(pages, position="hidden")
    nav.run()