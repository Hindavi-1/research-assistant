"""OpenAI provider — swap-in alternative behind the same BaseLLMProvider interface."""
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.llm.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    name = "openai"

    def get_chat_model(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            api_key=self.api_key,
        )
