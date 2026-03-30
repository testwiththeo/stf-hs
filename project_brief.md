# STF-HS Project Brief
**Smart Test Data Factory with Hardware Simulation**

---

## 1) Project Overview

### Bahasa Indonesia
STF-HS adalah proyek QA automation untuk menghasilkan data uji sensor yang realistis menggunakan simulasi berbasis waktu.  
Tujuan utamanya adalah mengurangi ketergantungan pada pembuatan data uji manual yang lambat, tidak konsisten, dan sulit direproduksi.

### English
STF-HS is a QA automation project that generates realistic sensor test data using time-based simulation.  
Its core goal is to reduce dependency on manual test data creation, which is slow, inconsistent, and hard to reproduce.

---

## 2) Problem Statement

### Bahasa Indonesia
Dalam konteks software + hardware lab automation:
- Test data sering dibuat manual (spreadsheet/script ad-hoc).
- Sulit mensimulasikan perilaku sensor yang realistis (noise, delay, trend).
- Regression testing jadi lambat karena skenario tidak terstandardisasi.
- Sulit menjamin reproducibility antar engineer/team.

### English
In software + hardware lab automation contexts:
- Test data is often manually created (spreadsheets/ad-hoc scripts).
- It is hard to simulate realistic sensor behavior (noise, delay, trend).
- Regression testing becomes slow due to non-standardized scenarios.
- Reproducibility across engineers/teams is difficult.

---

## 3) Proposed Solution

### Bahasa Indonesia
Membangun pipeline sederhana namun scalable:
1. Baca konfigurasi simulasi (`SimulationConfig`).
2. Bangun sensor simulator (MVP: temperature).
3. Jalankan orchestrator simulasi berbasis event/time (`EquipmentSimulator` + SimPy).
4. Normalisasi output data.
5. Ekspor hasil ke CSV.
6. Jalankan lewat CLI untuk kemudahan penggunaan CI/manual.

### English
Build a simple yet scalable pipeline:
1. Read simulation config (`SimulationConfig`).
2. Build sensor simulators (MVP: temperature).
3. Run event/time-based simulation (`EquipmentSimulator` + SimPy).
4. Normalize output records.
5. Export output to CSV.
6. Execute via CLI for CI/manual usage.

---

## 4) MVP Scope

### Included
- `TemperatureSensor` simulator
- `EquipmentSimulator` orchestrator
- `DataGenerator` pipeline
- CSV exporter
- CLI command: generate from config
- Integration test (end-to-end generate + export)

### Not in MVP (future)
- Pressure/motion sensors
- Advanced failure injection
- Statistical validation layer (KS-test)
- Dashboard/UI
- Multi-format exporters beyond CSV

---

## 5) Architecture (MVP)

`Config -> Sensor Builder -> Simulator -> Row Normalizer -> CSV Export -> Report`

- **Config Layer**: validation input
- **Simulation Layer**: time-step based sensor updates
- **Generation Layer**: convert readings into portable rows
- **Export Layer**: write CSV for downstream QA workflows
- **CLI Layer**: user-friendly execution

---

## 6) Key Engineering Decisions

### Bahasa Indonesia
- **Python + SimPy**: cepat dibangun, cocok untuk discrete-event simulation.
- **Config-driven approach**: mudah scale skenario tanpa ubah core logic.
- **Simple exporter (CSV)**: interoperable dengan tools QA umum.
- **Integration test first**: memastikan alur utama benar dari awal.

### English
- **Python + SimPy**: fast to build, suitable for discrete-event simulation.
- **Config-driven approach**: easy to scale scenarios without changing core logic.
- **Simple exporter (CSV)**: interoperable with common QA tools.
- **Integration test first**: validates the main workflow early.

---

## 7) Hiring-Relevant Value (Formulatrix Context)

### Bahasa Indonesia
Proyek ini menunjukkan:
- Problem solving untuk domain automation + instrumentation.
- Kemampuan membangun QA tooling, bukan hanya menjalankan test case.
- Pemahaman reproducibility dan regression-readiness.
- Kemampuan membuat sistem sederhana yang punya dampak operasional nyata.

### English
This project demonstrates:
- Problem-solving in automation + instrumentation domains.
- Ability to build QA tooling, not only execute test cases.
- Understanding of reproducibility and regression readiness.
- Ability to create simple systems with real operational impact.

---

## 8) Success Criteria (MVP)

- CLI dapat generate file CSV dari config JSON.
- Data berisi timestamp + value + state + quality.
- Integration test pass.
- README/project brief dapat menjelaskan use case dan impact secara jelas.

---

## 9) Demo Script (for Recruiter / Interview)

```bash
poetry run pytest -v
poetry run python -m stf_hs.cli generate \
  --config examples/mvp_config.json \
  --output outputs/mvp.csv
