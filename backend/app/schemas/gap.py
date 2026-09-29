import uuid

from pydantic import BaseModel, Field

from app.models.gap import GapType


class ResearchGapRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    gap_type: GapType
    supporting_paper_ids: list[str]
    evidence_summary: str
    confidence_score: float

    model_config = {"from_attributes": True}


class GapLLMOutput(BaseModel):
    """Shape the LLM is prompted to return for one gap (parsed from structured JSON output)."""

    title: str = Field(..., description="Short, specific name for the gap.")
    description: str = Field(..., description="1-3 sentences describing the gap precisely.")
    gap_type: GapType
    supporting_paper_indices: list[int] = Field(
        ..., description="Indices (0-based, into the provided paper list) of papers that evidence this gap."
    )
    evidence_summary: str = Field(
        ..., description="Explanation of *why* this is a gap, referencing what the supporting papers do/don't cover."
    )
    confidence_score: float = Field(..., ge=0, le=1)
