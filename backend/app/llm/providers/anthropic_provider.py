"""Anthropic provider — swap-in alternative behind the same BaseLLMProvider interface."""
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel

from app.llm.base import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):
    name = "anthropic"

    def get_chat_model(self) -> BaseChatModel:
        return ChatAnthropic(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            api_key=self.api_key,
        )
