import { CheckCircle2, ShieldAlert } from "lucide-react";

export default function SystemStatus({ prediction, optimization }) {
  const highLoad = prediction?.status === "HIGH_LOAD";
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-black/10">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-400">System status</p>
          <h2 className="mt-1 text-xl font-semibold text-white">
            {highLoad ? "High load detected" : "Operating normally"}
          </h2>
        </div>
        {highLoad ? <ShieldAlert className="text-amber-400" size={28} /> : <CheckCircle2 className="text-emerald-400" size={28} />}
      </div>
      <div className="grid gap-3 sm:grid-cols-3">
        <div className="rounded-xl bg-slate-950/70 p-4">
          <p className="text-xs text-slate-500">Prediction</p>
          <p className={`mt-1 font-semibold ${highLoad ? "text-amber-300" : "text-emerald-300"}`}>{prediction?.status || "—"}</p>
        </div>
        <div className="rounded-xl bg-slate-950/70 p-4">
          <p className="text-xs text-slate-500">Risk probability</p>
          <p className="mt-1 font-semibold text-white">{prediction ? `${(prediction.probability * 100).toFixed(1)}%` : "—"}</p>
        </div>
        <div className="rounded-xl bg-slate-950/70 p-4">
          <p className="text-xs text-slate-500">Optimization</p>
          <p className="mt-1 font-semibold text-white">{optimization?.state?.optimized ? "ACTIVE" : "STANDBY"}</p>
        </div>
      </div>
      <p className="mt-4 text-sm leading-6 text-slate-400">
        {prediction?.reason || "Waiting for performance data..."}
      </p>
    </div>
  );
}
