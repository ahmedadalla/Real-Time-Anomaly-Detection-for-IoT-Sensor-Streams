from __future__ import annotations

import argparse
import csv
import random
import time
from datetime import UTC, datetime
from pathlib import Path

import requests

from .config import load_runtime_config
from .paths import NORMAL_DATA_PATH


BASELINES = {
    "FIT": (1.5, 0.6),
    "LIT": (500.0, 120.0),
    "AIT": (180.0, 55.0),
    "PIT": (80.0, 40.0),
    "DPIT": (20.0, 2.0),
    "MV": (1.0, 0.6),
    "P": (1.0, 0.45),
    "UV": (1.0, 0.3),
}


def _profile_for_feature(name: str) -> tuple[float, float]:
    for prefix, profile in BASELINES.items():
        if name.startswith(prefix):
            return profile
    return 1.0, 0.25


def generate_reading(feature_columns: list[str], abnormal: bool = False) -> dict[str, float]:
    reading: dict[str, float] = {}
    for feature in feature_columns:
        mean, spread = _profile_for_feature(feature)
        value = random.gauss(mean, spread)
        if feature.startswith(("MV", "P", "UV")):
            value = round(max(0.0, min(2.0, value)))
        else:
            value = max(0.0, value)
        reading[feature] = float(value)

    if abnormal:
        affected = random.sample(feature_columns, k=min(4, len(feature_columns)))
        for feature in affected:
            mean, spread = _profile_for_feature(feature)
            reading[feature] = max(0.0, mean + random.choice([-1, 1]) * spread * random.uniform(6.0, 10.0))
    return reading


def inject_anomaly(reading: dict[str, float], feature_columns: list[str]) -> dict[str, float]:
    anomalous = dict(reading)
    affected = random.sample(feature_columns, k=min(4, len(feature_columns)))
    for feature in affected:
        value = anomalous[feature]
        if feature.startswith(("MV", "P", "UV")):
            anomalous[feature] = 2.0 if value < 1.0 else 0.0
        elif value == 0:
            anomalous[feature] = random.uniform(50.0, 500.0)
        else:
            anomalous[feature] = max(0.0, value * random.uniform(2.5, 6.0))
    return anomalous


def iter_csv_readings(csv_path: Path, feature_columns: list[str], skip_rows: int = 0):
    while True:
        with csv_path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for _ in range(skip_rows):
                next(reader, None)
            for row in reader:
                yield {feature: float(row[feature]) for feature in feature_columns}


def run_simulator(
    api_url: str,
    interval: float,
    anomaly_every: int | None,
    data_path: Path = NORMAL_DATA_PATH,
    use_csv_data: bool = True,
    skip_rows: int | None = None,
) -> None:
    config = load_runtime_config()
    sensor_url = api_url.rstrip("/") + "/sensor"
    if skip_rows is None:
        skip_rows = int(config.stabilization_hours * 3600)
    readings = iter_csv_readings(data_path, config.feature_columns, skip_rows=skip_rows) if use_csv_data else None
    count = 0
    while True:
        count += 1
        abnormal = bool(anomaly_every and count % anomaly_every == 0)
        if readings is None:
            reading = generate_reading(config.feature_columns, abnormal=abnormal)
        else:
            reading = next(readings)
            if abnormal:
                reading = inject_anomaly(reading, config.feature_columns)

        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "values": reading,
        }
        response = requests.post(sensor_url, json=payload, timeout=10)
        response.raise_for_status()
        prediction = response.json().get("prediction")
        if prediction:
            label = prediction["anomaly_label"]
            score = prediction["anomaly_score"]
            print(f"window={count} anomaly_label={label} anomaly_score={score:.6f}")
        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send simulated IoT readings to the FastAPI backend.")
    parser.add_argument("--api-url", default="http://127.0.0.1:8000")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--anomaly-every", type=int, default=25)
    parser.add_argument("--data-path", type=Path, default=NORMAL_DATA_PATH)
    parser.add_argument(
        "--skip-rows",
        type=int,
        default=None,
        help="Rows to skip before replaying CSV data. Defaults to stabilization_hours * 3600.",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Use synthetic random readings instead of replaying Data/raw_data/normal_data.csv.",
    )
    args = parser.parse_args()
    run_simulator(
        args.api_url,
        args.interval,
        args.anomaly_every,
        data_path=args.data_path,
        use_csv_data=not args.random,
        skip_rows=args.skip_rows,
    )


if __name__ == "__main__":
    main()
