from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

from app.config import settings
from app.ml.preprocess import FEATURES

def generate_dataset(rows: int = 3000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    traffic = rng.uniform(5, 1000, rows)
    response = rng.uniform(25, 650, rows)
    cpu = rng.uniform(10, 98, rows)
    memory = rng.uniform(15, 98, rows)
    db_time = rng.uniform(2, 350, rows)
    active_users = rng.uniform(1, 1200, rows)
    system_load = rng.uniform(0.1, 16, rows)
    score = (
        0.25*(traffic/1000) + 0.20*(response/650) + 0.15*(cpu/100) +
        0.10*(memory/100) + 0.10*(db_time/350) + 0.10*(active_users/1200) +
        0.10*(system_load/16)
    )
    target = ((score + rng.normal(0, 0.035, rows)) >= 0.52).astype(int)
    return pd.DataFrame({
        "traffic_rps": traffic.round(2),
        "response_time_ms": response.round(2),
        "cpu_percent": cpu.round(2),
        "memory_percent": memory.round(2),
        "database_query_time_ms": db_time.round(2),
        "active_users": active_users.round(2),
        "system_load": system_load.round(2),
        "target": target,
    })

def train_and_save() -> dict:
    dataset = Path(settings.dataset_path)
    model_path = Path(settings.model_path)
    dataset.parent.mkdir(parents=True, exist_ok=True)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_dataset()
    df.to_csv(dataset, index=False)
    x_train, x_test, y_train, y_test = train_test_split(
        df[FEATURES], df["target"], test_size=0.20, random_state=42, stratify=df["target"]
    )
    model = RandomForestClassifier(
        n_estimators=180, max_depth=10, min_samples_leaf=3,
        class_weight="balanced", random_state=42, n_jobs=-1
    )
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= 0.50).astype(int)
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        "rows": int(len(df)),
    }
    joblib.dump(model, model_path)
    return metrics

if __name__ == "__main__":
    print(train_and_save())
