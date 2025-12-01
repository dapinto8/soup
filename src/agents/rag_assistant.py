from langchain.agents import create_agent
from tools import search, search_with_score
from core import VectorStoreAbstract

SYSTEM_PROMPT = """
You are a helpful assistant that can answer questions and help with tasks.
"""

class RAGAssistant:
    """
    A RAG assistant. This is the main class for the RAG assistant.
    """

    def __init__(self, model: str, vector_store: VectorStoreAbstract):
        self.agent = create_agent(
            model=model,
            tools=[search(vector_store), search_with_score(vector_store)],
            system_prompt=SYSTEM_PROMPT,
            verbose=True
        )

    def run(self, query: str) -> str:
        return self.agent.invoke({
            "messages": [
                {"role": "user", "content": query}
            ]
        })


