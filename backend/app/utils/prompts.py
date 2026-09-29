"""Centralized prompt templates for every LLM-driven graph node."""

PAPER_SUMMARY_PROMPT = """You are a meticulous research assistant. Summarize the following paper in \
3-4 sentences for a literature review. Focus on: (1) what problem it addresses, (2) its core method/\
contribution, (3) its key finding, and (4) any explicitly stated limitation.

Title: {title}
Authors: {authors}
Year: {year}
Abstract: {abstract}

Return ONLY the summary text, no preamble.
"""

GAP_IDENTIFICATION_SYSTEM_PROMPT = """You are a senior research scientist performing a systematic \
literature review to identify UNADDRESSED research gaps. You will be given a research query/topic and \
a numbered list of papers (with summaries) retrieved for that topic.

Your job: identify {num_gaps} distinct, SPECIFIC research gaps — things the retrieved literature does \
NOT adequately address, based ONLY on the evidence in the provided papers. For each gap:
- Ground it explicitly in the papers (cite them by index).
- Classify its type: methodological, empirical, theoretical, application, or contradiction.
- Explain concretely WHY it's a gap — what's missing, limited, or conflicting in the cited papers.
- Do not invent gaps unsupported by the provided papers; do not hallucinate paper content.
- Give a confidence_score (0-1) reflecting how strongly the evidence supports this being a real gap.

Respond ONLY with a JSON array of objects, each with EXACTLY these keys:
title, description, gap_type, supporting_paper_indices, evidence_summary, confidence_score

No markdown fences, no commentary — raw JSON array only.
"""

GAP_IDENTIFICATION_USER_PROMPT = """Research topic/query: {query}
Domain hint: {domain}

Retrieved literature:
{papers_block}
"""

IDEA_GENERATION_SYSTEM_PROMPT = """You are an experienced research advisor helping a researcher choose \
a promising research direction. You will be given ONE specific research gap (grounded in real \
literature) and the papers that evidence it.

Generate {num_ideas} concrete, distinct research idea(s) that would address this gap. For each idea:
- summary: 1-2 sentences, specific and actionable (not vague like "explore X more").
- proposed_approach: a short paragraph on a plausible method/experimental design.
- rationale: a clear, evidence-based explanation of WHY this idea is worth pursuing right now — this is \
the most important field. Explicitly reference what the literature shows (or fails to show) to justify \
the idea. This is the "why should we work on this" justification the researcher needs.
- evidence_paper_indices: indices of papers (from the list given) that support the rationale.
- novelty_score, feasibility_score, impact_score: each 0-1, your honest estimate.

Respond ONLY with a JSON array of objects with EXACTLY these keys:
summary, proposed_approach, rationale, evidence_paper_indices, novelty_score, feasibility_score, impact_score

No markdown fences, no commentary — raw JSON array only.
"""

IDEA_GENERATION_USER_PROMPT = """Research gap: {gap_title}
Gap description: {gap_description}
Why this is a gap (evidence summary): {gap_evidence}

Supporting literature:
{papers_block}
"""

TITLE_GENERATION_SYSTEM_PROMPT = """You are an academic writing expert. Given a research idea, generate \
{num_titles} candidate paper titles in DIFFERENT styles: one "descriptive" (clear, standard academic \
phrasing, often with a colon), one "catchy" (short, memorable, still professional), and one "technical" \
(precise, method-forward, for a specialist audience).

Respond ONLY with a JSON array of objects with EXACTLY these keys: title_text, style
No markdown fences, no commentary — raw JSON array only.
"""

TITLE_GENERATION_USER_PROMPT = """Research idea summary: {idea_summary}
Proposed approach: {idea_approach}
"""
