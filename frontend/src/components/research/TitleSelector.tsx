import { CheckCircle2 } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/lib/cn";
import type { ResearchTitle } from "@/lib/types";

interface TitleSelectorProps {
  titles: ResearchTitle[];
  selectedTitleId: string | null;
  onSelect: (titleId: string) => void;
  disabled?: boolean;
}

export function TitleSelector({ titles, selectedTitleId, onSelect, disabled }: TitleSelectorProps) {
  if (titles.length === 0) return null;

  return (
    <div className="space-y-2">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
        Candidate titles — pick one
      </p>
      {titles.map((title) => {
        const isSelected = title.id === selectedTitleId || title.is_selected;
        return (
          <button
            key={title.id}
            type="button"
            disabled={disabled}
            onClick={() => onSelect(title.id)}
            className={cn(
              "flex w-full items-center justify-between gap-2 rounded-lg border px-3 py-2 text-left text-sm transition-colors",
              isSelected
                ? "border-brand-500 bg-brand-50 dark:bg-brand-900/20"
                : "border-slate-200 hover:border-brand-300 dark:border-slate-700",
              disabled && "cursor-not-allowed opacity-60"
            )}
          >
            <span className="flex-1 text-slate-800 dark:text-slate-100">{title.title_text}</span>
            <Badge>{title.style}</Badge>
            {isSelected && <CheckCircle2 size={16} className="shrink-0 text-brand-600" />}
          </button>
        );
      })}
    </div>
  );
}
