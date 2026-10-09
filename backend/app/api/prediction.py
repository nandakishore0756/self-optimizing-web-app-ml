from fastapi import APIRouter
from app.ml.predict import predict_load
from app.monitoring.system_monitor import get_system_metrics

router = APIRouter(prefix="/prediction", tags=["prediction"])

@router.get("")
def prediction() -> dict:
    metrics = get_system_metrics()
    return {"metrics": metrics, "prediction": predict_load(metrics)}
