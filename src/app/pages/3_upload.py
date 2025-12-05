
import streamlit as st
from config import UPLOADS_DIR
from app.components import get_selected_collection
from dependencies import get_ingestion_service
from shared import logger

def _check_collection_ready() -> bool:
    collection = get_selected_collection()
    if not collection:
        st.warning(
            "⚠️ No collection selected. Please create or select a collection "
            "from the sidebar before uploading documents."
        )
        return False
    return True 

def _save_uploaded_file(uploaded_file: st.file_uploader) -> str:
    save_path = UPLOADS_DIR / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

def _upload_pdf() -> None:
    st.markdown("#### 📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a PDF document to add to the collection",
    )

    if uploaded_file is not None:
        st.success(f"File ready: **{uploaded_file.name}** ({uploaded_file.size:,} bytes)")

        if st.button("🚀 Ingest PDF", type="primary", key="ingest_pdf_btn"):
            if not _check_collection_ready():
                return

            with st.spinner("Processing PDF..."):
                # Save file
                file_path = _save_uploaded_file(uploaded_file)
                logger.info(f"Ingesting file: {file_path}")

                # Ingest
                collection = get_selected_collection()
                ingestion_service = get_ingestion_service()
                result = ingestion_service.ingest_file(collection_name=collection, file_path=file_path)
                logger.info(f"Ingestion result: {result}")

                if result.success:
                    st.success(f"✅ **Success!** Ingested `{result.document_name}` into collection `{collection}`")
                    logger.info(f"Ingested {result.chunk_count} chunks into collection {collection}")
                    # Track ingested document
                    # if "ingested_documents" not in st.session_state:
                    #     st.session_state.ingested_documents = []
                    # st.session_state.ingested_documents.append({
                    #     "name": result.document_name,
                    #     "type": "pdf",
                    #     "chunks": result.chunk_count,
                    #     "collection": result.collection_name,
                    # })
                else:
                    st.error(f"❌ **Failed:** {result.message}")
                    logger.error(f"Failed to ingest {result.document_name} into collection {collection}: {result.message}")


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