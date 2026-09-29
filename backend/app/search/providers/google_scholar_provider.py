"""
Google Scholar provider.

NOTE: Google Scholar has no official public API, and scraping it directly
violates its Terms of Service and is aggressively rate-limited/blocked. This
provider is implemented behind the same `BaseSearchProvider` interface so it
can be dropped in later via a compliant third-party API (e.g. SerpAPI,
ScraperAPI's Scholar endpoint) purely by filling in `_fetch()` — no other
code changes required. It is NOT enabled by default (`SEARCH_PROVIDERS` in
.env.example excludes it) until a compliant backend is configured.
"""
from app.core.exceptions import SearchProviderError
from app.core.logging import logger
from app.schemas.paper import RawPaperResult
from app.search.base import BaseSearchProvider


class GoogleScholarProvider(BaseSearchProvider):
    name = "google_scholar"

    async def search(self, query: str) -> list[RawPaperResult]:
        if not self.api_key:
            logger.warning(
                "GoogleScholarProvider is disabled: no compliant API key configured "
                "(e.g. SERPAPI_KEY). Skipping this source."
            )
            return []
        try:
            return await self._fetch(query)
        except Exception as exc:  # noqa: BLE001
            raise SearchProviderError(self.name, str(exc)) from exc

    async def _fetch(self, query: str) -> list[RawPaperResult]:
        """Plug a compliant Scholar API (e.g. SerpAPI) in here.

        Left unimplemented intentionally — see module docstring.
        """
        raise NotImplementedError(
            "Wire up a compliant Google Scholar API provider (e.g. SerpAPI) here."
        )
