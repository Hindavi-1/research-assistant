"""
Lightweight unit tests that don't require a live DB/LLM/network — they check
the graph structure and pure utility functions. Integration tests that hit
Postgres and a real LLM should live in a separate `tests/integration/`
module (not included in this vertical slice) gated behind env vars.
"""
from app.graph.workflow import build_research_discovery_graph
from app.rag.chunking import chunk_text
from app.utils.json_parsing import extract_json_array


def test_graph_has_expected_nodes():
    graph = build_research_discovery_graph()
    compiled = graph.compile()
    node_names = set(compiled.get_graph().nodes.keys())

    expected = {
        "literature_retrieval",
        "literature_analysis",
        "gap_identification",
        "evidence_synthesis",
        "idea_generation",
        "title_generation",
    }
    assert expected.issubset(node_names)


def test_chunk_text_short_text_returns_single_chunk():
    chunks = chunk_text("This is a short abstract about graph neural networks.")
    assert len(chunks) == 1


def test_chunk_text_long_text_splits_with_overlap():
    long_text = "word " * 2000
    chunks = chunk_text(long_text, chunk_size=200, overlap=20)
    assert len(chunks) > 1


def test_extract_json_array_handles_markdown_fences():
    raw = '```json\n[{"a": 1}, {"a": 2}]\n```'
    parsed = extract_json_array(raw)
    assert parsed == [{"a": 1}, {"a": 2}]


def test_extract_json_array_handles_plain_json():
    raw = '[{"title": "Gap A"}]'
    parsed = extract_json_array(raw)
    assert parsed[0]["title"] == "Gap A"


def test_extract_json_array_returns_empty_on_garbage():
    assert extract_json_array("not json at all") == []
