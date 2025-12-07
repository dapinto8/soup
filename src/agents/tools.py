from langchain_core.tools import tool
from langchain_core.documents import Document

from core import VectorStoreAbstract
from shared import logger
from typing import Callable

# Constants
RETRIEVAL_K = 5

def create_search_tool(vector_store: VectorStoreAbstract, collection_name: str, sources_accumulator: list[Document] | None = None) -> Callable[[str], str]:

    logger.info(f"Creating search tool with collection: {collection_name}")

    @tool(
        "search_documents",
        description=(
            "Search the knowledge base for relevant information. "
            "Use this tool to find context for answering user questions. "
            "Input should be a search query string."
        ),
    )
    def search(query: str) -> str:
        logger.info(f"Searching documents with query: {query[:100]}...")

        try:
            docs = vector_store.similarity_search(collection_name, query, k=RETRIEVAL_K)
            # logger.info(f"Docs: {docs}")

            if not docs:
                logger.info("No documents found for query")
                return "No relevant documents found in the knowledge base."

            logger.info(f"Found {len(docs)} documents")

            # Capture sources for UI if accumulator provided
            if sources_accumulator is not None:
                sources_accumulator.extend(docs)

            # Format results for the LLM
            formatted_results = _format_documents(docs)
            return formatted_results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return f"Search encountered an error. Please try again later."

    return search


def _format_documents(docs: list[Document]) -> str:
    return "\n\n---\n\n".join([doc.page_content for doc in docs])