from datetime import datetime, timedelta, timezone
import random

from stf_hs.config import TemperatureSensorConfig
from stf_hs.sensors.temperature import TemperatureSensor


def test_temperature_sensor_delay_state_and_quality() -> None:
    config = TemperatureSensorConfig(
        sensor_id="temp-01",
        initial_celsius=25.0,
        trend_per_step=1.0,
        noise_stddev=0.0,
        min_celsius=10.0,
        max_celsius=100.0,
        delay_seconds=10,
        state_low_celsius=24.0,
        state_high_celsius=26.0,
        quality_min_celsius=20.0,
        quality_max_celsius=26.0,
    )
    sensor = TemperatureSensor(config=config, rng=random.Random(11))
    sensor.configure_timing(interval_seconds=5)

    start = datetime(2026, 3, 29, tzinfo=timezone.utc)
    readings = []
    for step in range(4):
        readings.append(
            sensor.read(
                step=step,
                elapsed_seconds=step * 5,
                timestamp=start + timedelta(seconds=step * 5),
                equipment_id="STACK-01",
            )
        )

    assert [item.state for item in readings] == ["WARMUP", "WARMUP", "STABLE", "HIGH"]
    assert [item.quality for item in readings] == ["GOOD", "GOOD", "GOOD", "BAD"]
    assert [item.value for item in readings] == [25.0, 25.0, 26.0, 27.0]
