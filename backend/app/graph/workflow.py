"""
LangGraph workflow assembly.

This is the vertical slice's full pipeline as a linear StateGraph:

    literature_retrieval -> literature_analysis -> gap_identification
        -> evidence_synthesis -> idea_generation -> title_generation -> END

Future phases (abstract/methodology/sections generation, etc.) attach as
additional nodes appended after `title_generation` — the graph structure is
what makes that an additive change rather than a rewrite.

A checkpointer (in-memory here; swap for a Postgres checkpointer in
production) lets a run be resumed/inspected node-by-node, which matters for
Phase 4's human-in-the-loop review sitting right after this graph completes.
"""
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from app.graph.nodes import (
    evidence_synthesis_node,
    gap_identification_node,
    idea_generation_node,
    literature_analysis_node,
    literature_retrieval_node,
    title_generation_node,
)
from app.graph.state import AgentState


def build_research_discovery_graph():
    """Build (but do not compile with a persistent checkpointer) the pipeline graph."""
    graph = StateGraph(AgentState)

    graph.add_node("literature_retrieval", literature_retrieval_node)
    graph.add_node("literature_analysis", literature_analysis_node)
    graph.add_node("gap_identification", gap_identification_node)
    graph.add_node("evidence_synthesis", evidence_synthesis_node)
    graph.add_node("idea_generation", idea_generation_node)
    graph.add_node("title_generation", title_generation_node)

    graph.set_entry_point("literature_retrieval")
    graph.add_edge("literature_retrieval", "literature_analysis")
    graph.add_edge("literature_analysis", "gap_identification")
    graph.add_edge("gap_identification", "evidence_synthesis")
    graph.add_edge("evidence_synthesis", "idea_generation")
    graph.add_edge("idea_generation", "title_generation")
    graph.add_edge("title_generation", END)

    return graph


_checkpointer = MemorySaver()
_compiled_graph = build_research_discovery_graph().compile(checkpointer=_checkpointer)


def get_compiled_graph():
    """Return the compiled, checkpointed graph — used by services/research_service.py."""
    return _compiled_graph
