"""
Phase 2 node (part 1): Literature intelligence.

Generates a short structured summary for each retrieved paper (problem,
method, finding, limitation) using the configured LLM. These summaries are
what the gap-identification node reasons over, so they're persisted back
onto the `Paper` row rather than only kept in graph state.
"""
import asyncio
from uuid import UUID

from sqlalchemy import select

from app.core.database import db_session_ctx
from app.core.logging import logger
from app.graph.state import AgentState
from app.llm.factory import get_llm
from app.models.paper import Paper
from app.utils.prompts import PAPER_SUMMARY_PROMPT

_MAX_CONCURRENT_SUMMARIES = 5


async def _summarize_one(llm, paper: Paper) -> tuple[str, str]:
    prompt = PAPER_SUMMARY_PROMPT.format(
        title=paper.title,
        authors=", ".join(paper.authors[:5]) or "Unknown",
        year=paper.published_year or "n.d.",
        abstract=paper.abstract or "No abstract available.",
    )
    response = await llm.ainvoke(prompt)
    return str(paper.id), response.content.strip()


async def literature_analysis_node(state: AgentState) -> dict:
    session_id = UUID(state["session_id"])
    llm = get_llm()  # uses configured provider (Groq by default)

    async with db_session_ctx() as db:
        result = await db.execute(select(Paper).where(Paper.session_id == session_id))
        papers = list(result.scalars().all())

        semaphore = asyncio.Semaphore(_MAX_CONCURRENT_SUMMARIES)

        async def bounded(p: Paper):
            async with semaphore:
                return await _summarize_one(llm, p)

        logger.info(f"[literature_analysis] summarizing {len(papers)} papers...")
        summaries = await asyncio.gather(*[bounded(p) for p in papers], return_exceptions=True)

        paper_summaries: dict[str, str] = {}
        for p, res in zip(papers, summaries):
            if isinstance(res, Exception):
                logger.error(f"Summary failed for paper {p.id}: {res}")
                continue
            paper_id, summary_text = res
            p.summary = summary_text
            paper_summaries[paper_id] = summary_text

    logger.info(f"[literature_analysis] summarized {len(paper_summaries)}/{len(papers)} papers.")

    return {
        "paper_summaries": paper_summaries,
        "stage": "analyzing_literature",
    }
