import streamlit as st
from core import Collection
from .confirm_delete_collection_dialog import confirm_delete_collection_dialog
from typing import Callable

def collection_card(collection: Collection, on_rename: Callable[[str, str], None], on_delete: Callable[[str], None]) -> None:
    name = collection.name
    is_editing = st.session_state.get("editing_collection") == name

    with st.container(border=True):
        col_name, col_info, col_actions = st.columns([3, 2, 2])
        
        with col_name:
            if is_editing:
                new_name = st.text_input(
                    "Collection name",
                    value=name,
                    key=f"edit_input_{name}",
                    label_visibility="collapsed",
                )
            else:
                st.markdown(f"### {name}")
        
        # with col_info:
        #     st.caption(f"📄 {doc_count} documents")
        #     st.caption(f"📐 {embedding_model}")
        
        with col_actions:
            if is_editing:
                _render_edit_mode_buttons(original_name=name, new_name=new_name, on_rename=on_rename)
            else:
                _render_view_mode_buttons(name=name, on_delete=on_delete)

def _render_edit_mode_buttons(original_name: str, new_name: str, on_rename: Callable[[str, str], None]) -> None:
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("💾 Save", key=f"save_{original_name}", use_container_width=True):
            on_rename(original_name, new_name)
    
    with btn_col2:
        if st.button("✖ Cancel", key=f"cancel_{original_name}", use_container_width=True):
            st.session_state.editing_collection = None
            st.rerun()

def _render_view_mode_buttons(name: str, on_delete: Callable[[str], None]) -> None:
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("✏️ Edit", key=f"edit_{name}", use_container_width=True):
            st.session_state.editing_collection = name
            st.rerun()
    
    with btn_col2:
        if st.button("🗑️ Delete", key=f"delete_{name}", use_container_width=True):
            confirm_delete_collection_dialog(name, on_delete)