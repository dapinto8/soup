import chromadb
import uuid
from core import VectorStoreAbstract
from langchain_core.documents import Document
from embeddings import get_embedding

class ChromaVectorStore(VectorStoreAbstract):
    """
    A Chroma vector store. This is the implementation of the VectorStoreAbstract interface for the Chroma vector store.
    """
    def __init__(self, model: str):
        self.client = chromadb.HttpClient(host="localhost", port=8000)
        self.embedding = get_embedding(model)
    
    def create_collection(self, collection_name: str) -> None:
        self.client.create_collection(name=collection_name, embedding_function=self.embedding.embed_documents)

    def collection_exists(self, collection_name: str) -> bool:
        return self.client.get_collection(name=collection_name) is not None

    def add_documents(self, collection_name: str, documents: list[Document]) -> None:
        documents_with_ids = self._get_documents_with_ids(documents)
        self.client.get_collection(name=collection_name).add(documents_with_ids)

    def _get_documents_with_ids(self, documents: list[Document]) -> list[Document]:
        for document in documents:
            document.metadata["id"] = str(uuid.uuid4())
        return documents