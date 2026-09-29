"""Groq provider — the DEFAULT LLM backend (fast inference, e.g. Llama 3.3 / Kimi / etc.)."""
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_groq import ChatGroq

from app.llm.base import BaseLLMProvider


class GroqProvider(BaseLLMProvider):
    name = "groq"

    def get_chat_model(self) -> BaseChatModel:
        return ChatGroq(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            api_key=self.api_key,
        )
