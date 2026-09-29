"""
LLM provider interface.

Every concrete provider (Groq, OpenAI, Anthropic, ...) implements this
interface. Nothing else in the codebase (graph nodes, services) imports a
provider class directly — they always go through `app.llm.factory.get_llm()`
and depend only on `BaseLLMProvider` / the returned LangChain chat model.
This is what makes swapping providers a one-line `.env` change.
"""
from abc import ABC, abstractmethod
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel


class BaseLLMProvider(ABC):
    """Wraps a LangChain-compatible chat model behind a uniform construction interface."""

    name: str = "base"

    def __init__(self, model: str, temperature: float, max_tokens: int, api_key: str, **kwargs: Any):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key
        self.extra_kwargs = kwargs

    @abstractmethod
    def get_chat_model(self) -> BaseChatModel:
        """Return a ready-to-use LangChain BaseChatModel instance (used by LangGraph nodes)."""
        raise NotImplementedError

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{self.__class__.__name__} model={self.model}>"
