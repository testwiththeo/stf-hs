from __future__ import annotations

from stf_hs.models import SensorReading


def normalize_reading(reading: SensorReading) -> dict[str, str | float]:
    return {
        "timestamp": reading.timestamp.isoformat().replace("+00:00", "Z"),
        "equipment_id": reading.equipment_id,
        "sensor_id": reading.sensor_id,
        "sensor_type": reading.sensor_type,
        "value": reading.value,
        "state": reading.state,
        "quality": reading.quality,
    }


def normalize_readings(readings: list[SensorReading]) -> list[dict[str, str | float]]:
    return [normalize_reading(reading) for reading in readings]
