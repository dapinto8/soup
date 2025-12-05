import streamlit as st

def home_page() -> None:
    """Home page."""
    st.title("🍜 Welcome to Soup RAG")

    # Page config
    st.set_page_config(
        page_title="Soup RAG",
        page_icon="🍜",
        # layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        A RAG (Retrieval-Augmented Generation) chat application for learning
        and experimenting with document-based AI conversations.
        
        ### Getting Started
        
        1. **Select a Model** - Choose your LLM from the sidebar. 
           The embedding model is automatically selected for compatibility.
        
        2. **Create a Collection** - Click "New Collection" in the sidebar
           to create a document collection.
        
        3. **Upload Documents** - Go to the **Upload** page to add PDFs or text.
        
        4. **Start Chatting** - Go to the **Chat** page to ask questions
           about your documents.
        
        ---
        
        ### Current Configuration
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Model:**")
        if "selected_model" in st.session_state:
            st.code(st.session_state.selected_model.name)
        else:
            st.code("Not selected")
    
    with col2:
        st.markdown("**Collection:**")
        if "selected_collection" in st.session_state:
            st.code(st.session_state.selected_collection)
        else:
            st.code("Not selected")

home_page()
