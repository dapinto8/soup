import streamlit as st
from dependencies import get_collection_service

def collection_selector() -> None:
    st.sidebar.markdown("### 📂 Collection")

    collection_service = get_collection_service()
    
    collections = collection_service.get_collections()
    collection_names = [collection.name for collection in collections]

    if not collection_names:
        st.sidebar.info("No collections yet. Create one to get started.")
        _create_collection_button()
        return

    current_selection = st.session_state.selected_collection
    if current_selection not in collection_names:
        current_selection = collection_names[0]
        st.session_state.selected_collection = current_selection
    
    current_index = collection_names.index(current_selection)

    selected_collection = st.sidebar.selectbox(
        "Select a collection",
        options=collection_names,
        index=current_index,
        key="collection_selector_dropdown",
        help="Choose a collection to work with",
    )

    if selected_collection != st.session_state.selected_collection:
        st.session_state.selected_collection = selected_collection
        st.rerun()

    _create_collection_button()

def _create_collection_button() -> None:
    if st.sidebar.button("➕ New Collection", use_container_width=True):
        st.session_state.show_create_collection_modal = True
        st.rerun()

def get_selected_collection() -> str | None:
    return st.session_state.selected_collection