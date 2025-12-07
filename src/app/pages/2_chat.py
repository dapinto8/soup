import asyncio
import streamlit as st
from app.components import get_selected_model, get_selected_collection
from dependencies import get_chat_service
from shared import logger

def init_chat_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []


def _render_sources(sources: list[dict]):
    if not sources:
        return

    with st.expander(f"📚 Sources ({len(sources)} documents)", expanded=False):
        for i, source in enumerate(sources, 1):
            source_name = source.get("source", "Unknown")
            page = source.get("page")
            preview = source.get("preview", "")

            # Header with source info
            header = f"**{i}. {source_name}**"
            if page is not None:
                header += f" (Page {page})"

            st.markdown(header)
            st.caption(preview)

            if i < len(sources):
                st.divider()


def _redner_message(message: dict):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Render sources if present (assistant messages only)
        if message["role"] == "assistant" and message.get("sources"):
            _render_sources(message["sources"])


def _render_chat_history():
    for message in st.session_state.messages:
        _redner_message(message)


async def _stream_response(query: str, collection: str, model: str) -> tuple[str, list[dict]]:
    chat_service = get_chat_service()

    full_response = ""
    sources = []

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        async for chunk in chat_service.stream_chat(query, collection, model):
            logger.info(f"Chunk: {chunk}")
            if chunk.type == "token":
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")

            elif chunk.type == "sources":
                sources = chat_service.format_sources_for_display(chunk.sources)

            elif chunk.type == "error":
                full_response = chunk.content
                message_placeholder.markdown(full_response)
                break

            elif chunk.type == "done":
                # Remove cursor
                message_placeholder.markdown(full_response)

        # Render sources after streaming complete
        if sources:
            _render_sources(sources)

    return full_response, sources


def _handle_user_input(prompt: str, collection: str, model: str):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream response
    full_response, sources = asyncio.run(
        _stream_response(prompt, collection, model)
    )

    # Add assistant message to history (with sources)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response,
            "sources": sources,
        }
    )


def chat_page() -> None:
    """Chat page."""
    st.title("💬 Chat")

    init_chat_state()

    model = get_selected_model()
    collection = get_selected_collection()

    st.markdown("---")

    # Check if ready to chat
    if not model or not collection:
        st.warning("⚠️ Please select a model and collection from the sidebar to start chatting.")
        return

    # Render chat history
    _render_chat_history()

    # Chat input
    if prompt := st.chat_input("Ask me anything about your documents..."):
        _handle_user_input(prompt, collection, model.name)


chat_page()