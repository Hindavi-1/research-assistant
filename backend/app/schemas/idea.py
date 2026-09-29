import uuid

from pydantic import BaseModel, Field

from app.models.idea import ReviewStatus


class ResearchTitleRead(BaseModel):
    id: uuid.UUID
    title_text: str
    style: str
    review_status: ReviewStatus
    is_selected: bool

    model_config = {"from_attributes": True}


class ResearchIdeaRead(BaseModel):
    id: uuid.UUID
    gap_id: uuid.UUID
    summary: str
    proposed_approach: str
    rationale: str
    evidence_citations: list[str]
    novelty_score: float
    feasibility_score: float
    impact_score: float
    review_status: ReviewStatus
    reviewer_notes: str | None
    titles: list[ResearchTitleRead] = []

    model_config = {"from_attributes": True}


class IdeaLLMOutput(BaseModel):
    """Shape the LLM is prompted to return for one idea grounded in a gap."""

    summary: str = Field(..., description="1-2 sentence summary of the research idea.")
    proposed_approach: str = Field(..., description="A short paragraph on how one would approach it.")
    rationale: str = Field(
        ..., description="Why this idea is worth pursuing — the explicit justification the user asked for."
    )
    evidence_paper_indices: list[int] = Field(
        ..., description="Indices (0-based, into the provided paper list) backing the rationale."
    )
    novelty_score: float = Field(..., ge=0, le=1)
    feasibility_score: float = Field(..., ge=0, le=1)
    impact_score: float = Field(..., ge=0, le=1)


class TitleLLMOutput(BaseModel):
    title_text: str
    style: str = Field(..., description="One of: descriptive, catchy, technical")


class HumanReviewRequest(BaseModel):
    """Phase 4 input: human decisions on ideas/titles."""

    idea_id: uuid.UUID
    status: ReviewStatus
    reviewer_notes: str | None = None
    selected_title_id: uuid.UUID | None = None
