import { BrainCircuit, Gauge } from "lucide-react";

export default function PredictionPanel({ prediction }) {
  const probability = prediction ? prediction.probability * 100 : 0;
  const confidence = prediction ? prediction.confidence * 100 : 0;
  const highLoad = prediction?.status === "HIGH_LOAD";

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
      <div className="flex items-center gap-3">
        <div className="rounded-xl bg-slate-800 p-2">
          <BrainCircuit size={20} className="text-violet-300" />
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-slate-500">ML engine</p>
          <h3 className="font-semibold text-white">Load prediction</h3>
        </div>
      </div>
      <div className="mt-6 space-y-5">
        <div>
          <div className="mb-2 flex justify-between text-sm">
            <span className="text-slate-400">High-load probability</span>
            <span className="font-semibold text-white">{probability.toFixed(1)}%</span>
          </div>
          <div className="h-3 overflow-hidden rounded-full bg-slate-800">
            <div className={`h-full rounded-full transition-all ${highLoad ? "bg-amber-400" : "bg-emerald-400"}`} style={{ width: `${Math.max(3, probability)}%` }} />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-xl bg-slate-950/70 p-4">
            <p className="text-xs text-slate-500">Status</p>
            <p className="mt-1 font-semibold text-white">{prediction?.status || "—"}</p>
          </div>
          <div className="rounded-xl bg-slate-950/70 p-4">
            <p className="text-xs text-slate-500">Confidence</p>
            <p className="mt-1 font-semibold text-white">{confidence.toFixed(1)}%</p>
          </div>
        </div>
        <div className="flex gap-3 rounded-xl bg-slate-950/70 p-4">
          <Gauge size={20} className="mt-0.5 shrink-0 text-slate-500" />
          <p className="text-sm leading-6 text-slate-400">{prediction?.reason || "Waiting..."}</p>
        </div>
      </div>
    </div>
  );
}
