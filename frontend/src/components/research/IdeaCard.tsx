"use client";

import { useState } from "react";
import { Check, X, ChevronDown, Lightbulb } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { ScoreBar } from "@/components/ui/ScoreBar";
import { TitleSelector } from "@/components/research/TitleSelector";
import { cn } from "@/lib/cn";
import type { Paper, ResearchGap, ResearchIdea } from "@/lib/types";

interface IdeaCardProps {
  idea: ResearchIdea;
  gap?: ResearchGap;
  papers: Paper[];
  onReview: (ideaId: string, status: "approved" | "rejected", selectedTitleId?: string) => Promise<void>;
  index?: number;
}

const STATUS_VARIANT = {
  pending: "default",
  approved: "success",
  rejected: "danger",
  edited: "info",
} as const;

const STATUS_COLOR: Record<string, string> = {
  approved: "border-l-emerald-400",
  rejected: "border-l-rose-400",
  edited: "border-l-brand-400",
  pending: "border-l-slate-200 dark:border-l-slate-700",
};

export function IdeaCard({ idea, gap, papers, onReview, index = 0 }: IdeaCardProps) {
  const [selectedTitleId, setSelectedTitleId] = useState<string | null>(
    idea.titles.find((t) => t.is_selected)?.id ?? null
  );
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [expanded, setExpanded] = useState(idea.review_status === "pending");

  const evidencePapers = papers.filter((p) => idea.evidence_citations.includes(p.id));
  const isDecided = idea.review_status !== "pending";

  const avgScore = Math.round(
    ((idea.novelty_score + idea.feasibility_score + idea.impact_score) / 3) * 100
  );

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
    <div
      className={cn(
        "rounded-2xl border border-slate-200/80 bg-white shadow-sm transition-all duration-200",
        "dark:border-slate-800/70 dark:bg-slate-900/60",
        "border-l-[3px]",
        STATUS_COLOR[idea.review_status],
        "hover:shadow-md",
        "animate-fade-in"
      )}
      style={{ animationDelay: `${index * 60}ms` }}
    >
      {/* Always-visible header */}
      <button
        type="button"
        className="flex w-full items-start gap-3 p-4 text-left"
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
      >
        <div className="min-w-0 flex-1">
          {/* Meta row */}
          <div className="mb-1.5 flex flex-wrap items-center gap-2">
            <Badge variant={STATUS_VARIANT[idea.review_status]}>{idea.review_status}</Badge>
            {gap && (
              <span className="text-[11px] font-medium text-brand-600 dark:text-brand-400 truncate max-w-[200px]">
                → {gap.title}
              </span>
            )}
            <span className="ml-auto text-[11px] font-bold text-slate-400">
              avg&nbsp;{avgScore}%
            </span>
          </div>

          {/* Summary — always visible */}
          <p className="text-sm font-bold leading-snug text-slate-900 dark:text-white">
            {idea.summary}
          </p>

          {/* Collapsed preview: score mini-bars */}
          {!expanded && (
            <div className="mt-2 flex gap-3">
              {[
                { label: "N", value: idea.novelty_score },
                { label: "F", value: idea.feasibility_score },
                { label: "I", value: idea.impact_score },
              ].map(({ label, value }) => {
                const pct = Math.round(value * 100);
                const color =
                  pct >= 70
                    ? "bg-emerald-400"
                    : pct >= 40
                    ? "bg-amber-400"
                    : "bg-rose-400";
                return (
                  <div key={label} className="flex items-center gap-1">
                    <span className="text-[10px] font-bold text-slate-400">{label}</span>
                    <div className="h-1 w-12 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
                      <div className={cn("h-full rounded-full", color)} style={{ width: `${pct}%` }} />
                    </div>
                    <span className="text-[10px] font-semibold text-slate-500">{pct}%</span>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <ChevronDown
          size={15}
          className={cn(
            "mt-1 shrink-0 text-slate-400 transition-transform duration-200",
            expanded && "rotate-180"
          )}
        />
      </button>

      {/* Expanded detail */}
      {expanded && (
        <div className="border-t border-slate-100 px-4 pb-4 pt-3 space-y-4 dark:border-slate-800/60 animate-fade-in">
          {/* Proposed approach */}
          <div>
            <p className="mb-1 text-[10px] font-bold uppercase tracking-widest text-slate-400">
              Proposed Approach
            </p>
            <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-300">
              {idea.proposed_approach}
            </p>
          </div>

          {/* Rationale */}
          <div className="rounded-xl border border-brand-100 bg-gradient-to-br from-brand-50/80 to-violet-50/50 p-3 dark:border-brand-900/30 dark:from-brand-900/10 dark:to-violet-900/10">
            <div className="mb-1.5 flex items-center gap-1.5">
              <Lightbulb size={12} className="text-brand-500" />
              <p className="text-[10px] font-bold uppercase tracking-widest text-brand-600 dark:text-brand-400">
                Why work on this
              </p>
            </div>
            <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-200">
              {idea.rationale}
            </p>
            {evidencePapers.length > 0 && (
              <ul className="mt-2 space-y-1">
                {evidencePapers.map((p) => (
                  <li key={p.id} className="flex items-start gap-1.5 text-xs text-slate-500 dark:text-slate-400">
                    <span className="mt-1 h-1 w-1 shrink-0 rounded-full bg-brand-400" />
                    <span>
                      {p.title}{" "}
                      <span className="text-slate-400">({p.published_year ?? "n.d."})</span>
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Score bars */}
          <div className="flex flex-col gap-2 sm:flex-row">
            <ScoreBar label="Novelty" value={idea.novelty_score} />
            <ScoreBar label="Feasibility" value={idea.feasibility_score} />
            <ScoreBar label="Impact" value={idea.impact_score} />
          </div>

          {/* Title selector */}
          <TitleSelector
            titles={idea.titles}
            selectedTitleId={selectedTitleId}
            onSelect={setSelectedTitleId}
            disabled={isDecided}
          />

          {/* Actions */}
          {!isDecided && (
            <div className="flex gap-2 pt-1">
              <Button size="sm" onClick={handleApprove} disabled={isSubmitting}>
                <Check size={13} />
                Approve idea
              </Button>
              <Button size="sm" variant="secondary" onClick={handleReject} disabled={isSubmitting}>
                <X size={13} />
                Reject
              </Button>
            </div>
          )}

          {isDecided && (
            <p className={cn(
              "text-xs font-semibold",
              idea.review_status === "approved" ? "text-emerald-600 dark:text-emerald-400" : "text-slate-400"
            )}>
              {idea.review_status === "approved" ? "✓ Approved" : "✗ Rejected"}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
