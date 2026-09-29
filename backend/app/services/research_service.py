"""
Research orchestration service.

`run_pipeline` is the glue between the FastAPI layer and the LangGraph
workflow: it builds initial state, invokes the compiled graph, and maps the
resulting stage/errors back onto the persisted `ResearchSession` row so the
frontend can poll session status independently of the (potentially long-
running) graph invocation.
"""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import db_session_ctx
from app.core.exceptions import InvalidPipelineStateError, ResearchAssistantError
from app.core.logging import logger
from app.graph.state import new_state
from app.graph.workflow import get_compiled_graph
from app.models.idea import ResearchIdea, ResearchTitle, ReviewStatus
from app.models.session import PipelineStage
from app.schemas.idea import HumanReviewRequest
from app.services import session_service


async def run_pipeline(session_id: uuid.UUID, query: str, domain: str | None) -> None:
    """Run the full Phase 1-3 pipeline for a session. Intended to run as a background task."""
    graph = get_compiled_graph()
    config = {"configurable": {"thread_id": str(session_id)}}

    async with db_session_ctx() as db:
        await session_service.update_stage(db, session_id, PipelineStage.RETRIEVING_LITERATURE)

    try:
        initial_state = new_state(session_id, query, domain)
        final_state = await graph.ainvoke(initial_state, config=config)

        async with db_session_ctx() as db:
            await session_service.update_stage(db, session_id, PipelineStage.AWAITING_HUMAN_REVIEW)

        logger.info(
            f"[run_pipeline] session={session_id} completed: "
            f"{len(final_state.get('paper_ids', []))} papers, "
            f"{len(final_state.get('gap_ids', []))} gaps, "
            f"{len(final_state.get('idea_ids', []))} ideas."
        )

    except ResearchAssistantError as exc:
        logger.error(f"[run_pipeline] session={session_id} failed: {exc.message}")
        async with db_session_ctx() as db:
            await session_service.update_stage(db, session_id, PipelineStage.FAILED, error_message=exc.message)

    except Exception as exc:  # noqa: BLE001
        logger.exception(f"[run_pipeline] session={session_id} failed unexpectedly")
        async with db_session_ctx() as db:
            await session_service.update_stage(db, session_id, PipelineStage.FAILED, error_message=str(exc))


async def submit_human_review(db: AsyncSession, review: HumanReviewRequest) -> ResearchIdea:
    """Phase 4: persist a human decision (approve/reject/edit) on an idea, optionally selecting a title."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    result = await db.execute(
        select(ResearchIdea)
        .where(ResearchIdea.id == review.idea_id)
        .options(selectinload(ResearchIdea.titles))
    )
    idea = result.scalar_one_or_none()
    if idea is None:
        raise InvalidPipelineStateError(f"Idea {review.idea_id} not found.")

    idea.review_status = review.status
    idea.reviewer_notes = review.reviewer_notes

    if review.selected_title_id is not None:
        for title in idea.titles:
            title.is_selected = title.id == review.selected_title_id
            if title.is_selected:
                title.review_status = ReviewStatus.APPROVED

    await db.flush()
    await db.refresh(idea)
    return idea
