from pathlib import Path
from core import VectorStoreAbstract, IngestionResult
from loaders import get_loader
from shared import split_documents
from langchain_core.documents import Document
from shared import logger


class IngestionService:
    """
    A service for ingesting data into a vector store.
    """
    def __init__(self, store: VectorStoreAbstract):
        self._vector_store = store

    def ingest_file(self, collection_name: str, file_path: str) -> IngestionResult:
        path = Path(file_path)

        try:
            logger.info(f"Ingesting file: {path.name}")
            loader = get_loader(path.suffix)
            documents = loader.load(path)

            logger.info(f"Loaded {len(documents)} documents")

            for doc in documents:
                doc.metadata["original_file"] = path.name

            return self._process_documents(collection_name, documents, path.name)

        except Exception as e:
            return IngestionResult(
                success=False,
                document_name=path.name,
                chunk_count=0,
                collection_name=collection_name,
                message=f"Failed to ingest documents: {e}",
            )

    def _process_documents(self, collection_name: str, documents: list[Document], document_name: str) -> IngestionResult:
        # Split into chunks
        chunks = split_documents(documents)
        logger.info(f"Split into {len(chunks)} chunks")

        if not chunks:
            return IngestionResult(
                success=False,
                document_name=document_name,
                chunk_count=0,
                collection_name=collection_name,
                message="No content to ingest after splitting",
            )
        
        # Store in vector database
        self._vector_store.add_documents(collection_name, chunks)
        logger.info(f"Added {len(chunks)} chunks to collection {collection_name}")

        return IngestionResult(
            success=True,
            document_name=document_name,
            chunk_count=len(chunks),
            collection_name=collection_name,
            message=f"Successfully ingested {len(chunks)} chunks",
        )
