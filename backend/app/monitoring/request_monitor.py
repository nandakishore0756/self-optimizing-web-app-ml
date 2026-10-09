from collections import deque
from threading import Lock
from time import perf_counter, time

class RequestMonitor:
    def __init__(self) -> None:
        self._lock = Lock()
        self.total_requests = 0
        self.active_requests = 0
        self._recent_requests = deque(maxlen=5000)
        self._recent_latencies = deque(maxlen=5000)

    def start_request(self) -> float:
        with self._lock:
            self.active_requests += 1
        return perf_counter()

    def end_request(self, started_at: float) -> None:
        elapsed_ms = (perf_counter() - started_at) * 1000
        now = time()
        with self._lock:
            self.active_requests = max(0, self.active_requests - 1)
            self.total_requests += 1
            self._recent_requests.append(now)
            self._recent_latencies.append(elapsed_ms)

    def snapshot(self, window_seconds: float = 10.0) -> dict:
        cutoff = time() - window_seconds
        with self._lock:
            while self._recent_requests and self._recent_requests[0] < cutoff:
                self._recent_requests.popleft()
            request_count = len(self._recent_requests)
            traffic_rps = request_count / window_seconds
            latencies = list(self._recent_latencies)
            avg_latency = sum(latencies[-request_count:]) / request_count if request_count and len(latencies) >= request_count else (sum(latencies) / len(latencies) if latencies else 0.0)
            return {
                "traffic_rps": round(traffic_rps, 2),
                "active_requests": self.active_requests,
                "average_latency_ms": round(avg_latency, 2),
                "total_requests": self.total_requests,
            }

request_monitor = RequestMonitor()
