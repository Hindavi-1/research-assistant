"""
Search/discovery provider interface.

Every literature source (arXiv, Semantic Scholar, Google Scholar, ...)
implements this interface and returns a list of `RawPaperResult` — a
provider-agnostic shape. Nothing downstream (RAG ingestion, LangGraph nodes)
needs to know which source a paper came from. New sources are added by
writing one class and registering it in `app.search.factory`.
"""
from abc import ABC, abstractmethod

from app.schemas.paper import RawPaperResult


class BaseSearchProvider(ABC):
    name: str = "base"

    def __init__(self, api_key: str | None = None, max_results: int = 15):
        self.api_key = api_key
        self.max_results = max_results

    @abstractmethod
    async def search(self, query: str) -> list[RawPaperResult]:
        """Search this provider for the given query, returning normalized results."""
        raise NotImplementedError
