"""Tests for pipeline configuration loading and validation."""

from __future__ import annotations

import pytest

from dataset_foundry.config import load_config
from dataset_foundry.exceptions import ConfigurationError

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


def test_load_valid_config(tmp_path):
    config_path = tmp_path / "foundry.yaml"
    config_path.write_text(VALID_YAML, encoding="utf-8")

    config = load_config(config_path)

    assert config.name == "demo"
    assert config.profile == "sft"
    assert len(config.sources) == 1
    assert config.sources[0].uri == "/data/in"
    assert config.export.format == "jsonl"


def test_missing_file_raises(tmp_path):
    with pytest.raises(ConfigurationError):
        load_config(tmp_path / "missing.yaml")


def test_invalid_profile_raises(tmp_path):
    config_path = tmp_path / "foundry.yaml"
    config_path.write_text(VALID_YAML.replace("sft", "bogus"), encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_config(config_path)


def test_invalid_export_format_raises(tmp_path):
    config_path = tmp_path / "foundry.yaml"
    config_path.write_text(VALID_YAML.replace("jsonl", "xml"), encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_config(config_path)


def test_malformed_yaml_raises(tmp_path):
    config_path = tmp_path / "foundry.yaml"
    config_path.write_text("name: [unclosed", encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_config(config_path)
