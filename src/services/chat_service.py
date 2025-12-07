from dataclasses import dataclass
from core import VectorStoreAbstract
from shared import logger
from typing import AsyncGenerator
from langchain_core.documents import Document
from agents import RAGAssistant

@dataclass
class StreamChunk:
    """Represents a chunk of streamed response."""

    type: str  # "token", "sources", "error", "done"
    content: str = ""
    sources: list[Document] | None = None

class ChatService:
    """
    A service for chatting with a model.
    """

    def __init__(self, store: VectorStoreAbstract):
        """Initialize ChatService."""
        self.store = store
        logger.info("ChatService initialized")

    async def stream_chat(self, query: str, collection: str, model: str) -> AsyncGenerator[StreamChunk]:
        try:
            assistant = RAGAssistant(model=model, store=self.store, collection_name=collection)
            logger.info(f"Assistant created: {assistant}")

            full_response = ""

            # Stream events
            async for event in assistant.astream(query):
                event_type = event.get("event", "")

                # Handle LLM token streaming
                if event_type == "on_chat_model_stream":
                    chunk = event.get("data", {}).get("chunk")
                    if chunk and hasattr(chunk, "content") and chunk.content:
                        full_response += chunk.content
                        yield StreamChunk(type="token", content=chunk.content)

                # Handle tool start
                elif event_type == "on_tool_start":
                    tool_name = event.get("name", "unknown")
                    logger.info(f"Tool started: {tool_name}")

                # Handle tool end
                elif event_type == "on_tool_end":
                    tool_name = event.get("name", "unknown")
                    logger.info(f"Tool ended: {tool_name}")

                # Handle errors
                elif event_type == "on_error":
                    error_msg = event.get("data", {}).get("error", "Unknown error")
                    logger.error(f"Stream error event: {error_msg}")
                    yield StreamChunk(
                        type="error",
                        content="Something went wrong. Please try again later.",
                    )
                    return

            # After streaming complete, yield sources
            sources = []  #assistant.get_sources()
            logger.info(f"Sources: {len(sources)}")
            # if sources:
            #     # Deduplicate sources by content
            #     unique_sources = self._deduplicate_sources(sources)
            #     yield StreamChunk(type="sources", sources=unique_sources)

            # Signal completion
            yield StreamChunk(type="done", content=full_response)

            logger.info(
                f"stream_chat complete: {len(full_response)} chars, "
                f"{full_response} response, "
                f"{len(sources)} sources"
            )

        except Exception as e:
            logger.error(f"Error streaming chat: {e}")
            yield StreamChunk(
                type="error",
                content="Something went wrong. Please try again later.",
            )

    def _deduplicate_sources(self, sources: list[Document]) -> list[Document]:
        seen = set()
        unique = []

        for doc in sources:
            content_hash = hash(doc.page_content[:200])  # Hash first 200 chars
            if content_hash not in seen:
                seen.add(content_hash)
                unique.append(doc)

        return unique

    def format_sources_for_display(self, sources: list[Document]) -> list[dict]:
        formatted = []

        for doc in sources:
            logger.info(f"Document: {doc}")
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page")

            # Create preview (first 200 chars)
            preview = doc.page_content[:200]
            if len(doc.page_content) > 200:
                preview += "..."

            formatted.append(
                {
                    "source": source,
                    "page": page,
                    "preview": preview,
                    "full_content": doc.page_content,
                }
            )

        return formatted
