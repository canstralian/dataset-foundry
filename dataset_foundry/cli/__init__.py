"""Command-line interface for Dataset Foundry.

Provides the ``foundry`` command with subcommands for validating pipeline
configuration and running pipelines. Configuration-driven behavior is
validated up front so failures are reported clearly before any pipeline
stage executes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dataset_foundry.config import load_config
from dataset_foundry.constants import DEFAULT_MANIFEST_FILENAME
from dataset_foundry.exceptions import DatasetFoundryError
from dataset_foundry.pipeline import Pipeline


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="foundry",
        description="Dataset Foundry: build reproducible, versioned datasets.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a pipeline configuration file."
    )
    validate_parser.add_argument("config", help="Path to the pipeline YAML config.")

    run_parser = subparsers.add_parser("run", help="Run a dataset pipeline.")
    run_parser.add_argument("config", help="Path to the pipeline YAML config.")
    run_parser.add_argument(
        "--manifest-dir",
        default=".",
        help="Directory to write the run manifest into (default: current directory).",
    )

    subparsers.add_parser("version", help="Show the Dataset Foundry version.")

    return parser


def _cmd_validate(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    print(f"Configuration '{args.config}' is valid.")
    print(f"  name: {config.name}")
    print(f"  profile: {config.profile}")
    print(f"  sources: {len(config.sources)}")
    print(f"  export format: {config.export.format}")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    pipeline = Pipeline(config)
    manifest = pipeline.run()

    manifest_path = Path(args.manifest_dir) / DEFAULT_MANIFEST_FILENAME
    written_path = manifest.write(manifest_path)
    print(f"Pipeline '{config.name}' completed. Manifest written to '{written_path}'.")
    return 0


def _cmd_version(_args: argparse.Namespace) -> int:
    try:
        from importlib.metadata import version

        print(version("dataset-foundry"))
    except Exception:
        print("0.1.0")
    return 0


_COMMANDS = {
    "validate": _cmd_validate,
    "run": _cmd_run,
    "version": _cmd_version,
}


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``foundry`` console script."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    handler = _COMMANDS[args.command]
    try:
        return handler(args)
    except DatasetFoundryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
