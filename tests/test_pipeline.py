"""Tests for the Pipeline orchestrator."""

from __future__ import annotations

from dataset_foundry.config import ExportConfig, PipelineConfig, SourceConfig
from dataset_foundry.manifest import Manifest
from dataset_foundry.pipeline import Pipeline


def _config() -> PipelineConfig:
    return PipelineConfig(
        name="demo",
        profile="sft",
        sources=[SourceConfig(type="local", uri="/data/in")],
        export=ExportConfig(format="jsonl", output_path="/data/out.jsonl"),
    )


def test_pipeline_run_returns_manifest():
    pipeline = Pipeline(_config())
    manifest = pipeline.run()

    assert isinstance(manifest, Manifest)
    assert manifest.name == "demo"
    assert manifest.profile == "sft"
    assert manifest.source_uris == ["/data/in"]
    assert manifest.export_format == "jsonl"
    assert manifest.output_path == "/data/out.jsonl"


def test_pipeline_run_with_no_sources():
    config = _config().model_copy(update={"sources": []})
    manifest = Pipeline(config).run()
    assert manifest.source_uris == []
