"""
High-level RAG retriever used by LangGraph nodes.

Wraps `vector_store.similarity_search` and joins back to `Paper` rows so
callers get fully-formed context (paper metadata + matched excerpt) rather
than raw chunk rows — this is what grounds gap analysis and idea generation
in actual retrieved literature instead of the LLM's parametric memory.
"""
import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.paper import Paper
from app.rag.vector_store import similarity_search


@dataclass
class RetrievedContext:
    paper: Paper
    matched_excerpt: str
    relevance_score: float  # 1 - cosine_distance, higher is better


async def retrieve_relevant_context(
    db: AsyncSession, session_id: uuid.UUID, query: str, top_k: int = 8
) -> list[RetrievedContext]:
    chunk_results = await similarity_search(db, session_id, query, top_k=top_k)

    contexts: list[RetrievedContext] = []
    for chunk, distance in chunk_results:
        # chunk.paper is eagerly loaded via selectinload in similarity_search.
        contexts.append(
            RetrievedContext(
                paper=chunk.paper,
                matched_excerpt=chunk.content,
                relevance_score=round(1 - distance, 4),
            )
        )
    return contexts


def format_context_for_prompt(contexts: list[RetrievedContext]) -> str:
    """Render retrieved context as a numbered list the LLM can cite back by index."""
    lines = []
    for i, ctx in enumerate(contexts):
        p = ctx.paper
        lines.append(
            f"[{i}] {p.title} ({p.published_year or 'n.d.'}) — {', '.join(p.authors[:3]) or 'Unknown authors'}\n"
            f"    Excerpt: {ctx.matched_excerpt[:500]}"
        )
    return "\n".join(lines)
