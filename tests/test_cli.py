"""Tests for the ``foundry`` CLI."""

from __future__ import annotations

import json

import pytest

from dataset_foundry.cli import main

VALID_YAML = """
name: demo
profile: sft
sources:
  - type: local
    uri: /data/in
export:
  format: jsonl
  output_path: /data/out.jsonl
"""


@pytest.fixture()
def config_file(tmp_path):
    path = tmp_path / "foundry.yaml"
    path.write_text(VALID_YAML, encoding="utf-8")
    return path


def test_validate_command_success(config_file, capsys):
    exit_code = main(["validate", str(config_file)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "is valid" in captured.out


def test_validate_command_missing_file(tmp_path, capsys):
    exit_code = main(["validate", str(tmp_path / "missing.yaml")])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error" in captured.err


def test_run_command_writes_manifest(config_file, tmp_path, capsys):
    exit_code = main(["run", str(config_file), "--manifest-dir", str(tmp_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    manifest_path = tmp_path / "manifest.json"
    assert manifest_path.exists()

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert data["name"] == "demo"
    assert "Manifest written" in captured.out


def test_version_command(capsys):
    exit_code = main(["version"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip()
