import uuid

from pydantic import BaseModel


class PaperRead(BaseModel):
    id: uuid.UUID
    source: str
    source_id: str
    title: str
    abstract: str | None
    authors: list[str]
    published_year: int | None
    url: str | None
    pdf_url: str | None
    citation_count: int | None
    venue: str | None
    summary: str | None

    model_config = {"from_attributes": True}


class RawPaperResult(BaseModel):
    """Provider-agnostic shape returned by every SearchProvider implementation.

    Every provider (arXiv, Semantic Scholar, Google Scholar, ...) normalizes
    its raw API/scrape response into this shape, so downstream code (RAG
    ingestion, gap analysis) never needs to know which provider a paper
    came from.
    """

    source: str
    source_id: str
    title: str
    abstract: str | None = None
    authors: list[str] = []
    published_year: int | None = None
    url: str | None = None
    pdf_url: str | None = None
    citation_count: int | None = None
    venue: str | None = None
