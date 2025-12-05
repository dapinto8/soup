from core import VectorStoreAbstract
from persistence import ChromaVectorStore
from services import CollectionService, IngestionService
 
_vector_store = None
_ingestion_service = None

def get_vector_store() -> VectorStoreAbstract:
    global _vector_store
    if _vector_store is None:
        _vector_store = ChromaVectorStore()
    return _vector_store

def get_collection_service() -> CollectionService:
    _ = get_vector_store()
    return CollectionService(store=_vector_store)

def get_ingestion_service() -> IngestionService:
    global _ingestion_service
    if _ingestion_service is None:
        _ingestion_service = IngestionService(store=_vector_store)
    return _ingestion_service

