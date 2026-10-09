import math
import time
from fastapi import APIRouter

router = APIRouter(prefix="/load-test", tags=["demo"])

@router.get("/work")
def work(iterations: int = 50000) -> dict:
    iterations = max(1000, min(iterations, 250000))
    started = time.perf_counter()
    value = sum(math.sqrt(number * number) for number in range(iterations))
    elapsed_ms = (time.perf_counter() - started) * 1000
    return {"iterations": iterations, "elapsed_ms": round(elapsed_ms, 2), "result": round(value, 2)}
