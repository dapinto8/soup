from core import LLMModelConfig

MODEL_REGISTRY: dict[str, LLMModelConfig] = {
    "Ollama - Llama 3.2": LLMModelConfig(
        provider="ollama",
        model="llama3.2"
    ),
    "Ollama - Mistral": LLMModelConfig(
        provider="ollama",
        model="mistral"
    ),
    "OpenAI - GPT-4o": LLMModelConfig(
        provider="openai",
        model="gpt-4o"
    ),
    "OpenAI - GPT-4o-mini": LLMModelConfig(
        provider="openai",
        model="gpt-4o-mini"
    ),
    "Anthropic - Claude Sonnet 4.5": LLMModelConfig(
        provider="anthropic",
        model="claude-sonnet-4-5-20250929",
    ),
}

# Default model on first load
DEFAULT_MODEL = "Ollama - Llama 3.2"

def get_model_config(model: str) -> LLMModelConfig:
    """Get the model config for a given model name."""
    if model not in MODEL_REGISTRY:
        raise ValueError(f"Model {model} not found in registry")
    return MODEL_REGISTRY[model]