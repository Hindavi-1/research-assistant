"""
Search factory — builds and fans out to all configured search providers.

Usage:

    from app.search.factory import search_literature
    papers = await search_literature("graph neural networks for drug discovery")

`SEARCH_PROVIDERS` in settings controls which sources run (default:
arxiv, semantic_scholar). Adding a source = implement BaseSearchProvider +
register it in `_PROVIDER_REGISTRY`.
"""
import asyncio

from app.config import get_settings
from app.core.logging import logger
from app.schemas.paper import RawPaperResult
from app.search.base import BaseSearchProvider
from app.search.providers import ArxivProvider, GoogleScholarProvider, SemanticScholarProvider

_PROVIDER_REGISTRY: dict[str, type[BaseSearchProvider]] = {
    "arxiv": ArxivProvider,
    "semantic_scholar": SemanticScholarProvider,
    "google_scholar": GoogleScholarProvider,
}

_API_KEY_MAP = {
    "semantic_scholar": "SEMANTIC_SCHOLAR_API_KEY",
}


def _build_provider(name: str) -> BaseSearchProvider:
    settings = get_settings()
    provider_cls = _PROVIDER_REGISTRY[name]
    api_key = getattr(settings, _API_KEY_MAP.get(name, ""), None)
    return provider_cls(api_key=api_key, max_results=settings.MAX_PAPERS_PER_SOURCE)


def get_active_providers() -> list[BaseSearchProvider]:
    settings = get_settings()
    providers = []
    for name in settings.SEARCH_PROVIDERS:
        if name not in _PROVIDER_REGISTRY:
            logger.warning(f"Unknown search provider '{name}' in SEARCH_PROVIDERS, skipping.")
            continue
        providers.append(_build_provider(name))
    return providers


def _dedupe(papers: list[RawPaperResult]) -> list[RawPaperResult]:
    """Dedupe across sources by normalized title (arXiv & Semantic Scholar often overlap)."""
    seen: set[str] = set()
    unique: list[RawPaperResult] = []
    for p in papers:
        key = p.title.strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


async def search_literature(query: str) -> list[RawPaperResult]:
    """Fan out the query to every configured, active search provider and merge results."""
    providers = get_active_providers()
    if not providers:
        logger.warning("No search providers configured/active.")
        return []

    results_per_provider = await asyncio.gather(
        *[p.search(query) for p in providers], return_exceptions=True
    )

    merged: list[RawPaperResult] = []
    for provider, result in zip(providers, results_per_provider):
        if isinstance(result, Exception):
            logger.error(f"Provider '{provider.name}' failed: {result}")
            continue
        logger.info(f"Provider '{provider.name}' returned {len(result)} papers.")
        merged.extend(result)

    return _dedupe(merged)
