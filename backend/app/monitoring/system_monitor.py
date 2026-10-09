import os
import random
import psutil

from app.monitoring.database_monitor import measure_database_query_time
from app.monitoring.request_monitor import request_monitor
from app.monitoring.simulation_monitor import simulation_monitor

def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))

def get_system_metrics() -> dict:
    actual_cpu = psutil.cpu_percent(interval=0.05)
    actual_memory = psutil.virtual_memory().percent
    load_average = None
    if hasattr(os, "getloadavg"):
        try:
            load_average = os.getloadavg()[0]
        except OSError:
            pass

    req = request_monitor.snapshot()
    sim = simulation_monitor.snapshot()
    db_ms = measure_database_query_time()
    base_rps = max(req["traffic_rps"], 5.0)
    base_response = max(req["average_latency_ms"], 40.0)

    if sim.mode == "high-load":
        cpu = _clamp(max(actual_cpu, 82.0 + random.uniform(-3, 4)))
        memory = _clamp(max(actual_memory, 84.0 + random.uniform(-2, 4)))
        traffic = min(1200.0, base_rps * sim.multiplier + 400.0)
        db_query = min(400.0, max(db_ms, 45.0) * 3.5)
        response = min(900.0, max(base_response, 120.0) * 3.6)
        active_users = min(1500, max(25, int(traffic * 1.6)))
        system_load = max(load_average or 1.0, cpu / 8.0)
    else:
        cpu = _clamp(actual_cpu)
        memory = _clamp(actual_memory)
        traffic = min(500.0, max(base_rps, 2.0))
        db_query = max(db_ms, 1.0)
        response = min(400.0, max(base_response, 35.0))
        active_users = min(500, max(1, int(traffic * 1.3)))
        system_load = load_average if load_average is not None else round(cpu / 100, 2)

    return {
        "traffic_rps": round(traffic, 2),
        "response_time_ms": round(response, 2),
        "cpu_percent": round(cpu, 2),
        "memory_percent": round(memory, 2),
        "database_query_time_ms": round(db_query, 2),
        "active_users": active_users,
        "system_load": round(system_load, 2),
        "simulation_mode": sim.mode,
        "active_requests": req["active_requests"],
        "total_requests": req["total_requests"],
    }
