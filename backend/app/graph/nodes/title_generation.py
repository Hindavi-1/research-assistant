"""
Phase 3 node (part 2): Title generation.

For each generated idea, produces multiple candidate titles in distinct
styles (descriptive / catchy / technical) so the human reviewer (Phase 4)
has real options rather than a single take-it-or-leave-it title.
"""
import asyncio

from app.core.database import db_session_ctx
from app.core.logging import logger
from app.graph.state import AgentState
from app.llm.factory import get_llm
from app.models.idea import ResearchTitle
from app.utils.json_parsing import extract_json_array
from app.utils.prompts import TITLE_GENERATION_SYSTEM_PROMPT, TITLE_GENERATION_USER_PROMPT

NUM_TITLES_PER_IDEA = 3
_VALID_STYLES = {"descriptive", "catchy", "technical"}


async def _generate_titles_for_idea(llm, idea: dict) -> list[dict]:
    system_prompt = TITLE_GENERATION_SYSTEM_PROMPT.format(num_titles=NUM_TITLES_PER_IDEA)
    user_prompt = TITLE_GENERATION_USER_PROMPT.format(
        idea_summary=idea["summary"], idea_approach=idea["proposed_approach"]
    )
    response = await llm.ainvoke([("system", system_prompt), ("user", user_prompt)])
    return extract_json_array(response.content)


async def title_generation_node(state: AgentState) -> dict:
    llm = get_llm()
    ideas = state.get("ideas", [])

    if not ideas:
        logger.warning("[title_generation] no ideas available; skipping.")
        return {"titles": {}, "stage": "generating_titles"}

    titles_by_idea: dict[str, list[dict]] = {}

    async with db_session_ctx() as db:
        for idea in ideas:
            try:
                raw_titles = await _generate_titles_for_idea(llm, idea)
            except Exception as exc:  # noqa: BLE001
                logger.error(f"Title generation failed for idea {idea['id']}: {exc}")
                continue

            idea_titles: list[dict] = []
            for item in raw_titles:
                title_text = item.get("title_text", "").strip()
                style = str(item.get("style", "descriptive")).lower()
                style = style if style in _VALID_STYLES else "descriptive"
                if not title_text:
                    continue

                title_row = ResearchTitle(idea_id=idea["id"], title_text=title_text, style=style)
                db.add(title_row)
                await db.flush()

                idea_titles.append({"id": str(title_row.id), "title_text": title_text, "style": style})

            titles_by_idea[idea["id"]] = idea_titles

    total = sum(len(v) for v in titles_by_idea.values())
    logger.info(f"[title_generation] generated {total} titles across {len(ideas)} ideas.")

    return {
        "titles": titles_by_idea,
        "stage": "generating_titles",
    }
