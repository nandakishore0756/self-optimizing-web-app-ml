from app.database.database import SessionLocal
from app.database.models import OptimizationEvent
from app.optimizer.state import state_manager

def _log_event(event_type: str, action: str, reason: str, details: str) -> None:
    db = SessionLocal()
    try:
        db.add(OptimizationEvent(
            event_type=event_type,
            action=action,
            reason=reason,
            details=details,
        ))
        db.commit()
    finally:
        db.close()

def apply_prediction(prediction: dict) -> dict:
    status = prediction["status"]
    current = state_manager.snapshot()

    if status == "HIGH_LOAD" and not current["optimized"]:
        reason = prediction["reason"]
        new_state = state_manager.optimize(reason)
        actions = [
            "Response caching enabled",
            "Database query optimization enabled",
            "Pagination limit reduced from 50 to 20",
            "Heavy non-essential components disabled",
        ]
        _log_event("OPTIMIZE", "Auto-optimization activated", reason, "; ".join(actions))
        return {"state": new_state, "actions": actions}

    if status == "NORMAL" and current["optimized"]:
        reason = "Load returned to the normal range."
        new_state = state_manager.recover(reason)
        _log_event(
            "RECOVER",
            "Standard configuration restored",
            reason,
            "Caching disabled; normal pagination restored; heavy components re-enabled.",
        )
        return {"state": new_state, "actions": ["Standard application configuration restored"]}

    return {"state": current, "actions": []}
