from abc import ABC, abstractmethod
from langchain_core.documents import Document

class LoaderAbstract(ABC):
    """
    Abstract class for the loader. This is the interface that all loader implementations must implement.
    """

    @staticmethod
    @abstractmethod
    def load(source: str) -> list[Document]:
        pass
