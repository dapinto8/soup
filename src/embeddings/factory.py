from langchain_ollama import OllamaEmbeddings
from langchain_core.embeddings import Embeddings

EMBEDDINGS: dict[str, type[Embeddings]] = {
    "ollama": OllamaEmbeddings(model="nomic-embed-text"),
}

def get_embedding(model: str) -> type[Embeddings]:
    """
    Factory function that returns the appropriate embedding class based on model.
    """
    embedding = EMBEDDINGS.get(model)
    if embedding is None:
        raise ValueError(f"Unsupported model: {model}")
    return embedding