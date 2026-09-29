"""Read-side service: assembling the full result payload for a session."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.gap import ResearchGap
from app.models.idea import ResearchIdea
from app.models.paper import Paper


async def get_papers(db: AsyncSession, session_id: uuid.UUID) -> list[Paper]:
    result = await db.execute(
        select(Paper).where(Paper.session_id == session_id).order_by(Paper.citation_count.desc().nullslast())
    )
    return list(result.scalars().all())


async def get_gaps(db: AsyncSession, session_id: uuid.UUID) -> list[ResearchGap]:
    result = await db.execute(
        select(ResearchGap)
        .where(ResearchGap.session_id == session_id)
        .order_by(ResearchGap.confidence_score.desc())
    )
    return list(result.scalars().all())


async def get_ideas(db: AsyncSession, session_id: uuid.UUID) -> list[ResearchIdea]:
    result = await db.execute(
        select(ResearchIdea)
        .where(ResearchIdea.session_id == session_id)
        .options(selectinload(ResearchIdea.titles))
        .order_by(ResearchIdea.impact_score.desc())
    )
    return list(result.scalars().all())
