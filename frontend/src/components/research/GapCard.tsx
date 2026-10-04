"use client";

import { useState } from "react";
import { ChevronDown, Target } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/lib/cn";
import type { GapType, Paper, ResearchGap } from "@/lib/types";

interface GapCardProps {
  gap: ResearchGap;
  papers: Paper[];
  index?: number;
}

const GAP_TYPE_VARIANT: Record<GapType, "info" | "warning" | "default" | "danger" | "purple"> = {
  methodological: "info",
  empirical: "default",
  theoretical: "warning",
  application: "purple",
  contradiction: "danger",
};

const GAP_TYPE_COLOR: Record<GapType, string> = {
  methodological: "border-l-brand-400",
  empirical: "border-l-slate-400",
  theoretical: "border-l-amber-400",
  application: "border-l-violet-400",
  contradiction: "border-l-rose-400",
};

export function GapCard({ gap, papers, index = 0 }: GapCardProps) {
  const [expanded, setExpanded] = useState(false);
  const supportingPapers = papers.filter((p) => gap.supporting_paper_ids.includes(p.id));
  const pct = Math.round(gap.confidence_score * 100);

  return (
    <div
      className={cn(
        "rounded-xl border border-slate-200/80 bg-white shadow-sm transition-all duration-200",
        "dark:border-slate-800/70 dark:bg-slate-900/60",
        "border-l-[3px]",
        GAP_TYPE_COLOR[gap.gap_type],
        "hover:shadow-md",
        "animate-fade-in"
      )}
      style={{ animationDelay: `${index * 60}ms` }}
    >
      {/* Always visible: title, type, confidence */}
      <button
        type="button"
        className="flex w-full items-start gap-3 p-4 text-left"
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
      >
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2 mb-1">
            <Badge variant={GAP_TYPE_VARIANT[gap.gap_type]}>{gap.gap_type}</Badge>
            <span className="text-[11px] font-semibold text-slate-400">
              {pct}% confidence
            </span>
          </div>
          <h4 className="text-sm font-bold leading-snug text-slate-900 dark:text-white">
            {gap.title}
          </h4>
          {!expanded && (
            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 line-clamp-2">
              {gap.description}
            </p>
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
        <div className="border-t border-slate-100 px-4 pb-4 pt-3 space-y-3 dark:border-slate-800/60 animate-fade-in">
          <p className="text-sm text-slate-600 dark:text-slate-300">{gap.description}</p>

          <div className="rounded-lg bg-slate-50 p-3 dark:bg-slate-800/50">
            <p className="mb-1 text-[10px] font-bold uppercase tracking-widest text-slate-400">
              Why this is a gap
            </p>
            <p className="text-xs leading-relaxed text-slate-600 dark:text-slate-300">
              {gap.evidence_summary}
            </p>
          </div>

          {supportingPapers.length > 0 && (
            <div>
              <p className="mb-1.5 text-[10px] font-bold uppercase tracking-widest text-slate-400">
                Evidenced by
              </p>
              <ul className="space-y-1">
                {supportingPapers.map((p) => (
                  <li key={p.id} className="flex items-start gap-1.5 text-xs text-slate-500 dark:text-slate-400">
                    <span className="mt-1 h-1 w-1 shrink-0 rounded-full bg-brand-400" />
                    <span>
                      {p.title}{" "}
                      <span className="text-slate-400">({p.published_year ?? "n.d."})</span>
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Confidence bar */}
          <div>
            <div className="mb-1 flex items-center justify-between text-[10px] font-bold uppercase tracking-widest text-slate-400">
              <span>Confidence</span>
              <span className={cn(pct >= 70 ? "text-emerald-500" : pct >= 40 ? "text-amber-500" : "text-rose-500")}>
                {pct}%
              </span>
            </div>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
              <div
                className={cn(
                  "h-full rounded-full bg-gradient-to-r transition-all duration-700",
                  pct >= 70 ? "from-emerald-400 to-emerald-500" : pct >= 40 ? "from-amber-400 to-orange-400" : "from-rose-400 to-rose-500"
                )}
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
