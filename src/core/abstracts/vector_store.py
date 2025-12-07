from abc import ABC, abstractmethod
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from core.entities import Collection, LLMModelConfig

class VectorStoreAbstract(ABC):
    """
    Abstract class for the vector store. This is the interface that all vector store implementations must implement.
    """

    @abstractmethod
    def create_collection(self, collection_name: str, model_config: LLMModelConfig) -> Collection:
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        pass
    
    @abstractmethod
    def get_collections(self) -> list[Collection]:
        pass

    @abstractmethod
    def add_documents(self, collection_name: str, documents: list[Document]) -> None:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> None:
        pass

    @abstractmethod
    def similarity_search(self, collection_name: str, query: str, k: int) -> list[Document]:
        pass
