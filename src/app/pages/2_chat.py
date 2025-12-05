import streamlit as st
from app.components import get_selected_model, get_selected_collection

def chat_page() -> None:
    """Chat page."""
    st.title("💬 Chat")

    # Page config
    st.set_page_config(
        page_title="Chat",
        page_icon="💬",
        # layout="wide",
        initial_sidebar_state="expanded",
    )


    # Show current configuration
    col1, col2 = st.columns(2)
    with col1:
        model = get_selected_model()
        st.info(f"🤖 Model: **{model.name}**")
    with col2:
        collection = get_selected_collection()
        if collection:
            st.info(f"📁 Collection: **{collection}**")
        else:
            st.warning("No collection selected")

    st.markdown("---")
    
    # Placeholder content
    st.markdown(
        """
        ### 🚧 Coming Soon
        
        This page will feature:
        
        - **Chat Interface** — Conversational UI with message history
        - **RAG Retrieval** — Automatic context retrieval from your documents
        - **Source Citations** — See which documents informed each response
        - **Streaming Responses** — Real-time response generation
        
        ---
        
        For now, make sure you have:
        1. Selected a model in the sidebar
        2. Created or selected a collection
        3. Uploaded some documents on the **Upload** page
        """
    )

    # Placeholder chat container (for future implementation)
    st.markdown("### Chat Preview")
    
    chat_container = st.container(height=400)
    with chat_container:
        st.chat_message("assistant").write(
            "👋 Hello! I'm your RAG assistant. Once implemented, I'll help you "
            "chat with your documents. Upload some documents first, then come back here!"
        )
    
    # Disabled input placeholder
    st.chat_input(
        "Ask a question about your documents...",
        disabled=True,
    )
    
    st.caption("💡 Chat functionality will be implemented in the next phase.")


chat_page()