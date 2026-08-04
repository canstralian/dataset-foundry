"""Tests for Manifest immutability and serialization."""

from __future__ import annotations

import pytest

from dataset_foundry.exceptions import ManifestError
from dataset_foundry.manifest import Manifest


def _manifest() -> Manifest:
    return Manifest(
        name="demo",
        profile="sft",
        source_uris=["/data/in"],
        record_count=10,
        export_format="jsonl",
        output_path="/data/out.jsonl",
    )


def test_manifest_is_frozen():
    manifest = _manifest()
    with pytest.raises(Exception):
        manifest.name = "changed"  # type: ignore[misc]


def test_manifest_write_and_read_roundtrip(tmp_path):
    manifest = _manifest()
    path = manifest.write(tmp_path / "manifest.json")

    loaded = Manifest.read(path)
    assert loaded.name == manifest.name
    assert loaded.source_uris == manifest.source_uris
    assert loaded.record_count == manifest.record_count


def test_manifest_write_refuses_overwrite(tmp_path):
    manifest = _manifest()
    path = tmp_path / "manifest.json"
    manifest.write(path)

    with pytest.raises(ManifestError):
        manifest.write(path)


def test_manifest_read_missing_file_raises(tmp_path):
    with pytest.raises(ManifestError):
        Manifest.read(tmp_path / "missing.json")
