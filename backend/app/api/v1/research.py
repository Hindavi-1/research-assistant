"""
Phase 4 endpoints: human review of generated ideas/titles.

Kept as its own router (`/research/...`) since these actions operate on
ideas/titles directly rather than being scoped under a session path, which
keeps the frontend's review UI simple (it already has idea/title ids from
the `/sessions/{id}/ideas` payload).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.idea import HumanReviewRequest, ResearchIdeaRead
from app.services import research_service

router = APIRouter(prefix="/research", tags=["research"])


@router.post("/review", response_model=ResearchIdeaRead)
async def submit_review(payload: HumanReviewRequest, db: AsyncSession = Depends(get_db)):
    """Approve, reject, or edit-and-approve a generated idea, optionally selecting one of its titles."""
    return await research_service.submit_human_review(db, payload)
