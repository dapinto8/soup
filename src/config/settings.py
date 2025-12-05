from core import LLMModelConfig
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
SRC_DIR = BASE_DIR / "src"
APP_DIR = SRC_DIR / "app"
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"


MODEL_REGISTRY: list[LLMModelConfig] = [
    LLMModelConfig(
        name="Ollama - GPT-OSS",
        provider="ollama",
        model="gpt-oss:120b-cloud"
    ),
    LLMModelConfig(
        name="Ollama - DeepSeek V3.1",
        provider="ollama",
        model="deepseek-v3.1:671b-cloud"
    ),
    LLMModelConfig(
        name="Ollama - Mistral 3",
        provider="ollama",
        model="ministral-3:8b-cloud"
    ),
    # "OpenAI - GPT-4o": LLMModelConfig(
    #     provider="openai",
    #     model="gpt-4o"
    # ),
    # "OpenAI - GPT-4o-mini": LLMModelConfig(
    #     provider="openai",
    #     model="gpt-4o-mini"
    # ),
    # "Anthropic - Claude Sonnet 4.5": LLMModelConfig(
    #     provider="anthropic",
    #     model="claude-sonnet-4-5-20250929",
    # ),
]

# Default model on first load
DEFAULT_MODEL = MODEL_REGISTRY[0]

def get_model_config(model: str) -> LLMModelConfig:
    """Get the model config for a given model name."""
    for model_config in MODEL_REGISTRY:
        if model_config.name == model:
            return model_config
    raise ValueError(f"Model {model} not found in registry")