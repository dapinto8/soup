import streamlit as st
from dependencies import get_collection_service

@st.dialog("Create Collection")
def create_collection_dialog() -> None:
    st.write("Create a new collection")

    collection_service = get_collection_service()

    # Collection name input
    collection_name = st.text_input(
        "Collection Name",
        placeholder="e.g., Meeting Notes Q4 2024",
        help="Give your collection a descriptive name",
    )

    # Validation
    is_valid = bool(collection_name and collection_name.strip())
    name_exists = collection_service.collection_exists(collection_name)

    if name_exists:
        st.error("A collection with this name already exists.")

    # Create collection button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.session_state.show_create_collection_modal = False
            st.rerun()
    with col2:
        if st.button("Create Collection", type="primary", use_container_width=True, disabled=not is_valid or name_exists):
            collection_service.create_collection(collection_name)
            st.session_state.show_create_collection_modal = False
            st.success(f"Collection '{collection_name}' created!")
            st.rerun()

def render_create_collection_dialog() -> None:
    if st.session_state.show_create_collection_modal:
        create_collection_dialog()