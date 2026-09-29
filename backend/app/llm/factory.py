"""
LLM factory — the single place that decides *which* provider to instantiate.

Usage everywhere else in the app:

    from app.llm.factory import get_llm
    chat_model = get_llm()                      # uses LLM_PROVIDER from settings (Groq by default)
    chat_model = get_llm(provider="openai")      # explicit override, e.g. per-request

Adding a new provider = write a class implementing BaseLLMProvider + one
line in `_PROVIDER_REGISTRY`. No other file needs to change.
"""
from functools import lru_cache

from langchain_core.language_models.chat_models import BaseChatModel

from app.config import get_settings
from app.core.exceptions import LLMProviderError
from app.core.logging import logger
from app.llm.base import BaseLLMProvider
from app.llm.providers import AnthropicProvider, GroqProvider, OpenAIProvider

_PROVIDER_REGISTRY: dict[str, type[BaseLLMProvider]] = {
    "groq": GroqProvider,
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
}

_API_KEY_MAP = {
    "groq": "GROQ_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}


def _build_provider(provider_name: str, model: str | None = None) -> BaseLLMProvider:
    settings = get_settings()
    provider_cls = _PROVIDER_REGISTRY.get(provider_name)
    if provider_cls is None:
        raise LLMProviderError(
            provider_name,
            f"Unknown provider. Available: {list(_PROVIDER_REGISTRY.keys())}",
        )

    api_key = getattr(settings, _API_KEY_MAP[provider_name], "")
    if not api_key:
        raise LLMProviderError(provider_name, f"Missing API key ({_API_KEY_MAP[provider_name]} not set).")

    return provider_cls(
        model=model or settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        max_tokens=settings.LLM_MAX_TOKENS,
        api_key=api_key,
    )


@lru_cache(maxsize=8)
def _cached_chat_model(provider_name: str, model: str | None) -> BaseChatModel:
    provider = _build_provider(provider_name, model)
    logger.info(f"Instantiated LLM provider={provider_name} model={provider.model}")
    return provider.get_chat_model()


def get_llm(provider: str | None = None, model: str | None = None) -> BaseChatModel:
    """Return a ready LangChain chat model for the configured (or overridden) provider."""
    settings = get_settings()
    provider_name = (provider or settings.LLM_PROVIDER).lower()
    return _cached_chat_model(provider_name, model)


def available_providers() -> list[str]:
    return list(_PROVIDER_REGISTRY.keys())
