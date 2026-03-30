from __future__ import annotations

import csv
from pathlib import Path


class CsvExporter:
    fieldnames = [
        "timestamp",
        "equipment_id",
        "sensor_id",
        "sensor_type",
        "value",
        "state",
        "quality",
    ]

    def export(self, rows: list[dict[str, str | float]], output_path: str | Path) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        return path
