
import streamlit as st
from app.components import sidebar, get_selected_collection


def _upload_pdf() -> None:
    # st.subheader("📄 PDF Upload")
    # st.write("Upload a PDF file to your collection.")
    st.markdown("#### 📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a PDF document to add to the collection",
    )

def _upload_text() -> None:
    # st.subheader("📝 Text Input")
    st.markdown("#### 📝 Upload Text")

    document_name = st.text_input(
        "Document Name",
        placeholder="e.g., Meeting Notes Q4 2024",
        help="Give your document a descriptive name",
    )
    
    text_content = st.text_area(
        "Text Content",
        height=200,
        placeholder="Paste or type your text content here...",
        help="The text that will be processed and added to the collection",
    )


def upload_page() -> None:
    """Upload page."""
    st.title("📤 Upload Documents")

    # Page config
    st.set_page_config(
        page_title="Upload",
        page_icon="📄",
        # layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        "Add documents to your collection for RAG-powered chat. "
        "Choose a source type below."
    )

    # Check if collection is selected
    collection = get_selected_collection()
    if collection:
        st.info(f"📁 Uploading to collection: **{collection}**")
    
    st.markdown("---")
    
    # Source type tabs
    tab_pdf, tab_text = st.tabs(["📄 PDF Upload", "📝 Text Input"])

    with tab_pdf:
        _upload_pdf()
    with tab_text:
        _upload_text()


upload_page()