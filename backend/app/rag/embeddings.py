"""
Embedding model access — also kept behind a light factory so the embedding
backend (local HuggingFace model vs. OpenAI embeddings API) is swappable via
`.env`, consistent with the LLM/search provider pattern used elsewhere.
"""
from functools import lru_cache

from langchain_core.embeddings import Embeddings

from app.config import get_settings


@lru_cache(maxsize=1)
def get_embedding_model() -> Embeddings:
    settings = get_settings()

    if settings.EMBEDDING_PROVIDER == "huggingface":
        from langchain_community.embeddings import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

    if settings.EMBEDDING_PROVIDER == "openai":
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY)

    raise ValueError(f"Unknown EMBEDDING_PROVIDER: {settings.EMBEDDING_PROVIDER}")


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    model = get_embedding_model()
    return model.embed_documents(texts)


def embed_query(text: str) -> list[float]:
    model = get_embedding_model()
    return model.embed_query(text)
