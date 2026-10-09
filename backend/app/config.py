from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    app_name: str = "AutoTune"
    app_version: str = "1.0.0"
    debug: bool = True
    database_url: str = f"sqlite:///{BASE_DIR / 'autotune.db'}"
    model_path: str = str(BASE_DIR / "app" / "ml" / "model.joblib")
    dataset_path: str = str(BASE_DIR / "datasets" / "performance_data.csv")
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()

def cors_origin_list() -> list[str]:
    return [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
