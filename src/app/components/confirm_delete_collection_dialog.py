import streamlit as st
from typing import Callable

@st.dialog("Delete Collection")
def confirm_delete_collection_dialog(name: str, on_delete: Callable[[str], None]) -> None:
    """Confirmation dialog for collection deletion."""
    st.warning(f"Are you sure you want to delete **{name}**?")
    st.caption("This will permanently remove all documents in this collection.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("🗑️ Delete", type="primary", use_container_width=True):
            on_delete(name)