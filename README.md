# RIF Dataset Foundry

A governed, configuration-driven dataset engineering platform for building reproducible, versioned datasets from heterogeneous sources.

> **Project status: pre-alpha architecture scaffold.** The repository contains Python packaging metadata, a CI workflow, and placeholder modules and specifications. It does **not** yet implement an end-to-end dataset pipeline. The capabilities described below are design goals, not shipped features.

## Vision

Transform raw datasets into evidence-backed, license-aware, semantically chunked datasets for supervised fine-tuning (SFT), direct preference optimization (DPO), retrieval-augmented generation (RAG), evaluation, and future AI workflows.

The central idea is that a dataset is more than its exported rows: it should be possible to explain where each record came from, why it was admitted, which transformations produced it, and which configuration and artifact version can reproduce it.

## Intended workflow

The proposed pipeline is:

```text
Declared sources
    -> provenance and licence admission
    -> loading and normalization
    -> deduplication
    -> structure-aware chunking
    -> quality assessment
    -> profile-specific export
    -> versioned artifacts and lineage manifest
```

Each transition is intended to record inputs, effective configuration, decisions, outputs, and failures. Sources with missing or disallowed rights evidence must not silently enter a composed dataset. Exact record schemas, policy outcomes, chunking strategies, quality thresholds, and export mappings require approved specifications before implementation.

## Engineering principles

- **Governance before composition:** verify source origin, intended use, and licence/provenance evidence before accepting material.
- **Reproducibility by design:** bind run configuration, source identity, transformation versions, and artifact digests to the output.
- **Evidence and lineage:** preserve a traceable relationship from an exported record to its source and each transformation; keep rejected records distinguishable from accepted ones.
- **Configuration before special cases:** prefer typed, composable adapters and explicit policies over hardcoded dataset-specific logic.
- **Context-aware segmentation:** specify and test structure-preserving chunking rather than assuming a fixed token window is semantically sufficient.
- **Meaningful validation:** implement positive, negative, boundary, and failure-path tests for each real pipeline stage; do not treat placeholder tests or a package smoke test as domain coverage.
- **Human-reviewed changes:** make small PRs, retain the existing CI and security gates, and require explicit review for architectural and publishing decisions.

These principles summarize the repository's existing [engineering guidance](CLAUDE.md); the detailed contracts are still to be written and approved.

## What exists today

| Area | Current state |
| --- | --- |
| Python package | `dataset_foundry/` scaffold with an installable `pyproject.toml` (declared version `0.0.0`, Python 3.11+) |
| Pipeline stages | Directories for loaders, normalization, chunking, deduplication, licence checks, quality, lineage, profiles, and export; implementations are placeholders |
| Specifications and ADRs | [Documentation paths](docs/) exist, but their present specification and ADR files are empty placeholders |
| CI | [GitHub Actions CI](.github/workflows/ci.yml) defines installation, Ruff lint/format, Mypy, Bandit, pip-audit, and pytest/coverage across Python 3.11 and 3.12 |
| Functional verification | No completed end-to-end pipeline or domain-stage test suite on the current base branch |

**Do not infer production readiness from package installation, CI configuration, or a passing smoke test.** Review the result of the relevant workflow against the exact commit before reporting a check as successful.

## Repository map

```text
dataset_foundry/       Planned pipeline components and package scaffold
docs/specifications/   Placeholder domain specifications
docs/architecture/     Placeholder architecture documents
docs/adr/              Placeholder architectural decision records
docs/examples/         Placeholder examples
tests/                 Stage test placeholders
CLAUDE.md              Repository engineering instructions
pyproject.toml         Package metadata and development dependencies
.github/workflows/     GitHub Actions configuration
```

## Development

The current scaffold can be installed for inspection:

```bash
git clone https://github.com/canstralian/dataset-foundry.git
cd dataset-foundry
python -m pip install -e ".[dev]"
python -c "import dataset_foundry; print('package import OK')"
```

This checks packaging/importability, **not** a working dataset pipeline. The tracked stage tests on the base branch are empty; pytest will not provide meaningful pipeline validation until substantive tests and corresponding implementations land. Do not bypass or disable the test gate to conceal that gap.

## Specification-first delivery

This project follows the progression **constitution → feature specification → clarification/research → plan and data contracts → tasks → implementation and evidence**. [GitHub Spec Kit](https://github.com/github/spec-kit) is a possible workflow aid, but the current repository does not contain an initialized `.specify/` workspace or completed Spec Kit feature packet.

The first specification should establish a governed dataset foundation: source identity, provenance and rights evidence, explicit admission decisions, traceable record/transform relationships, versioned output manifests, and testable fail-closed behavior. Architectural choices such as canonical hashing, evidence persistence, licence-policy interpretation, and initial adapter scope remain decisions for documented review, not assumptions to be smuggled into code.

Initial implementation should follow an approved, bounded vertical slice. Support for all SFT/DPO/RAG/evaluation profiles, external hosting, remote publishing, and broad connector coverage is **future work**, not a prerequisite for declaring a first slice complete.

## Contributing and review

Start with [`CLAUDE.md`](CLAUDE.md), check the actual state of the relevant specifications and ADRs, and propose a narrow issue or draft PR. State assumptions, evidence, acceptance criteria, test results tied to the head SHA, residual risks, and rollback. Preserve source originals and do not assume that downloadable data is licensed for reuse or model training.

Changes affecting external publication, licence policy, security controls, or architecture require explicit human approval. No merge or release is implied by a draft document.
