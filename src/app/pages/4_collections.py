import streamlit as st
from dependencies import get_collection_service
from app.components import collection_card

collection_service = get_collection_service()

def collections_page() -> None:
    """Collections page."""
    st.title("📚 Collections")
    st.caption("Manage your collections here.")

    collections = collection_service.get_collections()

    if not collections:
        _render_empty_state()
        return
    
    for collection in collections:
        collection_card(
            collection=collection,
            on_rename=lambda old, new: _handle_rename(old, new),
            on_delete=lambda name: _handle_delete(name),
        )


def _render_empty_state() -> None:
    st.info("No collections yet. Create one to get started.")

    if st.button("➕ Create Collection", type="primary"):
        st.session_state.show_create_collection_modal = True
        st.rerun()

def _handle_rename(old_name: str, new_name: str) -> None:
    if not new_name or new_name == old_name:
        return
    
    try:
        # needs implementation at src/services/collection_service.py
        # service.rename_collection(old_name, new_name)
        
        # Update selected collection if it was renamed
        if st.session_state.get("selected_collection") == old_name:
            st.session_state.selected_collection = new_name
        
        st.session_state.editing_collection = None
        st.rerun()
    except ValueError as e:
        st.error(str(e))

def _handle_delete(name: str) -> None:
    try:
        # needs implementation at src/services/collection_service.py
        collection_service.delete_collection(name)
        
        # Clear selection if deleted collection was selected
        if st.session_state.get("selected_collection") == name:
            st.session_state.selected_collection = None

        st.success(f"Collection **{name}** deleted successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to delete: {e}")

collections_page()