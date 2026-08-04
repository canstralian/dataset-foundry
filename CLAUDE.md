# CLAUDE.md

## Repository Mission

Build a governed, configuration-driven Dataset Foundry that transforms raw datasets into reproducible, versioned artifacts.

## Engineering Principles

- Architecture before implementation.
- Configuration before code.
- Immutable manifests.
- License validation before dataset composition.
- Semantic chunking over fixed token chunking.
- Evidence and lineage for every transformation.
- Plugin-first architecture.
- Small, reviewable pull requests.
- Specifications before implementation.
- ADRs for significant architectural decisions.

## Primary References

- docs/PROJECT_MANIFEST.md
- docs/ARCHITECTURE.md
- docs/specifications/
- docs/adr/
- docs/runbooks/

## Coding Standards

- Prefer composition over inheritance.
- Type hints throughout.
- Pydantic models for contracts.
- Configuration-driven behavior.
- Unit tests for every pipeline stage.
- No hardcoded dataset-specific logic.

## Success Criteria

Every dataset should be:

- Reproducible
- Versioned
- License-aware
- Quality scored
- Semantically chunked
- Fully traceable through lineage and manifests.
