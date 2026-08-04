"""Pipeline orchestration for Dataset Foundry.

The Pipeline wires together the configured stages (loaders, normalizers,
chunkers, license gate, quality scoring, exporters) and produces an
immutable Manifest describing the run. Stage implementations are resolved
at runtime, keeping the pipeline itself free of dataset-specific logic.
"""

from __future__ import annotations

from dataset_foundry.config import PipelineConfig
from dataset_foundry.manifest import Manifest


class Pipeline:
    """Executes a dataset pipeline run from a validated configuration."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config

    def run(self) -> Manifest:
        """Execute the pipeline and return the resulting Manifest.

        This orchestrates, in order: loading, normalization, license
        validation, chunking, classification, deduplication, quality
        scoring, and export. Stage wiring is intentionally left to be
        expanded as each stage's plugin registry is implemented.
        """
        source_uris = [source.uri for source in self.config.sources]

        # NOTE: stage execution (load -> normalize -> license_gate -> chunk
        # -> classify -> dedupe -> quality -> export) is implemented
        # incrementally as each stage's plugin registry becomes available.
        record_count = 0

        return Manifest(
            name=self.config.name,
            profile=self.config.profile,
            source_uris=source_uris,
            record_count=record_count,
            export_format=self.config.export.format,
            output_path=self.config.export.output_path,
        )
