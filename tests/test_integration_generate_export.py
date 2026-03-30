import csv
import json

from stf_hs.cli import main


def test_cli_generate_exports_csv(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    output_path = tmp_path / "generated.csv"

    config_path.write_text(
        json.dumps(
            {
                "equipment_id": "ROVER-01",
                "start_time": "2026-03-29T00:00:00Z",
                "duration_seconds": 60,
                "interval_seconds": 10,
                "seed": 123,
                "temperature_sensor": {
                    "sensor_id": "temp-qa",
                    "initial_celsius": 24.0,
                    "trend_per_step": 0.5,
                    "noise_stddev": 0.0,
                    "delay_seconds": 0,
                },
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(
        [
            "generate",
            "--config",
            str(config_path),
            "--output",
            str(output_path),
        ]
    )
    assert exit_code == 0
    assert output_path.exists()

    with output_path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 7
    assert rows[0]["timestamp"] == "2026-03-29T00:00:00Z"
    assert rows[-1]["timestamp"] == "2026-03-29T00:01:00Z"
    assert rows[0]["sensor_type"] == "temperature"
    assert rows[0]["quality"] in {"GOOD", "BAD"}
