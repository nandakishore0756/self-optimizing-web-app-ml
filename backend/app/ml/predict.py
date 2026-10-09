from pathlib import Path
import joblib
from app.config import settings
from app.ml.preprocess import build_feature_row
from app.ml.train import train_and_save

_model = None

def get_model():
    global _model
    if _model is None:
        path = Path(settings.model_path)
        if not path.exists():
            train_and_save()
        _model = joblib.load(path)
    return _model

def predict_load(metrics: dict) -> dict:
    model = get_model()
    row = [build_feature_row(metrics)]
    probability = float(model.predict_proba(row)[0][1])
    status = "HIGH_LOAD" if probability >= 0.50 else "NORMAL"
    confidence = probability if status == "HIGH_LOAD" else 1.0 - probability
    reasons = []
    if metrics["cpu_percent"] >= 75: reasons.append("high CPU utilization")
    if metrics["memory_percent"] >= 80: reasons.append("high memory utilization")
    if metrics["response_time_ms"] >= 250: reasons.append("elevated response time")
    if metrics["database_query_time_ms"] >= 100: reasons.append("slow database queries")
    if metrics["traffic_rps"] >= 400: reasons.append("high traffic volume")
    return {
        "probability": round(probability, 4),
        "confidence": round(confidence, 4),
        "status": status,
        "reason": ", ".join(reasons) if reasons else "performance metrics are within the normal operating range",
    }
