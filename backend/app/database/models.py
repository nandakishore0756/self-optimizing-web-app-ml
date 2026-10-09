from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

class MetricsRecord(Base):
    __tablename__ = "metrics"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    traffic_rps: Mapped[float] = mapped_column(Float, default=0.0)
    response_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    cpu_percent: Mapped[float] = mapped_column(Float, default=0.0)
    memory_percent: Mapped[float] = mapped_column(Float, default=0.0)
    database_query_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    active_users: Mapped[int] = mapped_column(Integer, default=0)
    system_load: Mapped[float] = mapped_column(Float, default=0.0)
    simulation_mode: Mapped[str] = mapped_column(String(32), default="normal")
    prediction_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    prediction_status: Mapped[str | None] = mapped_column(String(32), nullable=True)

class OptimizationEvent(Base):
    __tablename__ = "optimization_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    event_type: Mapped[str] = mapped_column(String(32))
    action: Mapped[str] = mapped_column(String(128))
    reason: Mapped[str] = mapped_column(Text)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
