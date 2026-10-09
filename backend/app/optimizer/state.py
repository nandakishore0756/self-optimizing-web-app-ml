from copy import deepcopy
from dataclasses import asdict, dataclass
from threading import Lock

@dataclass
class OptimizationState:
    optimized: bool = False
    caching_enabled: bool = False
    db_query_optimization: bool = False
    db_pagination_limit: int = 50
    heavy_components_enabled: bool = True
    last_reason: str = "System is operating normally."

class StateManager:
    def __init__(self) -> None:
        self._lock = Lock()
        self._state = OptimizationState()

    def snapshot(self) -> dict:
        with self._lock:
            return deepcopy(asdict(self._state))

    def optimize(self, reason: str) -> dict:
        with self._lock:
            self._state.optimized = True
            self._state.caching_enabled = True
            self._state.db_query_optimization = True
            self._state.db_pagination_limit = 20
            self._state.heavy_components_enabled = False
            self._state.last_reason = reason
            return deepcopy(asdict(self._state))

    def recover(self, reason: str) -> dict:
        with self._lock:
            self._state = OptimizationState(
                last_reason=reason
            )
            return deepcopy(asdict(self._state))

state_manager = StateManager()
