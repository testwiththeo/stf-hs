from __future__ import annotations

import random

from stf_hs.config import SimulationConfig
from stf_hs.models import SensorReading
from stf_hs.normalizer import normalize_readings
from stf_hs.sensors.temperature import TemperatureSensor
from stf_hs.simulator import EquipmentSimulator


class DataGenerator:
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config

    def generate_readings(self) -> list[SensorReading]:
        rng = random.Random(self.config.seed)
        sensors = [
            TemperatureSensor(config=self.config.temperature_sensor, rng=rng),
        ]
        simulator = EquipmentSimulator(config=self.config, sensors=sensors)
        return simulator.run()

    def generate_rows(self) -> list[dict[str, str | float]]:
        readings = self.generate_readings()
        return normalize_readings(readings)
