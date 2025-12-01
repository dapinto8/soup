from core import VectorStoreAbstract
from loaders import get_loader
from shared import split_documents


class IngestionService:
    """
    A service for ingesting data into a vector store.
    """
    def __init__(self, vector_store: VectorStoreAbstract):
        self.vector_store = vector_store

    def ingest(self, model: str, collection_name: str, source: str, source_type: str) -> None:
        try:
            if not self.vector_store.collection_exists(collection_name):
                self.vector_store.create_collection(collection_name, embedding_function=None)

            loader = get_loader(source_type)
            documents = loader.load(source)
            chunked_documents = split_documents(documents)
            self.vector_store.add_documents(collection_name, chunked_documents)
        except Exception as e:
            raise ValueError(f"Failed to ingest documents: {e}")