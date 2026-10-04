import { FlaskConical, Sparkles } from "lucide-react";

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/60 bg-white/75 backdrop-blur-xl dark:border-slate-800/60 dark:bg-[#070d1f]/80">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
        {/* Logo + Brand */}
        <div className="flex items-center gap-3">
          <div
            className="relative flex h-9 w-9 items-center justify-center rounded-xl text-white shadow-lg"
            style={{ background: "linear-gradient(135deg, #4c62f5 0%, #7c3aed 100%)" }}
          >
            <FlaskConical size={18} />
            {/* subtle glow dot */}
            <span className="absolute -right-0.5 -top-0.5 h-2.5 w-2.5 rounded-full border-2 border-white bg-emerald-400 dark:border-[#070d1f]" />
          </div>
          <div>
            <p className="text-sm font-bold tracking-tight text-slate-900 dark:text-white">
              AI Research Assistant
            </p>
            <p className="hidden text-[11px] text-slate-500 dark:text-slate-400 sm:block">
              Literature discovery &amp; idea generation
            </p>
          </div>
        </div>

        {/* Right side badge */}
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-medium text-brand-700 dark:border-brand-800/40 dark:bg-brand-900/20 dark:text-brand-300">
            <Sparkles size={11} />
            Agentic Pipeline · Phases 0–4
          </span>
        </div>
      </div>
    </header>
  );
}
