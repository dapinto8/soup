from shared import logger
from .tools import create_search_tool
from core import VectorStoreAbstract
from typing import AsyncIterator, Any
from .llms import get_chat_model
from langchain_core.documents import Document
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


SYSTEM_PROMPT = """
You are a helpful assistant that answers questions based on documents in a knowledge base.

SEARCH STRATEGY:
1. Search the knowledge base using the search_documents tool
2. If results are relevant, answer immediately based on them
3. If results seem off-topic, you may reformulate and search ONCE more with different keywords
4. Maximum 2-3 searches per question — then answer with whatever you found

WHEN TO REFORMULATE:
- Results don't address the user's actual question
- You need information on a different aspect of the question
- Initial query was too broad or too narrow

WHEN TO STOP AND ANSWER:
- Results contain relevant information (even if partial)
- You've already searched 2-3 times
- Reformulation is unlikely to help

ANSWERING:
- Base your answer on retrieved documents
- If information is incomplete, say what you found and what's missing
- Be concise and cite sources when relevant
"""

RETRIEVAL_K = 5

class RAGAssistant:
    """
    A RAG assistant. This is the main class for the RAG assistant.
    """

    def __init__(self, model: str, store: VectorStoreAbstract, collection_name: str):
        self._model = model
        self.vector_store = store
        self._collection_name = collection_name
        self.sources: list[Document] = []
        self._agent = self._create_agent()

    def _create_agent(self):
        """Create the agent executor with tools."""
        # Create LLM
        chat_model = get_chat_model(model_name=self._model)

        # Create tools with sources accumulator for capturing retrieved docs
        search_tool = create_search_tool(vector_store=self.vector_store, collection_name=self._collection_name, sources_accumulator=self.sources)
        tools = [search_tool]
        

        # Create agent
        logger.info(f"Creating agent with model: {self._model}")
        return create_agent(model=chat_model, tools=tools, system_prompt=SYSTEM_PROMPT)
        

    async def astream(self, query: str) -> AsyncIterator[dict[str, Any]]:
        logger.info(f"Starting astream for query: {query[:100]}...")
        # Clear sources from previous invocation
        self.sources.clear()

        logger.info(f"Starting astream for query: {query[:100]}...")

        # Create prompt template
        # TODO: Study more about this
        prompt_template  = ChatPromptTemplate.from_messages(
            [
                # ("system", SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
                # MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        ) 
        prompt = prompt_template.format(input=query)

        try:
            async for event in self._agent.astream_events(
                {"messages": [{"role": "user", "content": prompt}]},
                config={"recursion_limit": 8},
                version="v2"
            ):
                yield event

        except Exception as e:
            logger.error(f"Stream error: {e}")
            # Yield error event for handling upstream
            yield {
                "event": "on_error",
                "data": {"error": str(e)},
            }

    def stream_sync(self, query: str):
        self.sources.clear()

        logger.info(f"Starting sync stream for query: {query[:100]}...")

        try:
            for chunk in self._agent.stream({"messages": [{"role": "user", "content": query}]}, stream_mode="messages"):
                yield chunk

        except Exception as e:
            logger.error(f"Stream error: {e}")
            raise

    def invoke(self, query: str) -> dict[str, Any]:
        self.sources.clear()

        logger.info(f"Invoking agent for query: {query[:100]}...")

        try:
            result = self._agent.invoke({"messages": [{"role": "user", "content": query}]})
            return result

        except Exception as e:
            logger.error(f"Invoke error: {e}")
            raise


    def get_sources(self) -> list[Document]:
        logger.info(f"Getting sources: {len(self.sources)}")
        return self.sources.copy()
