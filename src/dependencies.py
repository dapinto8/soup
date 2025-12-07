from core import VectorStoreAbstract
from persistence import ChromaVectorStore
from services import CollectionService, IngestionService, ChatService
 
_vector_store = None
_ingestion_service = None
_collection_service = None
_chat_service = None

def get_vector_store() -> VectorStoreAbstract:
    global _vector_store
    if _vector_store is None:
        _vector_store = ChromaVectorStore()
    return _vector_store

def get_collection_service() -> CollectionService:
    global _collection_service
    if _collection_service is None:
        _collection_service = CollectionService(store=_vector_store)
    return _collection_service

def get_ingestion_service() -> IngestionService:
    global _ingestion_service
    if _ingestion_service is None:
        _ingestion_service = IngestionService(store=_vector_store)
    return _ingestion_service

def get_chat_service() -> ChatService:
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService(store=_vector_store)
    return _chat_service

get_vector_store()