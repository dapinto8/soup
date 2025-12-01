from abc import ABC, abstractmethod
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStoreRetriever

class VectorStoreAbstract(ABC):
    """
    Abstract class for the vector store. This is the interface that all vector store implementations must implement.
    """

    @abstractmethod
    def as_retriever(self) -> VectorStoreRetriever:
        pass

    @abstractmethod
    def create_collection(self, collection_name: str) -> None:
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def add_documents(self, collection_name: str, documents: list[Document]) -> None:
        pass
