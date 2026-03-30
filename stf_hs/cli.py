from __future__ import annotations

import argparse

from stf_hs.config import SimulationConfig
from stf_hs.exporter import CsvExporter
from stf_hs.generator import DataGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stf-hs",
        description="Smart Test Factory - Hardware Simulation CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate simulated sensor CSV data.")
    generate_parser.add_argument("--config", required=True, help="Path to simulation config JSON.")
    generate_parser.add_argument("--output", required=True, help="Path to output CSV file.")

    return parser


def cmd_generate(config_path: str, output_path: str) -> int:
    config = SimulationConfig.from_json_file(config_path)
    generator = DataGenerator(config)
    rows = generator.generate_rows()

    exporter = CsvExporter()
    path = exporter.export(rows=rows, output_path=output_path)
    print(f"generated_rows={len(rows)} output={path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        return cmd_generate(config_path=args.config, output_path=args.output)

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
