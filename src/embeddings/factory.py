from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

def get_embedding() -> OllamaEmbeddingFunction:
    return OllamaEmbeddingFunction(model_name="mxbai-embed-large")

# from langchain_ollama import OllamaEmbeddings
# from langchain_core.embeddings import Embeddings

# def get_embedding() -> type[Embeddings]:
#     # nomic-embed-text is too slow
#     return OllamaEmbeddings(model="mxbai-embed-large")