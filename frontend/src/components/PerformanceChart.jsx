import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function PerformanceChart({ data }) {
  const chartData = data.map((item) => ({
    time: new Date(item.timestamp).toLocaleTimeString(),
    cpu: item.cpu_percent,
    memory: item.memory_percent,
    latency: item.response_time_ms,
    traffic: item.traffic_rps / 10,
  }));

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
      <div className="mb-5">
        <p className="text-xs uppercase tracking-[0.18em] text-slate-500">Live telemetry</p>
        <h3 className="mt-1 text-xl font-semibold text-white">Performance trends</h3>
        <p className="mt-1 text-sm text-slate-500">CPU, memory, response time, and traffic scale over time.</p>
      </div>
      <div className="h-[320px]">
        {chartData.length < 2 ? (
          <div className="flex h-full items-center justify-center rounded-xl bg-slate-950/50 text-sm text-slate-600">Collecting telemetry...</div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" tick={{ fill: "#64748b", fontSize: 11 }} />
              <YAxis tick={{ fill: "#64748b", fontSize: 11 }} />
              <Tooltip contentStyle={{ background: "#020617", border: "1px solid #1e293b", borderRadius: 12, color: "#e2e8f0" }} />
              <Line type="monotone" dataKey="cpu" stroke="#a78bfa" strokeWidth={2.5} dot={false} name="CPU %" />
              <Line type="monotone" dataKey="memory" stroke="#38bdf8" strokeWidth={2.5} dot={false} name="Memory %" />
              <Line type="monotone" dataKey="latency" stroke="#fbbf24" strokeWidth={2.5} dot={false} name="Response ms" />
              <Line type="monotone" dataKey="traffic" stroke="#34d399" strokeWidth={2.5} dot={false} name="Traffic / 10" />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
