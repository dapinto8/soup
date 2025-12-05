import streamlit as st
from config import MODEL_REGISTRY
from core import LLMModelConfig

def model_selector() -> None:
    st.sidebar.markdown("### ✨ LLM Model")

    ## LLM Model Selector
    #current_index = MODEL_REGISTRY.index(st.session_state.selected_model)

    selected_model = st.sidebar.selectbox(
        "Select a model",
        options=MODEL_REGISTRY,
        # index=current_index,
        format_func=lambda x: x.name,
        key="model_selector_dropdown",
        help="Select the model to use for the RAG assistant",
    )

    if selected_model != st.session_state.selected_model:
        st.session_state.selected_model = selected_model
        st.rerun()

def get_selected_model() -> LLMModelConfig:
    return st.session_state.selected_model