from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def extract_timestamp(payload: dict[str, Any]) -> str | None:
    timestamp = payload.get("timestamp")
    return str(timestamp) if timestamp is not None else None


def normalize_reading(payload: dict[str, Any], feature_columns: list[str]) -> dict[str, float]:
    values = payload.get("values")
    source = values if isinstance(values, dict) else payload

    missing = [feature for feature in feature_columns if feature not in source]
    if missing:
        preview = ", ".join(missing[:8])
        suffix = "..." if len(missing) > 8 else ""
        raise ValueError(f"Missing required sensor features: {preview}{suffix}")

    normalized: dict[str, float] = {}
    for feature in feature_columns:
        try:
            normalized[feature] = float(source[feature])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Feature {feature} must be numeric") from exc
    return normalized


def readings_to_frame(readings: list[dict[str, float]], feature_columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame(readings, columns=feature_columns)


def scaler_feature_columns(feature_columns: list[str], scaler: Any) -> list[str]:
    fitted_columns = getattr(scaler, "feature_names_in_", None)
    return list(fitted_columns) if fitted_columns is not None else feature_columns


def preprocess_window(
    readings: list[dict[str, float]],
    feature_columns: list[str],
    scaler: Any,
) -> np.ndarray:
    transform_columns = scaler_feature_columns(feature_columns, scaler)
    scaler_rows = []
    for reading in readings:
        row = dict(reading)
        if "label" in transform_columns and "label" not in row:
            row["label"] = 0.0
        scaler_rows.append(row)

    frame = readings_to_frame(scaler_rows, transform_columns)
    scaled = scaler.transform(frame)
    return scaled.reshape(1, len(readings), len(transform_columns))


def flatten_window(window: np.ndarray) -> np.ndarray:
    return window.reshape(window.shape[0], -1)
