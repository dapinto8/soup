
from langchain_core.language_models.chat_models import BaseChatModel
from shared import logger
from config.settings import get_model_config


class UnsupportedModelError(Exception):
    """Raised when model provider is not supported."""

    pass


def get_chat_model(model_name: str, **kwargs) -> BaseChatModel:
    model_config = get_model_config(model_name)

    logger.info(f"Creating chat model: provider={model_config.provider}, model={model_config.model}")

    if model_config.provider == "ollama":
        return _create_ollama_model(model_config.model, **kwargs)
    elif model_config.provider == "openai":
        return _create_openai_model(model_config.model, **kwargs)
    elif model_config.provider == "anthropic":
        return _create_anthropic_model(model_config.model, **kwargs)
    else:
        raise UnsupportedModelError(
            f"Unsupported provider: '{model_config.provider}'. "
            f"Supported providers: ollama, openai, anthropic"
        )


def _create_ollama_model(model: str, **kwargs) -> BaseChatModel:
    """Create Ollama chat model."""
    from langchain_ollama import ChatOllama

    return ChatOllama(
        model=model,
        **kwargs,
    )


def _create_openai_model(model: str, **kwargs) -> BaseChatModel:
    """Create OpenAI chat model."""
    # from langchain_openai import ChatOpenAI

    # return ChatOpenAI(
    #     model=model,
    #     **kwargs,
    # )


def _create_anthropic_model(model: str, **kwargs) -> BaseChatModel:
    """Create Anthropic chat model."""
    # from langchain_anthropic import ChatAnthropic

    # return ChatAnthropic(
    #     model=model,
    #     **kwargs,
    # )