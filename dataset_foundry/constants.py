"""Repository-wide constants for Dataset Foundry."""

from __future__ import annotations

DEFAULT_CONFIG_FILENAME = "foundry.yaml"
DEFAULT_MANIFEST_FILENAME = "manifest.json"

SUPPORTED_PROFILES = ("sft", "dpo", "rag", "eval")
SUPPORTED_EXPORT_FORMATS = ("jsonl", "parquet", "huggingface")

MANIFEST_SCHEMA_VERSION = "1.0"
