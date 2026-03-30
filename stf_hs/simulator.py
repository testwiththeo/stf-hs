from __future__ import annotations

from datetime import timedelta
from typing import Protocol

import simpy

from stf_hs.config import SimulationConfig
from stf_hs.models import SensorReading


class Sensor(Protocol):
    sensor_id: str
    sensor_type: str

    def configure_timing(self, interval_seconds: int) -> None: ...

    def read(
        self,
        *,
        step: int,
        elapsed_seconds: int,
        timestamp,
        equipment_id: str,
    ) -> SensorReading: ...


class EquipmentSimulator:
    def __init__(self, config: SimulationConfig, sensors: list[Sensor]) -> None:
        self.config = config
        self.sensors = sensors
        self._env = simpy.Environment()
        self._readings: list[SensorReading] = []

        for sensor in self.sensors:
            sensor.configure_timing(self.config.interval_seconds)

    def run(self) -> list[SensorReading]:
        for sensor in self.sensors:
            self._env.process(self._run_sensor(sensor))

        self._env.run(until=self.config.duration_seconds + self.config.interval_seconds)
        self._readings.sort(key=lambda item: (item.timestamp, item.sensor_id))
        return self._readings

    def _run_sensor(self, sensor: Sensor):
        total_steps = (self.config.duration_seconds // self.config.interval_seconds) + 1
        for step in range(total_steps):
            elapsed_seconds = step * self.config.interval_seconds
            timestamp = self.config.start_time + timedelta(seconds=elapsed_seconds)
            reading = sensor.read(
                step=step,
                elapsed_seconds=elapsed_seconds,
                timestamp=timestamp,
                equipment_id=self.config.equipment_id,
            )
            self._readings.append(reading)

            if step < total_steps - 1:
                yield self._env.timeout(self.config.interval_seconds)
