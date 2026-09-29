"""
LangGraph state definition.

This is the single object threaded through every node of the pipeline.
Each node reads what it needs and returns a partial dict of updates
(standard LangGraph pattern) — nothing mutates state directly except via
the return value, which keeps nodes independently testable.

Note: heavy objects (Paper rows, etc.) are NOT stored in-graph as ORM
instances; we pass lightweight dicts/ids and let each node hit Postgres via
`session_id`. This keeps the graph state serializable (needed for LangGraph
checkpointing) and keeps Postgres as the single source of truth.
"""
import operator
from typing import Annotated, Any, TypedDict
from uuid import UUID


class AgentState(TypedDict, total=False):
    # ---- input ----
    session_id: str
    query: str
    domain: str | None

    # ---- Phase 1: literature retrieval ----
    raw_papers: list[dict[str, Any]]          # RawPaperResult dicts, as returned by search providers
    paper_ids: list[str]                       # Paper.id (as str) once persisted

    # ---- Phase 2: literature analysis + gap identification ----
    paper_summaries: dict[str, str]            # paper_id -> LLM summary
    gaps: list[dict[str, Any]]                  # GapLLMOutput-like dicts, enriched with paper ids
    gap_ids: list[str]

    # ---- Phase 3: idea + title generation ----
    ideas: list[dict[str, Any]]                 # one entry per gap, IdeaLLMOutput-like + gap_id
    idea_ids: list[str]
    titles: dict[str, list[dict[str, Any]]]     # idea_id -> list of TitleLLMOutput-like dicts

    # ---- pipeline bookkeeping ----
    stage: str
    errors: Annotated[list[str], operator.add]  # accumulates; multiple nodes may append


def new_state(session_id: UUID, query: str, domain: str | None) -> AgentState:
    return AgentState(
        session_id=str(session_id),
        query=query,
        domain=domain,
        raw_papers=[],
        paper_ids=[],
        paper_summaries={},
        gaps=[],
        gap_ids=[],
        ideas=[],
        idea_ids=[],
        titles={},
        stage="created",
        errors=[],
    )
