from fastapi import APIRouter
from app.monitoring.system_monitor import get_system_metrics

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("")
def metrics() -> dict:
    return get_system_metrics()
