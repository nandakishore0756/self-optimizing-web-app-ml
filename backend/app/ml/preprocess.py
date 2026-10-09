FEATURES = [
    "traffic_rps",
    "response_time_ms",
    "cpu_percent",
    "memory_percent",
    "database_query_time_ms",
    "active_users",
    "system_load",
]

def build_feature_row(metrics: dict) -> list[float]:
    return [float(metrics[name]) for name in FEATURES]
