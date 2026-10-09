import { Activity, RotateCcw, Zap } from "lucide-react";

export default function OptimizationLog({ events }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
      <div className="flex items-center gap-3">
        <div className="rounded-xl bg-slate-800 p-2"><Zap size={20} className="text-yellow-300" /></div>
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-slate-500">Automation</p>
          <h3 className="font-semibold text-white">Optimization events</h3>
        </div>
      </div>
      <div className="mt-5 space-y-3">
        {events.length === 0 && <p className="rounded-xl bg-slate-950/70 p-4 text-sm text-slate-500">No optimization events yet.</p>}
        {events.slice().reverse().map((event, index) => {
          const optimize = event.event_type === "OPTIMIZE";
          return (
            <div key={`${event.timestamp}-${index}`} className="rounded-xl border border-slate-800 bg-slate-950/60 p-4">
              <div className="flex items-start gap-3">
                {optimize ? <Zap size={18} className="mt-0.5 shrink-0 text-amber-400" /> : <RotateCcw size={18} className="mt-0.5 shrink-0 text-emerald-400" />}
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-xs font-semibold uppercase tracking-widest text-slate-500">{event.event_type}</span>
                    <span className="text-xs text-slate-600">{new Date(event.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <p className="mt-1 font-medium text-slate-200">{event.action}</p>
                  <p className="mt-1 text-sm leading-5 text-slate-500">{event.details}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      <div className="mt-5 flex items-center gap-2 text-xs text-slate-600"><Activity size={14} />Actions are application-level demo strategies.</div>
    </div>
  );
}
