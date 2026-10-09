import { useEffect, useMemo, useState } from "react";
import { Activity, Database, Gauge, HardDrive, RefreshCw, Server, Users, Zap } from "lucide-react";

import { getDashboard, getEvents, getHistory, restoreNormal, simulateHighLoad } from "../lib/api";
import MetricsCard from "../components/MetricsCard";
import OptimizationLog from "../components/OptimizationLog";
import PerformanceChart from "../components/PerformanceChart";
import PredictionPanel from "../components/PredictionPanel";
import SystemStatus from "../components/SystemStatus";

export default function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [history, setHistory] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");

  async function refresh() {
    try {
      const [snapshot, historyData, eventData] = await Promise.all([
        getDashboard(),
        getHistory(35),
        getEvents(20),
      ]);
      setDashboard(snapshot);
      setHistory(historyData);
      setEvents(eventData);
      setError("");
    } catch {
      setError("Backend unavailable. Start FastAPI at http://127.0.0.1:8000 and refresh this page.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 2000);
    return () => clearInterval(id);
  }, []);

  async function runSimulation(action) {
    setActionLoading(true);
    try {
      if (action === "high-load") await simulateHighLoad();
      else await restoreNormal();
      await refresh();
    } catch {
      setError("Could not change simulation mode.");
    } finally {
      setActionLoading(false);
    }
  }

  const metrics = dashboard?.metrics;
  const prediction = dashboard?.prediction;
  const optimization = dashboard?.optimization;
  const modeLabel = metrics?.simulation_mode === "high-load" ? "HIGH LOAD DEMO" : "NORMAL";

  const lastUpdated = useMemo(
    () => dashboard?.timestamp ? new Date(dashboard.timestamp).toLocaleTimeString() : "—",
    [dashboard]
  );

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-400">
        <div className="flex items-center gap-3"><RefreshCw size={19} className="animate-spin" />Starting AutoTune...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-violet-500/15 p-2 text-violet-300"><Zap size={21} /></div>
              <h1 className="text-xl font-bold tracking-tight">AutoTune</h1>
            </div>
            <p className="mt-1 text-sm text-slate-500">ML-powered self-optimizing web application</p>
          </div>
          <div className="hidden text-right sm:block">
            <p className="text-xs uppercase tracking-[0.18em] text-slate-600">System mode</p>
            <p className="mt-1 font-semibold text-slate-200">{modeLabel}</p>
            <p className="text-xs text-slate-600">Updated {lastUpdated}</p>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl space-y-6 px-6 py-6">
        {error && <div className="rounded-2xl border border-rose-900/50 bg-rose-950/30 px-5 py-4 text-sm text-rose-300">{error}</div>}

        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <MetricsCard label="CPU utilization" value={metrics?.cpu_percent?.toFixed(1) ?? "—"} unit="%" icon={Gauge} warning={metrics?.cpu_percent > 75} />
          <MetricsCard label="Memory utilization" value={metrics?.memory_percent?.toFixed(1) ?? "—"} unit="%" icon={HardDrive} warning={metrics?.memory_percent > 80} />
          <MetricsCard label="Traffic volume" value={metrics?.traffic_rps?.toFixed(1) ?? "—"} unit="req/s" icon={Activity} warning={metrics?.traffic_rps > 400} />
          <MetricsCard label="Response time" value={metrics?.response_time_ms?.toFixed(0) ?? "—"} unit="ms" icon={Server} warning={metrics?.response_time_ms > 250} />
        </section>

        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <MetricsCard label="Database query time" value={metrics?.database_query_time_ms?.toFixed(1) ?? "—"} unit="ms" icon={Database} warning={metrics?.database_query_time_ms > 100} />
          <MetricsCard label="Active users" value={metrics?.active_users ?? "—"} unit="users" icon={Users} warning={metrics?.active_users > 700} />
          <MetricsCard label="System load" value={metrics?.system_load?.toFixed(2) ?? "—"} unit="load" icon={Activity} warning={metrics?.system_load > 8} />
        </section>

        <SystemStatus prediction={prediction} optimization={optimization} />

        <section className="grid gap-6 lg:grid-cols-[1.65fr_1fr]">
          <PerformanceChart data={history} />
          <PredictionPanel prediction={prediction} />
        </section>

        <section className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
          <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
            <div>
              <p className="text-xs uppercase tracking-[0.18em] text-slate-500">Recruitment demo</p>
              <h3 className="mt-1 text-xl font-semibold text-white">Trigger the self-optimizing cycle</h3>
              <p className="mt-1 max-w-2xl text-sm leading-6 text-slate-500">
                High-load mode simulates application stress. The ML model predicts degradation,
                the optimizer activates strategies, and normal mode triggers recovery.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <button
                disabled={actionLoading}
                onClick={() => runSimulation("high-load")}
                className="rounded-xl bg-amber-400 px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-amber-300 disabled:cursor-not-allowed disabled:opacity-60"
              >
                Simulate High Traffic
              </button>
              <button
                disabled={actionLoading}
                onClick={() => runSimulation("normal")}
                className="rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-sm font-semibold text-slate-100 transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                Restore Normal
              </button>
            </div>
          </div>
        </section>

        <OptimizationLog events={events} />

        <footer className="pb-8 text-center text-xs text-slate-600">AutoTune • Monitor → Predict → Optimize → Recover</footer>
      </main>
    </div>
  );
}
