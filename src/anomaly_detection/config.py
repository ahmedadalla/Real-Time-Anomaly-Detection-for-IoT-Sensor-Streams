import json
from dataclasses import dataclass
from pathlib import Path

from .paths import CONFIG_PATH, FEATURE_COLUMNS_PATH


@dataclass(frozen=True)
class RuntimeConfig:
    feature_columns: list[str]
    window_size: int
    step_size: int
    stabilization_hours: float


def load_runtime_config(
    config_path: Path = CONFIG_PATH,
    feature_columns_path: Path = FEATURE_COLUMNS_PATH,
) -> RuntimeConfig:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    feature_columns = json.loads(feature_columns_path.read_text(encoding="utf-8"))
    return RuntimeConfig(
        feature_columns=feature_columns,
        window_size=int(config["window_size"]),
        step_size=int(config.get("step_size", 1)),
        stabilization_hours=float(config.get("stabilization_hours", 0)),
    )
