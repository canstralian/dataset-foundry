"""Configuration loading and validation for Dataset Foundry pipelines.

Configuration is the source of truth for pipeline behavior ("configuration
before code"). Pipelines are defined declaratively in YAML and validated
against this Pydantic contract before any stage executes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator

from dataset_foundry.constants import SUPPORTED_EXPORT_FORMATS, SUPPORTED_PROFILES
from dataset_foundry.exceptions import ConfigurationError


class SourceConfig(BaseModel):
    """Configuration for a single dataset source (loader)."""

    type: str
    uri: str
    options: dict[str, Any] = Field(default_factory=dict)


class ExportConfig(BaseModel):
    """Configuration for exporting the final dataset."""

    format: str
    output_path: str

    @field_validator("format")
    @classmethod
    def _validate_format(cls, value: str) -> str:
        if value not in SUPPORTED_EXPORT_FORMATS:
            raise ValueError(
                f"Unsupported export format '{value}'. "
                f"Expected one of: {', '.join(SUPPORTED_EXPORT_FORMATS)}"
            )
        return value


class PipelineConfig(BaseModel):
    """Top-level, immutable configuration contract for a pipeline run."""

    name: str
    profile: str
    sources: list[SourceConfig] = Field(default_factory=list)
    export: ExportConfig
    options: dict[str, Any] = Field(default_factory=dict)

    @field_validator("profile")
    @classmethod
    def _validate_profile(cls, value: str) -> str:
        if value not in SUPPORTED_PROFILES:
            raise ValueError(
                f"Unsupported profile '{value}'. "
                f"Expected one of: {', '.join(SUPPORTED_PROFILES)}"
            )
        return value

    model_config = {"frozen": True}


def load_config(path: str | Path) -> PipelineConfig:
    """Load and validate a pipeline configuration from a YAML file.

    Raises:
        ConfigurationError: if the file is missing, unreadable, or invalid.
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise ConfigurationError(f"Configuration file not found: {config_path}")

    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"Failed to parse YAML config '{config_path}': {exc}") from exc

    try:
        return PipelineConfig.model_validate(raw)
    except Exception as exc:  # pydantic.ValidationError
        raise ConfigurationError(f"Invalid configuration in '{config_path}': {exc}") from exc
