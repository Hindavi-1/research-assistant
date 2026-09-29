"""
Phase 1 node: Research discovery & paper retrieval.

Fans out to all configured search providers (via `app.search.factory`),
normalizes and deduplicates results, persists them as `Paper` rows, and
kicks off RAG ingestion (chunk + embed) so later nodes can retrieve
grounded context instead of relying on the LLM's memory.
"""
from uuid import UUID

from app.core.database import db_session_ctx
from app.core.exceptions import NoLiteratureFoundError
from app.core.logging import logger
from app.graph.state import AgentState
from app.models.paper import Paper
from app.rag.vector_store import ingest_paper_chunks
from app.search.factory import search_literature


async def literature_retrieval_node(state: AgentState) -> dict:
    query = state["query"]
    domain = state.get("domain")
    search_query = f"{query} {domain}".strip() if domain else query

    logger.info(f"[literature_retrieval] searching for: {search_query!r}")
    raw_papers = await search_literature(search_query)

    if not raw_papers:
        raise NoLiteratureFoundError(search_query)

    session_id = UUID(state["session_id"])
    paper_ids: list[str] = []
    raw_paper_dicts: list[dict] = []

    async with db_session_ctx() as db:
        for rp in raw_papers:
            paper = Paper(
                session_id=session_id,
                source=rp.source,
                source_id=rp.source_id,
                title=rp.title,
                abstract=rp.abstract,
                authors=rp.authors,
                published_year=rp.published_year,
                url=rp.url,
                pdf_url=rp.pdf_url,
                citation_count=rp.citation_count,
                venue=rp.venue,
            )
            db.add(paper)
            await db.flush()  # get paper.id

            await ingest_paper_chunks(db, paper)  # RAG: chunk + embed immediately

            paper_ids.append(str(paper.id))
            raw_paper_dicts.append({**rp.model_dump(), "id": str(paper.id)})

    logger.info(f"[literature_retrieval] persisted {len(paper_ids)} papers (RAG-ingested).")

    return {
        "raw_papers": raw_paper_dicts,
        "paper_ids": paper_ids,
        "stage": "retrieving_literature",
    }
