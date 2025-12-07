# Soup RAG

A RAG (Retrieval-Augmented Generation) application with Streamlit UI. Upload PDFs, create collections, and chat with your documents using local LLMs via Ollama.

## Prerequisites

- Python 3.13+
- [Ollama](https://ollama.ai/) - running locally with models pulled (e.g., `ollama pull llama3`)
- [ChromaDB](https://www.trychroma.com/) - vector database (installed via pip)

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/main.py
```

## Project Structure

```
src/
    main.py              # Entry point
    dependencies.py      # DI container
    app/
        streamlit_app.py # Main Streamlit app
        pages/           # Streamlit pages (Home, Chat, Upload, Collections)
        components/      # UI components
    agents/
        rag_assistant.py # RAG agent with search tools
        llms.py          # LLM configuration
        tools.py         # Search tools
    services/
        chat_service.py       # Chat streaming service
        collection_service.py # Collection management
        ingestion_service.py  # PDF ingestion
    core/                # Abstract interfaces
    embeddings/          # Embedding models
    loaders/             # Document loaders
    persistence/         # ChromaDB integration
    config/              # App configuration
    shared/              # Logging, utilities
    assets/              # Static assets
```

## Features

- PDF upload & chunking
- Vector storage with ChromaDB
- Chat with documents using RAG
- Multiple collections support
- Streaming responses
