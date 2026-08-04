"""Custom exceptions used throughout the Dataset Foundry pipeline."""

from __future__ import annotations


class DatasetFoundryError(Exception):
    """Base exception for all Dataset Foundry errors."""


class ConfigurationError(DatasetFoundryError):
    """Raised when pipeline configuration is invalid or missing."""


class LicenseValidationError(DatasetFoundryError):
    """Raised when a dataset source fails license validation."""


class PipelineStageError(DatasetFoundryError):
    """Raised when a pipeline stage fails during execution."""


class ManifestError(DatasetFoundryError):
    """Raised when manifest generation, loading, or validation fails."""
