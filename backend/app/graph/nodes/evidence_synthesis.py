"""
Phase 2 node (part 3): Evidence synthesis.

This is where the RAG retrieval loop actually closes: for each identified
gap, we run a targeted similarity search (gap title + description as the
query) against the session's embedded paper chunks, and attach the
best-matching excerpts as grounding evidence. This gives the idea-generation
node concrete text to point to, rather than only the LLM's own paraphrase
from the gap-identification step.
"""
from uuid import UUID

from sqlalchemy import select

from app.config import get_settings
from app.core.database import db_session_ctx
from app.core.logging import logger
from app.graph.state import AgentState
from app.models.gap import ResearchGap
from app.rag.retriever import format_context_for_prompt, retrieve_relevant_context

settings = get_settings()


async def evidence_synthesis_node(state: AgentState) -> dict:
    session_id = UUID(state["session_id"])
    gaps_state = state.get("gaps", [])

    if not gaps_state:
        logger.warning("[evidence_synthesis] no gaps to synthesize evidence for; skipping.")
        return {"stage": "synthesizing_evidence"}

    enriched_gaps: list[dict] = []

    async with db_session_ctx() as db:
        result = await db.execute(select(ResearchGap).where(ResearchGap.session_id == session_id))
        gap_rows = {str(g.id): g for g in result.scalars().all()}

        for gap_dict in gaps_state:
            gap_query = f"{gap_dict['title']}. {gap_dict['description']}"
            contexts = await retrieve_relevant_context(
                db, session_id, gap_query, top_k=settings.TOP_K_RETRIEVAL
            )
            retrieved_block = format_context_for_prompt(contexts)

            gap_row = gap_rows.get(gap_dict["id"])
            if gap_row is not None and retrieved_block:
                # Append retrieved grounding excerpts to the persisted evidence summary.
                gap_row.evidence_summary = (
                    f"{gap_row.evidence_summary}\n\nRetrieved grounding evidence:\n{retrieved_block}"
                )

            enriched_gaps.append(
                {
                    **gap_dict,
                    "retrieved_evidence_block": retrieved_block,
                }
            )

    logger.info(f"[evidence_synthesis] enriched {len(enriched_gaps)} gaps with retrieved evidence.")

    return {
        "gaps": enriched_gaps,
        "stage": "synthesizing_evidence",
    }
