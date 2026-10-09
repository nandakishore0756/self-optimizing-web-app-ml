from datetime import datetime, timezone
from sqlalchemy import desc

from app.database.database import SessionLocal
from app.database.models import MetricsRecord, OptimizationEvent
from app.ml.predict import predict_load
from app.monitoring.system_monitor import get_system_metrics
from app.optimizer.engine import apply_prediction

def collect_dashboard_snapshot() -> dict:
    metrics = get_system_metrics()
    prediction = predict_load(metrics)
    optimization = apply_prediction(prediction)

    db = SessionLocal()
    try:
        record = MetricsRecord(
            traffic_rps=metrics["traffic_rps"],
            response_time_ms=metrics["response_time_ms"],
            cpu_percent=metrics["cpu_percent"],
            memory_percent=metrics["memory_percent"],
            database_query_time_ms=metrics["database_query_time_ms"],
            active_users=metrics["active_users"],
            system_load=metrics["system_load"],
            simulation_mode=metrics["simulation_mode"],
            prediction_probability=prediction["probability"],
            prediction_status=prediction["status"],
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        record_id = record.id
    finally:
        db.close()

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
        "prediction": prediction,
        "optimization": optimization,
        "record_id": record_id,
    }

def get_history(limit: int = 30) -> list[dict]:
    limit = max(1, min(limit, 200))
    db = SessionLocal()
    try:
        rows = db.query(MetricsRecord).order_by(desc(MetricsRecord.id)).limit(limit).all()
        return [
            {
                "timestamp": row.timestamp.isoformat(),
                "traffic_rps": row.traffic_rps,
                "response_time_ms": row.response_time_ms,
                "cpu_percent": row.cpu_percent,
                "memory_percent": row.memory_percent,
                "database_query_time_ms": row.database_query_time_ms,
                "active_users": row.active_users,
                "system_load": row.system_load,
                "simulation_mode": row.simulation_mode,
                "prediction_probability": row.prediction_probability,
                "prediction_status": row.prediction_status,
            }
            for row in reversed(rows)
        ]
    finally:
        db.close()

def get_events(limit: int = 20) -> list[dict]:
    limit = max(1, min(limit, 100))
    db = SessionLocal()
    try:
        rows = db.query(OptimizationEvent).order_by(desc(OptimizationEvent.id)).limit(limit).all()
        return [
            {
                "timestamp": row.timestamp.isoformat(),
                "event_type": row.event_type,
                "action": row.action,
                "reason": row.reason,
                "details": row.details,
            }
            for row in reversed(rows)
        ]
    finally:
        db.close()
