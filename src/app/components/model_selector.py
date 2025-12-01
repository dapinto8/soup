import streamlit as st
from config import MODEL_REGISTRY

def model_selector() -> None:
    st.sidebar.markdown("### ✨ LLM Model")

    ## LLM Model Selector
    model_names = list(MODEL_REGISTRY.keys())
    current_index = model_names.index(st.session_state.selected_model)

    selected_model = st.sidebar.selectbox(
        "Select a model",
        options=model_names,
        index=current_index,
        key="model_selector_dropdown",
        help="Select the model to use for the RAG assistant",
    )

    if selected_model != st.session_state.selected_model:
        st.session_state.selected_model = selected_model
        st.rerun()

def get_selected_model() -> str:
    return st.session_state.selected_model