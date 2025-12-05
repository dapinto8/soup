from dataclasses import dataclass

@dataclass
class IngestionResult:
    success: bool
    document_name: str
    chunk_count: int
    collection_name: str
    message: str