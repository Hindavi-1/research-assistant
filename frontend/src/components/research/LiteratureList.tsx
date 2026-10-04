"use client";

import { useState } from "react";
import { ExternalLink, ChevronDown, BookOpen } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/lib/cn";
import type { Paper } from "@/lib/types";

interface LiteratureListProps {
  papers: Paper[];
}

function PaperCard({ paper, index }: { paper: Paper; index: number }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      className={cn(
        "group rounded-xl border border-slate-200/70 bg-slate-50/50 transition-all duration-200",
        "dark:border-slate-800/60 dark:bg-slate-800/30",
        "hover:border-brand-200 hover:bg-white hover:shadow-sm dark:hover:border-brand-800/40 dark:hover:bg-slate-800/50",
        "animate-fade-in"
      )}
      style={{ animationDelay: `${index * 40}ms` }}
    >
      {/* Always-visible header row */}
      <button
        type="button"
        className="flex w-full items-start gap-3 p-3 text-left"
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
      >
        {/* Index number */}
        <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-brand-100 text-[10px] font-bold text-brand-600 dark:bg-brand-900/40 dark:text-brand-400">
          {index + 1}
        </span>

        <div className="min-w-0 flex-1">
          <p className="text-sm font-semibold leading-snug text-slate-800 dark:text-slate-100 line-clamp-2 group-hover:text-brand-700 dark:group-hover:text-brand-300 transition-colors">
            {paper.title}
          </p>
          <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400 truncate">
            {paper.authors.slice(0, 2).join(", ")}
            {paper.authors.length > 2 ? " et al." : ""} &middot;{" "}
            {paper.published_year ?? "n.d."}
          </p>
        </div>

        <div className="flex shrink-0 items-center gap-1.5 ml-2">
          <Badge variant="info">{paper.source}</Badge>
          {paper.url && (
            <a
              href={paper.url}
              target="_blank"
              rel="noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="rounded-md p-1 text-slate-400 hover:bg-brand-50 hover:text-brand-600 dark:hover:bg-brand-900/30 dark:hover:text-brand-400 transition-colors"
              title="Open paper"
            >
              <ExternalLink size={13} />
            </a>
          )}
          <ChevronDown
            size={14}
            className={cn(
              "text-slate-400 transition-transform duration-200",
              expanded && "rotate-180"
            )}
          />
        </div>
      </button>

      {/* Expanded detail */}
      {expanded && (
        <div className="border-t border-slate-100 px-3 pb-3 pt-2.5 dark:border-slate-800/60 animate-fade-in">
          {paper.summary && (
            <p className="mb-2 text-xs leading-relaxed text-slate-600 dark:text-slate-300">
              {paper.summary}
            </p>
          )}
          {!paper.summary && paper.abstract && (
            <p className="mb-2 text-xs leading-relaxed text-slate-600 dark:text-slate-300 line-clamp-4">
              {paper.abstract}
            </p>
          )}
          <div className="flex flex-wrap gap-1.5">
            {typeof paper.citation_count === "number" && (
              <Badge>{paper.citation_count} citations</Badge>
            )}
            {paper.venue && <Badge>{paper.venue}</Badge>}
            {paper.pdf_url && (
              <a
                href={paper.pdf_url}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-wide bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200 hover:bg-emerald-100 dark:bg-emerald-900/30 dark:text-emerald-300 dark:ring-emerald-800/50 transition-colors"
              >
                PDF ↗
              </a>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export function LiteratureList({ papers }: LiteratureListProps) {
  if (papers.length === 0) return null;

  return (
    <section>
      {/* Section header */}
      <div className="mb-3 flex items-center gap-2">
        <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-brand-100 dark:bg-brand-900/40">
          <BookOpen size={13} className="text-brand-600 dark:text-brand-400" />
        </div>
        <h3 className="text-sm font-bold text-slate-800 dark:text-white">
          Retrieved literature
        </h3>
        <span className="ml-auto rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-500 dark:bg-slate-800 dark:text-slate-400">
          {papers.length}
        </span>
      </div>

      <div className="space-y-2 stagger-children">
        {papers.map((paper, i) => (
          <PaperCard key={paper.id} paper={paper} index={i} />
        ))}
      </div>
    </section>
  );
}
