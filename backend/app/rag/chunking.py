"""
Text chunking for RAG ingestion.

Retrieved papers typically only give us title + abstract (full text is
rarely open-access), so chunks are usually small — but the same chunker is
used if/when full-text PDFs are ingested in a future phase, so it's written
generically with token-aware splitting via tiktoken.
"""
import tiktoken

from app.config import get_settings

settings = get_settings()
_encoding = tiktoken.get_encoding("cl100k_base")


def chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> list[str]:
    """Split text into overlapping, token-bounded chunks."""
    if not text or not text.strip():
        return []

    chunk_size = chunk_size or settings.CHUNK_SIZE
    overlap = overlap or settings.CHUNK_OVERLAP

    tokens = _encoding.encode(text)
    if len(tokens) <= chunk_size:
        return [text.strip()]

    chunks: list[str] = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunks.append(_encoding.decode(chunk_tokens).strip())
        if end == len(tokens):
            break
        start = end - overlap  # slide window back by overlap

    return [c for c in chunks if c]


def build_paper_document(title: str, abstract: str | None, authors: list[str], year: int | None) -> str:
    """Build the canonical text representation of a paper used for embedding/chunking."""
    author_str = ", ".join(authors[:5]) + (" et al." if len(authors) > 5 else "")
    year_str = f" ({year})" if year else ""
    abstract_str = abstract or "No abstract available."
    return f"Title: {title}{year_str}\nAuthors: {author_str}\nAbstract: {abstract_str}"
