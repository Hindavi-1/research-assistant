"""Semantic Scholar search provider — free tier available, API key optional (higher rate limit with key)."""
import httpx

from app.core.exceptions import SearchProviderError
from app.core.logging import logger
from app.schemas.paper import RawPaperResult
from app.search.base import BaseSearchProvider

_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
_FIELDS = "title,abstract,authors,year,url,openAccessPdf,citationCount,venue,externalIds"


class SemanticScholarProvider(BaseSearchProvider):
    name = "semantic_scholar"

    async def search(self, query: str) -> list[RawPaperResult]:
        headers = {"x-api-key": self.api_key} if self.api_key else {}
        params = {"query": query, "limit": self.max_results, "fields": _FIELDS}

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.get(_BASE_URL, params=params, headers=headers)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPError as exc:
            logger.exception("Semantic Scholar search failed")
            raise SearchProviderError(self.name, str(exc)) from exc

        results: list[RawPaperResult] = []
        for item in data.get("data", []):
            pdf = (item.get("openAccessPdf") or {}).get("url")
            results.append(
                RawPaperResult(
                    source=self.name,
                    source_id=item.get("paperId", ""),
                    title=item.get("title") or "Untitled",
                    abstract=item.get("abstract"),
                    authors=[a.get("name", "") for a in item.get("authors", [])],
                    published_year=item.get("year"),
                    url=item.get("url"),
                    pdf_url=pdf,
                    citation_count=item.get("citationCount"),
                    venue=item.get("venue"),
                )
            )
        return results
