// Shared types mirroring backend Pydantic schemas (app/schemas/*).
// Keeping these in one place means every component/hook imports from here
// instead of re-declaring shapes, so a backend schema change only needs one
// frontend edit.

export type PipelineStage =
  | "created"
  | "retrieving_literature"
  | "analyzing_literature"
  | "identifying_gaps"
  | "synthesizing_evidence"
  | "generating_ideas"
  | "generating_titles"
  | "awaiting_human_review"
  | "completed"
  | "failed";

export const PIPELINE_STAGE_ORDER: PipelineStage[] = [
  "created",
  "retrieving_literature",
  "analyzing_literature",
  "identifying_gaps",
  "synthesizing_evidence",
  "generating_ideas",
  "generating_titles",
  "awaiting_human_review",
];

export const PIPELINE_STAGE_LABELS: Record<PipelineStage, string> = {
  created: "Session created",
  retrieving_literature: "Retrieving literature",
  analyzing_literature: "Analyzing literature",
  identifying_gaps: "Identifying research gaps",
  synthesizing_evidence: "Synthesizing evidence",
  generating_ideas: "Generating research ideas",
  generating_titles: "Generating titles",
  awaiting_human_review: "Ready for your review",
  completed: "Completed",
  failed: "Failed",
};

export interface ResearchSession {
  id: string;
  query: string;
  domain: string | null;
  stage: PipelineStage;
  error_message: string | null;
  llm_provider: string;
  llm_model: string;
  search_providers: string;
  created_at: string;
  updated_at: string;
}

export interface Paper {
  id: string;
  source: string;
  source_id: string;
  title: string;
  abstract: string | null;
  authors: string[];
  published_year: number | null;
  url: string | null;
  pdf_url: string | null;
  citation_count: number | null;
  venue: string | null;
  summary: string | null;
}

export type GapType =
  | "methodological"
  | "empirical"
  | "theoretical"
  | "application"
  | "contradiction";

export interface ResearchGap {
  id: string;
  title: string;
  description: string;
  gap_type: GapType;
  supporting_paper_ids: string[];
  evidence_summary: string;
  confidence_score: number;
}

export type ReviewStatus = "pending" | "approved" | "rejected" | "edited";

export interface ResearchTitle {
  id: string;
  title_text: string;
  style: string;
  review_status: ReviewStatus;
  is_selected: boolean;
}

export interface ResearchIdea {
  id: string;
  gap_id: string;
  summary: string;
  proposed_approach: string;
  rationale: string;
  evidence_citations: string[];
  novelty_score: number;
  feasibility_score: number;
  impact_score: number;
  review_status: ReviewStatus;
  reviewer_notes: string | null;
  titles: ResearchTitle[];
}

export interface CreateSessionPayload {
  query: string;
  domain?: string | null;
}

export interface HumanReviewPayload {
  idea_id: string;
  status: ReviewStatus;
  reviewer_notes?: string | null;
  selected_title_id?: string | null;
}
