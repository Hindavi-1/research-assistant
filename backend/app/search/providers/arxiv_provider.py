"""arXiv search provider — free, no API key required."""
import asyncio

import arxiv

from app.core.exceptions import SearchProviderError
from app.core.logging import logger
from app.schemas.paper import RawPaperResult
from app.search.base import BaseSearchProvider


class ArxivProvider(BaseSearchProvider):
    name = "arxiv"

    async def search(self, query: str) -> list[RawPaperResult]:
        try:
            return await asyncio.to_thread(self._search_sync, query)
        except Exception as exc:  # noqa: BLE001
            logger.exception("arXiv search failed")
            raise SearchProviderError(self.name, str(exc)) from exc

    def _search_sync(self, query: str) -> list[RawPaperResult]:
        client = arxiv.Client(page_size=self.max_results, delay_seconds=1.0, num_retries=2)
        search = arxiv.Search(
            query=query,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        results: list[RawPaperResult] = []
        for r in client.results(search):
            results.append(
                RawPaperResult(
                    source=self.name,
                    source_id=r.get_short_id(),
                    title=r.title.strip(),
                    abstract=(r.summary or "").strip().replace("\n", " "),
                    authors=[a.name for a in r.authors],
                    published_year=r.published.year if r.published else None,
                    url=r.entry_id,
                    pdf_url=r.pdf_url,
                    citation_count=None,  # arXiv does not expose citation counts
                    venue=(r.journal_ref or "arXiv preprint"),
                )
            )
        return results
