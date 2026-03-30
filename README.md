<p align="center">
  <img src="assets/stf-hs-logo.svg" alt="STF-HS Logo" width="860" />
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="SimPy" src="https://img.shields.io/badge/SimPy-Event%20Simulation-00A3FF?style=for-the-badge&logo=databricks&logoColor=white" />
  <img alt="Pytest" src="https://img.shields.io/badge/Pytest-Tested-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
  <img alt="CLI" src="https://img.shields.io/badge/CLI-Ready-1B8A5A?style=for-the-badge&logo=gnubash&logoColor=white" />
</p>

<p align="center">
  <strong>Smart Test Factory - Hardware Simulation</strong><br/>
  Config-driven QA data generation for software-hardware lab workflows.
</p>

---

## Overview

`STF-HS` generates realistic, reproducible sensor datasets for regression and integration testing.  
It replaces manual spreadsheet/ad-hoc data preparation with a deterministic simulation pipeline that can run in CI or local validation.

Core value:

- Standardized simulation scenarios
- Faster regression setup
- Reproducible results across engineers and environments
- Clear, testable pipeline from config to artifact

---

## Quick Navigation

- [Problem](#problem)
- [Solution](#solution)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [CLI Usage](#cli-usage)
- [Configuration Reference](#configuration-reference)
- [Output Contract](#output-contract)
- [Testing Strategy](#testing-strategy)
- [Roadmap](#roadmap)

---

## Problem

In software + hardware automation labs, test data is often:

- Manually created and inconsistent
- Difficult to model with realistic sensor behavior (trend, delay, noise)
- Hard to reproduce during regression cycles
- Not standardized across teams

These issues reduce release confidence and slow down issue triage.

---

## Solution

STF-HS provides a focused, production-like pipeline:

1. Read simulation config (`SimulationConfig`)
2. Build sensor simulator (`TemperatureSensor`)
3. Run time-based orchestration (`EquipmentSimulator` with SimPy)
4. Normalize portable rows
5. Export CSV artifact
6. Execute using CLI for CI/manual workflows

---

## Architecture

```text
Config JSON
   |
   v
Sensor Builder
   |
   v
EquipmentSimulator (time/event)
   |
   v
SensorReadings
   |
   v
Row Normalizer
   |
   v
CSV Exporter
   |
   v
CLI Summary
```

### Engineering choices

| Decision | Why it matters |
|---|---|
| Python + SimPy | Fast delivery for event/time simulation |
| Config-driven design | Scale scenarios without touching core orchestration |
| Deterministic seed | Stable regression comparisons |
| CSV output | Easy interoperability with QA ecosystems |
| Integration-first coverage | Validates end-to-end release-critical flow |

---

## Project Structure

```text
.
├── assets/
│   └── stf-hs-logo.svg
├── examples/
│   └── simulation_config.json
├── outputs/
│   └── simulation_run.csv
├── stf_hs/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── exporter.py
│   ├── generator.py
│   ├── models.py
│   ├── normalizer.py
│   ├── simulator.py
│   └── sensors/
│       ├── __init__.py
│       └── temperature.py
├── tests/
│   ├── test_config.py
│   ├── test_integration_generate_export.py
│   └── test_temperature_sensor.py
├── project_brief.md
├── pyproject.toml
└── README.md
```

---

## Getting Started

### Prerequisites

- Python `>=3.10`

### Install

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

### Run test suite

```bash
.venv/bin/pytest -v
```

### Generate dataset

```bash
.venv/bin/python -m stf_hs.cli generate \
  --config examples/simulation_config.json \
  --output outputs/simulation_run.csv
```

Expected output:

```text
generated_rows=<N> output=outputs/simulation_run.csv
```

---

## CLI Usage

```bash
python -m stf_hs.cli generate --config <config.json> --output <output.csv>
```

Arguments:

- `--config`: path to simulation config JSON
- `--output`: path to generated CSV

---

## Configuration Reference

Sample config: `examples/simulation_config.json`

| Field | Type | Description |
|---|---|---|
| `equipment_id` | string | Equipment identifier |
| `start_time` | string (ISO-8601 UTC) | Simulation start timestamp |
| `duration_seconds` | int | Total simulation duration |
| `interval_seconds` | int | Sampling interval |
| `seed` | int | Random seed for deterministic runs |
| `temperature_sensor.*` | object | Temperature simulator parameters |

Temperature parameters:

- `sensor_id`
- `initial_celsius`
- `trend_per_step`
- `noise_stddev`
- `min_celsius`
- `max_celsius`
- `delay_seconds`
- `state_low_celsius`
- `state_high_celsius`
- `quality_min_celsius`
- `quality_max_celsius`

Validation rules:

- `duration_seconds > 0`
- `interval_seconds > 0`
- `duration_seconds % interval_seconds == 0`
- Temperature ranges must be valid (`min < max`)
- State and quality threshold ranges must be valid

---

## Output Contract

CSV schema:

| Column | Type | Description |
|---|---|---|
| `timestamp` | string | ISO-8601 UTC timestamp |
| `equipment_id` | string | Equipment identifier |
| `sensor_id` | string | Sensor identifier |
| `sensor_type` | string | Sensor category (`temperature`) |
| `value` | float | Simulated sensor value |
| `state` | string | `WARMUP`, `LOW`, `STABLE`, `HIGH` |
| `quality` | string | `GOOD`, `BAD` |

Example row:

```csv
timestamp,equipment_id,sensor_id,sensor_type,value,state,quality
2026-03-29T00:00:20Z,ROCKMAKER-01,temp-chamber-a,temperature,24.764,STABLE,GOOD
```

---

## Testing Strategy

### Unit tests

- Config validation and boundary checks
- Temperature sensor behavior (`delay`, `state`, `quality`)

### Integration tests

- End-to-end CLI generation flow
- CSV existence, schema, row count, and timestamp boundaries

Run all tests:

```bash
.venv/bin/pytest -v
```

---

## Roadmap

1. Add `PressureSensor`
2. Add controlled failure injection (`stuck`, `spike`, `dropout`)
3. Add statistical trend checks for output verification
4. Add JSON summary report for quick triage

---

## License

Internal portfolio project for QA Automation / SDET hiring demonstration.
