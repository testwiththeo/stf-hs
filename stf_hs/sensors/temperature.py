from __future__ import annotations

import math
import random
from collections import deque
from datetime import datetime
from typing import Deque

from stf_hs.config import TemperatureSensorConfig
from stf_hs.models import SensorReading


class TemperatureSensor:
    sensor_type = "temperature"

    def __init__(self, config: TemperatureSensorConfig, rng: random.Random) -> None:
        self.config = config
        self._rng = rng
        self._true_value = config.initial_celsius
        self._delay_steps = 0
        self._delay_buffer: Deque[float] = deque()

    @property
    def sensor_id(self) -> str:
        return self.config.sensor_id

    def configure_timing(self, interval_seconds: int) -> None:
        if self.config.delay_seconds == 0:
            self._delay_steps = 0
            self._delay_buffer = deque()
            return

        self._delay_steps = math.ceil(self.config.delay_seconds / interval_seconds)
        self._delay_buffer = deque([self.config.initial_celsius] * self._delay_steps)

    def read(
        self,
        *,
        step: int,
        elapsed_seconds: int,
        timestamp: datetime,
        equipment_id: str,
    ) -> SensorReading:
        drifted_value = self._true_value + self.config.trend_per_step
        noisy_value = drifted_value + self._rng.gauss(0, self.config.noise_stddev)
        self._true_value = self._clamp(noisy_value, self.config.min_celsius, self.config.max_celsius)
        measured_value = self._apply_delay(self._true_value)

        return SensorReading(
            timestamp=timestamp,
            equipment_id=equipment_id,
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=round(measured_value, 3),
            state=self._derive_state(step=step, value=measured_value, elapsed_seconds=elapsed_seconds),
            quality=self._derive_quality(measured_value),
        )

    def _apply_delay(self, newest_value: float) -> float:
        if self._delay_steps == 0:
            return newest_value

        self._delay_buffer.append(newest_value)
        return self._delay_buffer.popleft()

    def _derive_state(self, *, step: int, value: float, elapsed_seconds: int) -> str:
        if self._delay_steps > 0 and step < self._delay_steps:
            return "WARMUP"
        if value < self.config.state_low_celsius:
            return "LOW"
        if value > self.config.state_high_celsius:
            return "HIGH"
        return "STABLE"

    def _derive_quality(self, value: float) -> str:
        in_quality_window = self.config.quality_min_celsius <= value <= self.config.quality_max_celsius
        return "GOOD" if in_quality_window else "BAD"

    @staticmethod
    def _clamp(value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(max_value, value))
