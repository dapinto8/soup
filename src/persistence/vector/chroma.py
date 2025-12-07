import chromadb
import uuid
from core import VectorStoreAbstract, Collection
from langchain_core.documents import Document
from embeddings import get_embedding
from langchain_core.vectorstores.base import VectorStoreRetriever
from shared import logger

class ChromaVectorStore(VectorStoreAbstract):
    """
    A Chroma vector store. This is the implementation of the VectorStoreAbstract interface for the Chroma vector store.
    """
    def __init__(self):
        self._client = chromadb.HttpClient(host="localhost", port=8000)
    
    def create_collection(self, collection_name: str) -> Collection:
        collection = self._client.create_collection(name=collection_name, embedding_function=get_embedding())
        return Collection(id=collection.id, name=collection.name, metadata=collection.metadata)

    def collection_exists(self, collection_name: str) -> bool:
        try:
            _ = self._client.get_collection(name=collection_name)
            return True
        except Exception:
            return False

    def get_collections(self) -> list[Collection]:
        return [Collection(id=collection.id, name=collection.name, metadata=collection.metadata) for collection in self._client.list_collections()]

    def add_documents(self, collection_name: str, documents: list[Document]) -> None:
        logger.info(f"Adding {len(documents)} documents to collection {collection_name}")
        collection = self._client.get_collection(name=collection_name)

        ids, docs_contents, metadatas = [], [], []
        for document in documents:
            ids.append(str(uuid.uuid4()))
            docs_contents.append(document.page_content)
            metadatas.append(document.metadata)

        collection.add(ids=ids, documents=docs_contents, metadatas=metadatas)

    def _get_documents_with_ids(self, documents: list[Document]) -> list[Document]:
        for document in documents:
            document.metadata["id"] = str(uuid.uuid4())
        return documents

    def delete_collection(self, collection_name: str) -> None:
        try:
            self._client.delete_collection(name=collection_name)
        except Exception as e:
            raise ValueError(f"Failed to delete collection: {e}")

    def similarity_search(self, collection_name: str, query: str, k: int) -> list[Document]:
        result = self._client.get_collection(name=collection_name).query(query_texts=query, n_results=k)
        # logger.info(f"Results: {result}")

        documents = []
        for document, metadata in zip(result["documents"], result["metadatas"]):
            documents.append(Document(page_content=document[0], metadata=metadata[0]))

        return documents