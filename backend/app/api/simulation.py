from fastapi import APIRouter
from app.monitoring.simulation_monitor import simulation_monitor

router = APIRouter(prefix="/simulation", tags=["simulation"])

@router.get("/status")
def simulation_status() -> dict:
    state = simulation_monitor.snapshot()
    return {"mode": state.mode, "multiplier": state.multiplier}

@router.post("/high-load")
def simulate_high_load() -> dict:
    state = simulation_monitor.set_high_load()
    return {"message": "High-load simulation enabled.", "mode": state.mode, "multiplier": state.multiplier}

@router.post("/normal")
def simulate_normal() -> dict:
    state = simulation_monitor.set_normal()
    return {"message": "Normal operating mode restored.", "mode": state.mode, "multiplier": state.multiplier}
