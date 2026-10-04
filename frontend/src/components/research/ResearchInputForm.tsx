"use client";

import { type FormEvent, useState } from "react";
import { Search, Zap } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface ResearchInputFormProps {
  onSubmit: (query: string, domain: string) => void;
  isSubmitting: boolean;
}

const EXAMPLE_QUERIES = [
  "Few-shot learning for low-resource NLP",
  "Graph neural networks for drug discovery",
  "Explainability in large language models",
  "Federated learning for medical imaging",
];

export function ResearchInputForm({ onSubmit, isSubmitting }: ResearchInputFormProps) {
  const [query, setQuery] = useState("");
  const [domain, setDomain] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSubmit(query.trim(), domain.trim());
  };

  return (
    <div className="relative overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-sm dark:border-slate-800/70 dark:bg-slate-900/60">
      {/* Gradient accent top bar */}
      <div
        className="absolute inset-x-0 top-0 h-1 rounded-t-2xl"
        style={{ background: "linear-gradient(90deg, #4c62f5 0%, #7c3aed 50%, #4c62f5 100%)" }}
      />

      <div className="px-6 pb-5 pt-6 space-y-4">
        {/* Heading */}
        <div>
          <h2 className="text-lg font-extrabold tracking-tight text-slate-900 dark:text-white">
            What do you want to&nbsp;
            <span className="gradient-text">research?</span>
          </h2>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400 max-w-xl">
            Enter keywords or describe your interest. The pipeline will retrieve literature,
            identify gaps, and generate evidence-backed ideas &amp; titles.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          {/* Query textarea */}
          <textarea
            id="research-query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={3}
            placeholder="e.g. graph neural networks for drug discovery, or a longer description of your research interest..."
            className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50/70 px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 transition-all focus:border-brand-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-slate-700 dark:bg-slate-800/50 dark:text-white dark:focus:border-brand-500 dark:focus:bg-slate-800"
            required
          />

          {/* Domain input */}
          <input
            id="research-domain"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            placeholder="Optional: domain hint (e.g. NLP, Computer Vision, Bioinformatics)"
            className="w-full rounded-xl border border-slate-200 bg-slate-50/70 px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 transition-all focus:border-brand-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-slate-700 dark:bg-slate-800/50 dark:text-white dark:focus:border-brand-500 dark:focus:bg-slate-800"
          />

          {/* Example queries */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[11px] font-semibold uppercase tracking-wide text-slate-400">
              Try:
            </span>
            {EXAMPLE_QUERIES.map((example) => (
              <button
                type="button"
                key={example}
                onClick={() => setQuery(example)}
                className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs text-slate-500 transition-all hover:border-brand-300 hover:bg-brand-50 hover:text-brand-600 dark:border-slate-700 dark:bg-slate-800/60 dark:text-slate-400 dark:hover:border-brand-700 dark:hover:text-brand-400"
              >
                {example}
              </button>
            ))}
          </div>

          {/* Submit */}
          <div className="flex items-center gap-3 pt-1">
            <Button
              id="submit-research"
              type="submit"
              size="lg"
              disabled={isSubmitting || !query.trim()}
              className="min-w-[220px]"
            >
              {isSubmitting ? (
                <>
                  <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                  Running pipeline…
                </>
              ) : (
                <>
                  <Search size={15} />
                  Discover &amp; generate ideas
                </>
              )}
            </Button>
            {isSubmitting && (
              <span className="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
                <Zap size={12} className="text-amber-500 animate-pulse" />
                Agentic pipeline running…
              </span>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
