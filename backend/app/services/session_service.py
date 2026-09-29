"""Session lifecycle: create, fetch, update pipeline stage."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.exceptions import SessionNotFoundError
from app.models.session import PipelineStage, ResearchSession
from app.schemas.session import ResearchSessionCreate

settings = get_settings()


async def create_session(db: AsyncSession, payload: ResearchSessionCreate) -> ResearchSession:
    session = ResearchSession(
        query=payload.query,
        domain=payload.domain,
        stage=PipelineStage.CREATED,
        llm_provider=settings.LLM_PROVIDER,
        llm_model=settings.LLM_MODEL,
        search_providers=",".join(settings.SEARCH_PROVIDERS),
    )
    db.add(session)
    await db.flush()
    await db.refresh(session)
    return session


async def get_session(db: AsyncSession, session_id: uuid.UUID) -> ResearchSession:
    session = await db.get(ResearchSession, session_id)
    if session is None:
        raise SessionNotFoundError(str(session_id))
    return session


async def list_sessions(db: AsyncSession, limit: int = 50) -> list[ResearchSession]:
    result = await db.execute(
        select(ResearchSession).order_by(ResearchSession.created_at.desc()).limit(limit)
    )
    return list(result.scalars().all())


async def update_stage(
    db: AsyncSession, session_id: uuid.UUID, stage: PipelineStage, error_message: str | None = None
) -> ResearchSession:
    session = await get_session(db, session_id)
    session.stage = stage
    session.error_message = error_message
    await db.flush()
    await db.refresh(session)
    return session
