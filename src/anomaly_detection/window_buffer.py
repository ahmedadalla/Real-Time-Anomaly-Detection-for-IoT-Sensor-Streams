from collections import deque
from typing import Deque


class WindowBuffer:
    def __init__(self, window_size: int) -> None:
        self.window_size = window_size
        self._readings: Deque[dict[str, float]] = deque(maxlen=window_size)

    def append(self, reading: dict[str, float]) -> bool:
        self._readings.append(reading)
        return self.ready

    @property
    def ready(self) -> bool:
        return len(self._readings) == self.window_size

    @property
    def count(self) -> int:
        return len(self._readings)

    def current_window(self) -> list[dict[str, float]]:
        return list(self._readings)

