from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SensorReading:
    timestamp: datetime
    equipment_id: str
    sensor_id: str
    sensor_type: str
    value: float
    state: str
    quality: str
