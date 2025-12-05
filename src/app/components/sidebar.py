import streamlit as st
from .model_selector import model_selector
from .collection_selector import collection_selector
from .create_collection_dialog import render_create_collection_dialog

def sidebar(title: str, pages: list[st.Page]) -> None:
    """Render the sidebar with global components."""
    with st.sidebar:
        st.title(title)

        for page in pages:
            st.sidebar.page_link(page, label=page.title, icon=page.icon)

        st.markdown("---")
        
        # Model selector (LLM + coupled embeddings)
        model_selector()

        # Collection selector
        collection_selector()

        # Create collection dialog
        render_create_collection_dialog()