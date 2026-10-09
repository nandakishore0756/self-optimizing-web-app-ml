from dataclasses import dataclass
from threading import Lock

@dataclass
class SimulationState:
    mode: str = "normal"
    multiplier: float = 1.0

class SimulationMonitor:
    def __init__(self) -> None:
        self._state = SimulationState()
        self._lock = Lock()

    def set_high_load(self) -> SimulationState:
        with self._lock:
            self._state = SimulationState("high-load", 3.2)
            return self._state

    def set_normal(self) -> SimulationState:
        with self._lock:
            self._state = SimulationState("normal", 1.0)
            return self._state

    def snapshot(self) -> SimulationState:
        with self._lock:
            return SimulationState(self._state.mode, self._state.multiplier)

simulation_monitor = SimulationMonitor()
