from fastapi import APIRouter, Query
from app.services import collect_dashboard_snapshot, get_events, get_history

router = APIRouter(tags=["dashboard"])

@router.get("/dashboard")
def dashboard() -> dict:
    return collect_dashboard_snapshot()

@router.get("/history")
def history(limit: int = Query(default=30, ge=1, le=200)) -> dict:
    return {"history": get_history(limit)}

@router.get("/events")
def events(limit: int = Query(default=20, ge=1, le=100)) -> dict:
    return {"events": get_events(limit)}
