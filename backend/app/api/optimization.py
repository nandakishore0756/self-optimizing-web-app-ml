from fastapi import APIRouter
from app.optimizer.state import state_manager
from app.services import get_events

router = APIRouter(prefix="/optimization", tags=["optimization"])

@router.get("/state")
def optimization_state() -> dict:
    return state_manager.snapshot()

@router.get("/events")
def optimization_events(limit: int = 20) -> dict:
    return {"events": get_events(limit)}
