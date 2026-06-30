from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import torch
from torch import nn

from .paths import SCALER_PATH, USAD_WEIGHTS_PATH


USAD_THRESHOLD = 0.0014934739


class Encoder(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 128) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(True),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(True),
            nn.Linear(hidden_dim // 2, hidden_dim // 4),
            nn.ReLU(True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class Decoder(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 128) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(hidden_dim // 4, hidden_dim // 2),
            nn.ReLU(True),
            nn.Linear(hidden_dim // 2, hidden_dim),
            nn.ReLU(True),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid(),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.net(z)


class USAD(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 128) -> None:
        super().__init__()
        self.encoder = Encoder(input_dim=input_dim, hidden_dim=hidden_dim)
        self.decoder1 = Decoder(input_dim=input_dim, hidden_dim=hidden_dim)
        self.decoder2 = Decoder(input_dim=input_dim, hidden_dim=hidden_dim)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        z = self.encoder(x)
        w1 = self.decoder1(z)
        w2 = self.decoder2(z)
        z2 = self.encoder(w1)
        w3 = self.decoder2(z2)
        return w1, w2, w3


class USADRuntime:
    def __init__(self, model: USAD, threshold: float = USAD_THRESHOLD) -> None:
        self.model = model
        self.threshold = threshold
        self.name = "USAD"

    def score(self, flattened_window: Any) -> float:
        tensor = torch.as_tensor(flattened_window, dtype=torch.float32)
        self.model.eval()
        with torch.no_grad():
            w1, _, w3 = self.model(tensor)
            error1 = torch.mean((tensor - w1) ** 2, dim=1)
            error2 = torch.mean((tensor - w3) ** 2, dim=1)
            score = 0.7 * error1 + 0.3 * error2
        return float(score.cpu().numpy()[0])

    def predict(self, flattened_window: Any) -> int:
        return int(self.score(flattened_window) > self.threshold)


@lru_cache(maxsize=1)
def load_scaler(path: Path = SCALER_PATH) -> Any:
    return joblib.load(path)


@lru_cache(maxsize=1)
def load_model(path: Path = USAD_WEIGHTS_PATH) -> USADRuntime:
    state_dict = torch.load(path, map_location=torch.device("cpu"))
    input_dim = int(state_dict["encoder.net.0.weight"].shape[1])
    model = USAD(input_dim=input_dim)
    model.load_state_dict(state_dict)
    model.eval()
    return USADRuntime(model)
