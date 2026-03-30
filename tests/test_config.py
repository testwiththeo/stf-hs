import pytest

from stf_hs.config import SimulationConfig


def test_simulation_config_valid_payload() -> None:
    config = SimulationConfig.from_dict(
        {
            "equipment_id": "NT8-01",
            "start_time": "2026-03-01T00:00:00Z",
            "duration_seconds": 60,
            "interval_seconds": 10,
            "seed": 7,
            "temperature_sensor": {"sensor_id": "temp-01"},
        }
    )

    assert config.equipment_id == "NT8-01"
    assert config.duration_seconds == 60
    assert config.interval_seconds == 10
    assert config.temperature_sensor.sensor_id == "temp-01"


def test_simulation_config_rejects_non_divisible_duration() -> None:
    with pytest.raises(ValueError, match="divisible"):
        SimulationConfig.from_dict(
            {
                "equipment_id": "NT8-01",
                "duration_seconds": 65,
                "interval_seconds": 10,
            }
        )
