from __future__ import annotations

import csv
import json
from collections import deque
from pathlib import Path
from threading import Lock

from .inference import PredictionResult
from .paths import PREDICTIONS_CSV_PATH, READINGS_CSV_PATH


class CSVStore:
    def __init__(
        self,
        readings_path: Path = READINGS_CSV_PATH,
        predictions_path: Path = PREDICTIONS_CSV_PATH,
        cache_size: int = 50,
    ) -> None:
        self.readings_path = readings_path
        self.predictions_path = predictions_path
        self.cache: deque[dict[str, object]] = deque(maxlen=cache_size)
        self._lock = Lock()
        self.readings_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_files()
        self._warm_cache()

    def _ensure_files(self) -> None:
        if not self.readings_path.exists():
            with self.readings_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["timestamp", "payload_json"])
                writer.writeheader()
        if not self.predictions_path.exists():
            with self.predictions_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["timestamp", "anomaly_score", "anomaly_label", "model_name"],
                )
                writer.writeheader()

    def _warm_cache(self) -> None:
        with self.predictions_path.open("r", newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        for row in rows[-(self.cache.maxlen or 0) :]:
            self.cache.append(
                {
                    "timestamp": row["timestamp"],
                    "anomaly_score": float(row["anomaly_score"]),
                    "anomaly_label": int(row["anomaly_label"]),
                    "model_name": row["model_name"],
                }
            )

    def save_reading(self, timestamp: str, reading: dict[str, float]) -> None:
        with self._lock, self.readings_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["timestamp", "payload_json"])
            writer.writerow({"timestamp": timestamp, "payload_json": json.dumps(reading, sort_keys=True)})

    def save_prediction(self, result: PredictionResult) -> dict[str, object]:
        item = {
            "timestamp": result.timestamp,
            "anomaly_score": result.anomaly_score,
            "anomaly_label": result.anomaly_label,
            "model_name": result.model_name,
        }
        with self._lock, self.predictions_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["timestamp", "anomaly_score", "anomaly_label", "model_name"],
            )
            writer.writerow(item)
            self.cache.append(item)
        return item

    def recent_predictions(self, limit: int = 20) -> list[dict[str, object]]:
        limit = max(1, min(limit, self.cache.maxlen or limit))
        return list(self.cache)[-limit:][::-1]

