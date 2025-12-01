from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStore
from core import VectorStoreAbstract

@tool(
    name="search",
    description="Search the vector store for the most relevant documents",
)
def search(vector_store: VectorStoreAbstract, query: str) -> list[Document]:
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )
    return retriever.invoke(query)

@tool(
    name="similarity_search",
    description="Search the vector store for the most relevant documents",
)
def search_with_score(vector_store: VectorStore, query: str, score_threshold: float = 0.5) -> list[Document]:
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": score_threshold}
    )
    return retriever.invoke(query)
