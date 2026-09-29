import { FlaskConical } from "lucide-react";

export function Header() {
  return (
    <header className="border-b border-slate-200 bg-white/80 backdrop-blur dark:border-slate-800 dark:bg-slate-950/80">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2">
          <div className="rounded-lg bg-brand-600 p-1.5 text-white">
            <FlaskConical size={18} />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900 dark:text-white">
              AI Research Assistant
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Literature discovery &amp; research idea generation
            </p>
          </div>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-500 dark:bg-slate-800 dark:text-slate-400">
          Phases 0–4
        </span>
      </div>
    </header>
  );
}
