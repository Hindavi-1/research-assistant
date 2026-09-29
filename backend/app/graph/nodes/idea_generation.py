"""
Phase 3 node (part 1): Research idea generation.

For each identified (and evidence-enriched) gap, prompts the LLM to propose
concrete research idea(s), each with an explicit, evidence-backed rationale
— the "why should we work on this" justification the project requires.
"""
import asyncio
from uuid import UUID

from sqlalchemy import select

from app.core.database import db_session_ctx
from app.core.logging import logger
from app.graph.state import AgentState
from app.llm.factory import get_llm
from app.models.idea import ResearchIdea
from app.models.paper import Paper
from app.utils.json_parsing import extract_json_array
from app.utils.prompts import IDEA_GENERATION_SYSTEM_PROMPT, IDEA_GENERATION_USER_PROMPT

IDEAS_PER_GAP = 2


def _format_supporting_papers(papers: list[Paper]) -> str:
    lines = []
    for i, p in enumerate(papers):
        summary = p.summary or (p.abstract or "")[:400]
        lines.append(f"[{i}] \"{p.title}\" ({p.published_year or 'n.d.'}) — {summary}")
    return "\n".join(lines)


async def _generate_for_gap(llm, gap_dict: dict, supporting_papers: list[Paper]) -> list[dict]:
    system_prompt = IDEA_GENERATION_SYSTEM_PROMPT.format(num_ideas=IDEAS_PER_GAP)
    user_prompt = IDEA_GENERATION_USER_PROMPT.format(
        gap_title=gap_dict["title"],
        gap_description=gap_dict["description"],
        gap_evidence=gap_dict["evidence_summary"],
        papers_block=_format_supporting_papers(supporting_papers),
    )
    response = await llm.ainvoke([("system", system_prompt), ("user", user_prompt)])
    return extract_json_array(response.content)


async def idea_generation_node(state: AgentState) -> dict:
    session_id = UUID(state["session_id"])
    llm = get_llm()
    gaps_state = state.get("gaps", [])

    if not gaps_state:
        logger.warning("[idea_generation] no gaps available; skipping.")
        return {"ideas": [], "idea_ids": [], "stage": "generating_ideas"}

    ideas_out: list[dict] = []
    idea_ids: list[str] = []

    async with db_session_ctx() as db:
        # Preload all papers for this session once, index by id for quick lookup.
        result = await db.execute(select(Paper).where(Paper.session_id == session_id))
        all_papers = {str(p.id): p for p in result.scalars().all()}

        for gap_dict in gaps_state:
            supporting_ids = gap_dict.get("supporting_paper_ids", [])
            supporting_papers = [all_papers[pid] for pid in supporting_ids if pid in all_papers]
            if not supporting_papers:
                supporting_papers = list(all_papers.values())[:5]  # fallback: some context is better than none

            try:
                raw_ideas = await _generate_for_gap(llm, gap_dict, supporting_papers)
            except Exception as exc:  # noqa: BLE001
                logger.error(f"Idea generation failed for gap {gap_dict['id']}: {exc}")
                continue

            for item in raw_ideas:
                try:
                    indices = item.get("evidence_paper_indices", [])
                    evidence_ids = [
                        str(supporting_papers[i].id) for i in indices if 0 <= i < len(supporting_papers)
                    ] or supporting_ids

                    idea = ResearchIdea(
                        session_id=session_id,
                        gap_id=UUID(gap_dict["id"]),
                        summary=item["summary"],
                        proposed_approach=item["proposed_approach"],
                        rationale=item["rationale"],
                        evidence_citations=evidence_ids,
                        novelty_score=float(item.get("novelty_score", 0.5)),
                        feasibility_score=float(item.get("feasibility_score", 0.5)),
                        impact_score=float(item.get("impact_score", 0.5)),
                    )
                    db.add(idea)
                    await db.flush()

                    idea_ids.append(str(idea.id))
                    ideas_out.append(
                        {
                            "id": str(idea.id),
                            "gap_id": gap_dict["id"],
                            "summary": idea.summary,
                            "proposed_approach": idea.proposed_approach,
                            "rationale": idea.rationale,
                            "evidence_citations": evidence_ids,
                            "novelty_score": idea.novelty_score,
                            "feasibility_score": idea.feasibility_score,
                            "impact_score": idea.impact_score,
                        }
                    )
                except (KeyError, ValueError, IndexError) as exc:
                    logger.error(f"Skipping malformed idea item: {exc} — {item}")

    logger.info(f"[idea_generation] generated {len(ideas_out)} ideas across {len(gaps_state)} gaps.")

    return {
        "ideas": ideas_out,
        "idea_ids": idea_ids,
        "stage": "generating_ideas",
    }
