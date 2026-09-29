"""
Phase 2 node (part 2): Research-gap identification.

Prompts the LLM to identify N distinct gaps in the retrieved (and now
summarized) literature, grounded via explicit paper indices. This is where
the RAG loop closes: instead of dumping every paper's full text into the
prompt, we could retrieve only the most relevant chunks for a candidate
sub-topic — for this vertical slice we pass all retrieved paper summaries
(bounded by MAX_PAPERS_PER_SOURCE * num providers, kept small deliberately)
since gap-finding benefits from seeing the whole retrieved set at once.
"""
from uuid import UUID

from sqlalchemy import select

from app.config import get_settings
from app.core.database import db_session_ctx
from app.core.logging import logger
from app.graph.state import AgentState
from app.llm.factory import get_llm
from app.models.gap import GapType, ResearchGap
from app.models.paper import Paper
from app.utils.json_parsing import extract_json_array
from app.utils.prompts import GAP_IDENTIFICATION_SYSTEM_PROMPT, GAP_IDENTIFICATION_USER_PROMPT

DEFAULT_NUM_GAPS = 5


def _format_papers_block(papers: list[Paper]) -> str:
    lines = []
    for i, p in enumerate(papers):
        summary = p.summary or (p.abstract or "")[:400]
        lines.append(f"[{i}] \"{p.title}\" ({p.published_year or 'n.d.'}) — {summary}")
    return "\n".join(lines)


async def gap_identification_node(state: AgentState) -> dict:
    settings = get_settings()
    session_id = UUID(state["session_id"])
    llm = get_llm()

    async with db_session_ctx() as db:
        result = await db.execute(select(Paper).where(Paper.session_id == session_id))
        papers = list(result.scalars().all())

        if not papers:
            logger.warning("[gap_identification] no papers available; skipping.")
            return {"gaps": [], "gap_ids": [], "stage": "identifying_gaps"}

        system_prompt = GAP_IDENTIFICATION_SYSTEM_PROMPT.format(num_gaps=DEFAULT_NUM_GAPS)
        user_prompt = GAP_IDENTIFICATION_USER_PROMPT.format(
            query=state["query"],
            domain=state.get("domain") or "not specified",
            papers_block=_format_papers_block(papers),
        )

        logger.info(f"[gap_identification] reasoning over {len(papers)} papers...")
        response = await llm.ainvoke([("system", system_prompt), ("user", user_prompt)])
        parsed = extract_json_array(response.content)

        gaps: list[dict] = []
        gap_ids: list[str] = []

        for item in parsed:
            try:
                indices = item.get("supporting_paper_indices", [])
                supporting_ids = [str(papers[i].id) for i in indices if 0 <= i < len(papers)]
                gap_type_raw = str(item.get("gap_type", "empirical")).lower()
                gap_type = gap_type_raw if gap_type_raw in GapType._value2member_map_ else "empirical"

                gap = ResearchGap(
                    session_id=session_id,
                    title=item["title"],
                    description=item["description"],
                    gap_type=GapType(gap_type),
                    supporting_paper_ids=supporting_ids,
                    evidence_summary=item.get("evidence_summary", ""),
                    confidence_score=float(item.get("confidence_score", 0.5)),
                )
                db.add(gap)
                await db.flush()

                gap_ids.append(str(gap.id))
                gaps.append(
                    {
                        "id": str(gap.id),
                        "title": gap.title,
                        "description": gap.description,
                        "gap_type": gap.gap_type.value,
                        "supporting_paper_ids": supporting_ids,
                        "evidence_summary": gap.evidence_summary,
                        "confidence_score": gap.confidence_score,
                    }
                )
            except (KeyError, ValueError, IndexError) as exc:
                logger.error(f"Skipping malformed gap item: {exc} — {item}")

    logger.info(f"[gap_identification] identified {len(gaps)} gaps.")

    return {
        "gaps": gaps,
        "gap_ids": gap_ids,
        "stage": "identifying_gaps",
    }
