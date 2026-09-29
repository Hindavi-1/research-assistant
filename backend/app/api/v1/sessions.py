"""
Session endpoints: create a research session (kicks off the pipeline as a
background task), poll its status, and fetch results once ready.
"""
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.gap import ResearchGapRead
from app.schemas.idea import ResearchIdeaRead
from app.schemas.paper import PaperRead
from app.schemas.session import ResearchSessionCreate, ResearchSessionRead, ResearchSessionStatus
from app.services import paper_service, research_service, session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=ResearchSessionRead, status_code=201)
async def create_research_session(
    payload: ResearchSessionCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Create a session from user input (keywords/description) and start the pipeline asynchronously."""
    session = await session_service.create_session(db, payload)
    # Commit now so the row is visible to the background task's own DB session.
    # (Starlette runs background tasks *before* dependency cleanup, so the
    # get_db commit would otherwise happen too late.)
    await db.commit()
    background_tasks.add_task(research_service.run_pipeline, session.id, session.query, session.domain)
    return session


@router.get("", response_model=list[ResearchSessionRead])
async def list_research_sessions(db: AsyncSession = Depends(get_db)):
    return await session_service.list_sessions(db)


@router.get("/{session_id}", response_model=ResearchSessionRead)
async def get_research_session(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await session_service.get_session(db, session_id)


@router.get("/{session_id}/status", response_model=ResearchSessionStatus)
async def get_research_session_status(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Lightweight polling endpoint for the frontend's pipeline-progress UI."""
    return await session_service.get_session(db, session_id)


@router.get("/{session_id}/papers", response_model=list[PaperRead])
async def get_session_papers(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await paper_service.get_papers(db, session_id)


@router.get("/{session_id}/gaps", response_model=list[ResearchGapRead])
async def get_session_gaps(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await paper_service.get_gaps(db, session_id)


@router.get("/{session_id}/ideas", response_model=list[ResearchIdeaRead])
async def get_session_ideas(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await paper_service.get_ideas(db, session_id)
