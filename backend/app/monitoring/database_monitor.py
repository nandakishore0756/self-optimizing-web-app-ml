from time import perf_counter
from sqlalchemy import text
from app.database.database import SessionLocal

def measure_database_query_time() -> float:
    started = perf_counter()
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    finally:
        db.close()
    return round((perf_counter() - started) * 1000, 2)
