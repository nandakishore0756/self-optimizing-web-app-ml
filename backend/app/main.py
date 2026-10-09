from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard import router as dashboard_router
from app.api.load_test import router as load_test_router
from app.api.metrics import router as metrics_router
from app.api.optimization import router as optimization_router
from app.api.prediction import router as prediction_router
from app.api.simulation import router as simulation_router
from app.config import cors_origin_list, settings
from app.database.database import init_db
from app.ml.predict import get_model
from app.monitoring.request_monitor import request_monitor

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="ML-powered self-optimizing web application demo: MONITOR → PREDICT → OPTIMIZE → RECOVER.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origin_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_metrics_middleware(request: Request, call_next):
    started = request_monitor.start_request()
    try:
        return await call_next(request)
    finally:
        request_monitor.end_request(started)

@app.on_event("startup")
def startup() -> None:
    init_db()
    get_model()

@app.get("/")
def root() -> dict:
    return {"name": settings.app_name, "version": settings.app_version, "status": "running", "docs": "/docs"}

@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "service": "autotune-backend"}

app.include_router(dashboard_router, prefix="/api")
app.include_router(metrics_router, prefix="/api")
app.include_router(prediction_router, prefix="/api")
app.include_router(optimization_router, prefix="/api")
app.include_router(simulation_router, prefix="/api")
app.include_router(load_test_router, prefix="/api")
