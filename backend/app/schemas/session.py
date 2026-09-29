import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.session import PipelineStage


class ResearchSessionCreate(BaseModel):
    """User input that kicks off the pipeline — keywords or free-text description."""

    query: str = Field(..., min_length=3, max_length=2000, description="Keywords or a description of the research interest.")
    domain: str | None = Field(None, description="Optional field/domain hint, e.g. 'NLP', 'Computer Vision'.")


class ResearchSessionRead(BaseModel):
    id: uuid.UUID
    query: str
    domain: str | None
    stage: PipelineStage
    error_message: str | None
    llm_provider: str
    llm_model: str
    search_providers: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResearchSessionStatus(BaseModel):
    """Lightweight polling payload for the frontend's progress UI."""

    id: uuid.UUID
    stage: PipelineStage
    error_message: str | None = None

    model_config = {"from_attributes": True}
