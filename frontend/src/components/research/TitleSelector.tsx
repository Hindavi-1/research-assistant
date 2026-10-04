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
      <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
        Candidate titles — pick one
      </p>
      <div className="space-y-1.5">
        {titles.map((title) => {
          const isSelected = title.id === selectedTitleId || title.is_selected;
          return (
            <button
              key={title.id}
              type="button"
              disabled={disabled}
              onClick={() => onSelect(title.id)}
              className={cn(
                "group flex w-full items-start gap-2.5 rounded-xl border px-3.5 py-2.5 text-left text-sm transition-all duration-150",
                isSelected
                  ? "border-brand-400 bg-brand-50 shadow-sm dark:border-brand-600 dark:bg-brand-900/20"
                  : "border-slate-200 bg-slate-50/50 hover:border-brand-300 hover:bg-brand-50/40 dark:border-slate-700/70 dark:bg-slate-800/30 dark:hover:border-brand-700 dark:hover:bg-brand-900/10",
                disabled && "cursor-not-allowed opacity-60"
              )}
            >
              {/* Selection indicator */}
              <span
                className={cn(
                  "mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-full border-2 transition-all",
                  isSelected
                    ? "border-brand-500 bg-brand-500"
                    : "border-slate-300 dark:border-slate-600"
                )}
              >
                {isSelected && <span className="h-1.5 w-1.5 rounded-full bg-white" />}
              </span>

              <span className="flex-1 font-medium leading-snug text-slate-800 dark:text-slate-100">
                {title.title_text}
              </span>

              <div className="flex shrink-0 items-center gap-1.5">
                <Badge>{title.style}</Badge>
                {isSelected && <CheckCircle2 size={14} className="text-brand-500" />}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
