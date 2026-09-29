"""
Centralized application configuration.

All environment-driven settings live here so that the rest of the codebase
never reads `os.environ` directly. This is what makes LLM providers, search
providers and embedding providers swappable purely through `.env` — the
factories in `app/llm/factory.py` and `app/search/factory.py` read from
this object, not from hardcoded values.
"""
from functools import lru_cache
import json
from typing import Annotated, List, Literal

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ---------------- App ----------------
    APP_ENV: str = "development"
    APP_NAME: str = "AI Research Assistant"
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: Annotated[List[str], NoDecode] = ["http://localhost:3000"]

    # ---------------- Database ----------------
    DATABASE_URL: str = (
        "postgresql+asyncpg://research_user:research_pass@localhost:5432/research_assistant"
    )
    DB_ECHO: bool = False

    # ---------------- LLM provider (pluggable) ----------------
    LLM_PROVIDER: Literal["groq", "openai", "anthropic"] = "groq"
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 4096

    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # ---------------- Embeddings (RAG) ----------------
    EMBEDDING_PROVIDER: Literal["huggingface", "openai"] = "huggingface"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIM: int = 384  # bge-small-en-v1.5 output dim; update if you swap models

    # ---------------- Search providers (pluggable) ----------------
    SEARCH_PROVIDERS: Annotated[List[str], NoDecode] = ["arxiv", "semantic_scholar"]
    SEMANTIC_SCHOLAR_API_KEY: str = ""
    MAX_PAPERS_PER_SOURCE: int = 15

    # ---------------- RAG chunking ----------------
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 120
    TOP_K_RETRIEVAL: int = 8

    # ---------------- Observability ----------------
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "research-assistant"

    @field_validator("SEARCH_PROVIDERS", "BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _split_csv(cls, v):
        if isinstance(v, str):
            value = v.strip()
            if value.startswith("["):
                return json.loads(value)
            return [item.strip() for item in value.split(",") if item.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton — import this everywhere instead of instantiating Settings()."""
    return Settings()
