"use client";

import { type FormEvent, useState } from "react";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";

interface ResearchInputFormProps {
  onSubmit: (query: string, domain: string) => void;
  isSubmitting: boolean;
}

const EXAMPLE_QUERIES = [
  "Few-shot learning for low-resource language translation",
  "Graph neural networks for drug discovery",
  "Explainability methods for large language models",
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
    <Card>
      <CardContent className="space-y-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
            What do you want to research?
          </h2>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Enter keywords or describe your research interest. We&apos;ll retrieve literature,
            analyze it, and surface evidence-backed gaps and ideas.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={3}
            placeholder="e.g. graph neural networks for drug discovery, or a longer description of your interest..."
            className="w-full resize-none rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-slate-700 dark:bg-slate-900 dark:text-white"
            required
          />
          <input
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            placeholder="Optional: domain hint (e.g. NLP, Computer Vision, Bioinformatics)"
            className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-slate-700 dark:bg-slate-900 dark:text-white"
          />

          <div className="flex flex-wrap items-center gap-2">
            {EXAMPLE_QUERIES.map((example) => (
              <button
                type="button"
                key={example}
                onClick={() => setQuery(example)}
                className="rounded-full border border-slate-200 px-3 py-1 text-xs text-slate-500 hover:border-brand-300 hover:text-brand-600 dark:border-slate-700 dark:text-slate-400"
              >
                {example}
              </button>
            ))}
          </div>

          <Button type="submit" disabled={isSubmitting || !query.trim()} className="w-full sm:w-auto">
            <Search size={16} />
            {isSubmitting ? "Starting pipeline..." : "Discover literature & generate ideas"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
