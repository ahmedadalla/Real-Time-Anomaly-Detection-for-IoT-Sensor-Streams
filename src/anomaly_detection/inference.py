from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from .preprocessing import flatten_window, preprocess_window


@dataclass(frozen=True)
class PredictionResult:
    timestamp: str
    anomaly_score: float
    anomaly_label: int
    model_name: str


def predict_window(
    readings: list[dict[str, float]],
    feature_columns: list[str],
    scaler: Any,
    model: Any,
    timestamp: str | None = None,
) -> PredictionResult:
    window = preprocess_window(readings, feature_columns, scaler)
    flattened = flatten_window(window)

    if hasattr(model, "score") and getattr(model, "name", None) == "USAD":
        anomaly_score = float(model.score(flattened))
        anomaly_label = int(anomaly_score > model.threshold)
        model_name = model.name
    elif hasattr(model, "predict"):
        raw_label = int(model.predict(flattened)[0])
        anomaly_label = 1 if raw_label == -1 else raw_label
        if hasattr(model, "decision_function"):
            anomaly_score = float(-model.decision_function(flattened)[0])
        elif hasattr(model, "score_samples"):
            anomaly_score = float(-model.score_samples(flattened)[0])
        else:
            anomaly_score = float(anomaly_label)
        model_name = type(model).__name__
    else:
        raise TypeError("Loaded model does not expose a supported inference interface")

    return PredictionResult(
        timestamp=timestamp or datetime.now(UTC).isoformat(),
        anomaly_score=anomaly_score,
        anomaly_label=anomaly_label,
        model_name=model_name,
    )
