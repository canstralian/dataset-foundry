"""Immutable manifest generation for reproducible dataset artifacts.

Every pipeline run produces a manifest recording configuration, sources,
record counts, and lineage references so the resulting dataset artifact is
fully traceable and reproducible.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from dataset_foundry.constants import MANIFEST_SCHEMA_VERSION
from dataset_foundry.exceptions import ManifestError


class Manifest(BaseModel):
    """An immutable record of a single dataset pipeline run."""

    schema_version: str = MANIFEST_SCHEMA_VERSION
    name: str
    profile: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_uris: list[str] = Field(default_factory=list)
    record_count: int = 0
    export_format: str
    output_path: str
    extra: dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}

    def write(self, path: str | Path) -> Path:
        """Write this manifest to disk as JSON, without overwriting an existing manifest."""
        manifest_path = Path(path)
        if manifest_path.exists():
            raise ManifestError(
                f"Manifest already exists at '{manifest_path}'. "
                "Manifests are immutable and must not be overwritten."
            )
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(self.model_dump_json(indent=2), encoding="utf-8")
        return manifest_path

    @classmethod
    def read(cls, path: str | Path) -> "Manifest":
        """Load a manifest from disk."""
        manifest_path = Path(path)
        if not manifest_path.is_file():
            raise ManifestError(f"Manifest file not found: {manifest_path}")
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ManifestError(f"Failed to parse manifest '{manifest_path}': {exc}") from exc
        return cls.model_validate(data)
