from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _parse_iso8601_utc(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class TemperatureSensorConfig:
    sensor_id: str = "temperature-main"
    initial_celsius: float = 25.0
    trend_per_step: float = 0.0
    noise_stddev: float = 0.2
    min_celsius: float = 15.0
    max_celsius: float = 40.0
    delay_seconds: int = 0
    state_low_celsius: float = 22.0
    state_high_celsius: float = 30.0
    quality_min_celsius: float = 18.0
    quality_max_celsius: float = 35.0

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TemperatureSensorConfig":
        config = cls(
            sensor_id=str(payload.get("sensor_id", "temperature-main")),
            initial_celsius=float(payload.get("initial_celsius", 25.0)),
            trend_per_step=float(payload.get("trend_per_step", 0.0)),
            noise_stddev=float(payload.get("noise_stddev", 0.2)),
            min_celsius=float(payload.get("min_celsius", 15.0)),
            max_celsius=float(payload.get("max_celsius", 40.0)),
            delay_seconds=int(payload.get("delay_seconds", 0)),
            state_low_celsius=float(payload.get("state_low_celsius", 22.0)),
            state_high_celsius=float(payload.get("state_high_celsius", 30.0)),
            quality_min_celsius=float(payload.get("quality_min_celsius", 18.0)),
            quality_max_celsius=float(payload.get("quality_max_celsius", 35.0)),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not self.sensor_id.strip():
            raise ValueError("temperature_sensor.sensor_id cannot be empty")
        if self.noise_stddev < 0:
            raise ValueError("temperature_sensor.noise_stddev must be >= 0")
        if self.min_celsius >= self.max_celsius:
            raise ValueError("temperature_sensor min/max range is invalid")
        if self.delay_seconds < 0:
            raise ValueError("temperature_sensor.delay_seconds must be >= 0")
        if self.state_low_celsius >= self.state_high_celsius:
            raise ValueError("temperature_sensor state range is invalid")
        if self.quality_min_celsius >= self.quality_max_celsius:
            raise ValueError("temperature_sensor quality range is invalid")


@dataclass(frozen=True)
class SimulationConfig:
    equipment_id: str
    start_time: datetime
    duration_seconds: int
    interval_seconds: int
    seed: int
    temperature_sensor: TemperatureSensorConfig

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SimulationConfig":
        temperature_payload = payload.get("temperature_sensor", {})
        config = cls(
            equipment_id=str(payload.get("equipment_id", "equipment-1")),
            start_time=_parse_iso8601_utc(payload.get("start_time", "2026-01-01T00:00:00Z")),
            duration_seconds=int(payload["duration_seconds"]),
            interval_seconds=int(payload["interval_seconds"]),
            seed=int(payload.get("seed", 42)),
            temperature_sensor=TemperatureSensorConfig.from_dict(temperature_payload),
        )
        config.validate()
        return config

    @classmethod
    def from_json_file(cls, path: str | Path) -> "SimulationConfig":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)

    def validate(self) -> None:
        if not self.equipment_id.strip():
            raise ValueError("equipment_id cannot be empty")
        if self.duration_seconds <= 0:
            raise ValueError("duration_seconds must be > 0")
        if self.interval_seconds <= 0:
            raise ValueError("interval_seconds must be > 0")
        if self.interval_seconds > self.duration_seconds:
            raise ValueError("interval_seconds must be <= duration_seconds")
        if self.duration_seconds % self.interval_seconds != 0:
            raise ValueError("duration_seconds must be divisible by interval_seconds")
