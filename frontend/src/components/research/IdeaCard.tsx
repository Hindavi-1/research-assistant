"use client";

import { useState } from "react";
import { Check, X } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { ScoreBar } from "@/components/ui/ScoreBar";
import { TitleSelector } from "@/components/research/TitleSelector";
import type { Paper, ResearchGap, ResearchIdea } from "@/lib/types";

interface IdeaCardProps {
  idea: ResearchIdea;
  gap?: ResearchGap;
  papers: Paper[];
  onReview: (ideaId: string, status: "approved" | "rejected", selectedTitleId?: string) => Promise<void>;
}

const STATUS_VARIANT = {
  pending: "default",
  approved: "success",
  rejected: "danger",
  edited: "info",
} as const;

export function IdeaCard({ idea, gap, papers, onReview }: IdeaCardProps) {
  const [selectedTitleId, setSelectedTitleId] = useState<string | null>(
    idea.titles.find((t) => t.is_selected)?.id ?? null
  );
  const [isSubmitting, setIsSubmitting] = useState(false);

  const evidencePapers = papers.filter((p) => idea.evidence_citations.includes(p.id));
  const isDecided = idea.review_status !== "pending";

  const handleApprove = async () => {
    setIsSubmitting(true);
    try {
      await onReview(idea.id, "approved", selectedTitleId ?? undefined);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReject = async () => {
    setIsSubmitting(true);
    try {
      await onReview(idea.id, "rejected");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <CardContent className="space-y-4">
        <div className="flex items-start justify-between gap-2">
          <div>
            {gap && <p className="text-xs font-medium text-brand-600">Addresses: {gap.title}</p>}
            <p className="mt-1 text-sm font-semibold text-slate-900 dark:text-white">{idea.summary}</p>
          </div>
          <Badge variant={STATUS_VARIANT[idea.review_status]}>{idea.review_status}</Badge>
        </div>

        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Proposed approach</p>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">{idea.proposed_approach}</p>
        </div>

        <div className="rounded-lg border border-brand-100 bg-brand-50/60 p-3 dark:border-brand-900/40 dark:bg-brand-900/10">
          <p className="text-xs font-medium uppercase tracking-wide text-brand-600">
            Why work on this idea
          </p>
          <p className="mt-1 text-sm text-slate-700 dark:text-slate-200">{idea.rationale}</p>
          {evidencePapers.length > 0 && (
            <ul className="mt-2 space-y-0.5">
              {evidencePapers.map((p) => (
                <li key={p.id} className="text-xs text-slate-500 dark:text-slate-400">
                  · {p.title} ({p.published_year ?? "n.d."})
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="flex flex-col gap-2 sm:flex-row">
          <ScoreBar label="Novelty" value={idea.novelty_score} />
          <ScoreBar label="Feasibility" value={idea.feasibility_score} />
          <ScoreBar label="Impact" value={idea.impact_score} />
        </div>

        <TitleSelector
          titles={idea.titles}
          selectedTitleId={selectedTitleId}
          onSelect={setSelectedTitleId}
          disabled={isDecided}
        />

        {!isDecided && (
          <div className="flex gap-2 pt-1">
            <Button size="sm" onClick={handleApprove} disabled={isSubmitting}>
              <Check size={14} /> Approve idea
            </Button>
            <Button size="sm" variant="secondary" onClick={handleReject} disabled={isSubmitting}>
              <X size={14} /> Reject
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
