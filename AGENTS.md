# AGENTS.md

## 1. Introduction

### Purpose of this Document

This document is the canonical reference for the **agents** that operate in and on the `dataset-foundry`
repository. It exists so that both human contributors and AI coding assistants (GitHub Copilot, and any
tool that reads an `AGENTS.md`/`CLAUDE.md`-style file) can quickly understand:

- what each agent is responsible for,
- how far along its implementation is, and
- how to invoke, configure, or extend it.

Keeping this file accurate matters because `dataset-foundry` is explicitly built "configuration before
code" and "architecture before implementation" (see `CLAUDE.md`). This file is part of that architecture
layer, and it will evolve alongside the specifications in `docs/specifications/` and the decisions
recorded in `docs/adr/`.

### What are Agents?

In this repository, "agent" covers two distinct but related concepts:

1. **AI coding agent(s)** — Custom GitHub Copilot agents defined under `.github/agents/*.agent.md`. These
   are persona/instruction files that configure an AI assistant with a specific role, responsibilities, and
   guardrails for working on this codebase. There is currently **one** such agent: the **Dataset Foundry
   Assistant**.
2. **Pipeline agents** — The modular, plugin-first processing stages implied by the package layout under
   `dataset_foundry/` (loader, normalizer, classifier, chunker, dedupe, license gate, quality scorer,
   exporter, lineage tracker, and registry). Each stage is meant to be an autonomous, single-responsibility,
   *deterministic* unit — not an AI/LLM agent — that consumes and produces well-defined data contracts, and
   is orchestrated by a pipeline runner. This mirrors the "Configuration-driven behavior" and "No
   hardcoded dataset-specific logic" coding standards in `CLAUDE.md`.

> **Current repository status (important):** `dataset-foundry` is presently in its architecture/scaffolding
> phase. The package and documentation *layout* already exists (folders and empty files), but almost none
> of the pipeline modules, docs, tests, `CONTRIBUTING.md`, `ROADMAP.md`, `CHANGELOG.md`, or `LICENSE` have
> content yet. This document describes the intended purpose of each pipeline agent based on the
> established layout and stated engineering principles, and is explicit about what is implemented today
> versus what is planned. Treat the "planned" items as an implementation guide, not as documentation of
> existing behavior.

## 2. Agent Overview

| # | Agent Name | Type | Brief Description | Status |
|---|---|---|---|---|
| 1 | Dataset Foundry Assistant | AI coding agent | Expert Copilot assistant for dataset engineering, schema design, and data quality work in this repo. | Active |
| 2 | Loader | Pipeline agent | Ingests raw data from local disk, GitHub, or the Hugging Face Hub. | Scaffolded |
| 3 | Normalizer | Pipeline agent | Converts heterogeneous raw records (code, Q&A, traces) into a canonical schema. | Scaffolded |
| 4 | Classifier | Pipeline agent | Labels records with domain and task-type metadata. | Scaffolded |
| 5 | Chunker | Pipeline agent | Splits content into semantically coherent chunks (AST/markdown/conversation/trace aware). | Scaffolded |
| 6 | Dedupe | Pipeline agent | Removes exact and semantic duplicate records. | Scaffolded |
| 7 | License Gate | Pipeline agent | Validates source licenses and checks compatibility before composition. | Scaffolded |
| 8 | Quality Scorer | Pipeline agent | Computes quality metrics and scores for records/datasets. | Scaffolded |
| 9 | Exporter | Pipeline agent | Serializes finished datasets to JSONL, Parquet, or Hugging Face `datasets` format. | Scaffolded |
| 10 | Lineage Tracker | Pipeline agent | Records transformation history/graph for full traceability. | Scaffolded |
| 11 | Registry | Pipeline agent | Maintains the catalog of known datasets, licenses, and export profiles. | Scaffolded |
| 12 | Pipeline Orchestrator | Pipeline agent | Runs the configured stages in order and emits an immutable manifest. | Scaffolded |

"Scaffolded" means the module file(s) and its place in the architecture exist (e.g. `dataset_foundry/loader/`),
but the implementation body is currently empty pending the relevant specification/ADR.

## 3. Detailed Agent Descriptions

### Agent: Dataset Foundry Assistant

- **Purpose:** Helps contributors design, validate, transform, document, and publish high-quality datasets,
  and helps keep the Dataset Foundry codebase itself aligned with its own engineering principles.
- **Key Features/Capabilities:**
  - Designing clear, consistent dataset schemas.
  - Validating dataset structure, types, and constraints.
  - Detecting missing values, duplicates, inconsistencies, and outliers.
  - Generating metadata, documentation, and data dictionaries.
  - Assisting with data transformation pipelines and reproducible ETL workflows.
  - Suggesting dataset versioning and organization strategies.
  - Producing scripts in Python, SQL, or JavaScript when appropriate.
  - Recommending best practices for licensing, provenance, and documentation.
- **How it Works:** It is a prompt/persona definition consumed by GitHub Copilot's custom agent tooling.
  It does not run continuously — it is invoked on demand (via Copilot Chat, Copilot CLI, or the Copilot
  coding agent) and follows the guidelines defined for it, such as prioritizing data integrity over
  convenience, explaining assumptions before structural changes, and asking for clarification instead of
  guessing.
- **Dependencies/Prerequisites:** GitHub Copilot access with custom-agent support enabled for this
  repository.
- **Configuration:** Defined in `.github/agents/dataset-foundry-assistant.agent.md`. This file is
  maintained by repository maintainers as part of Copilot tooling configuration; it is not intended to be
  edited casually by contributors or invoked directly as application code.

### Agent: Loader

- **Purpose:** Ingest raw source material into the pipeline from a variety of origins.
- **Key Features/Capabilities (planned):**
  - Common loader contract (`loader/base.py`) that all source loaders implement.
  - Local filesystem ingestion (`loader/local.py`).
  - GitHub repository ingestion (`loader/github.py`).
  - Hugging Face Hub dataset ingestion (`loader/huggingface.py`).
- **How it Works:** Each concrete loader is expected to implement the shared base interface so the rest of
  the pipeline can treat any source uniformly, in line with the plugin-first architecture principle.
- **Dependencies/Prerequisites:** Not yet pinned in `requirements.txt`. Based on the module names, a GitHub
  client library and the Hugging Face `huggingface_hub`/`datasets` libraries are anticipated for those
  respective loaders.
- **Configuration:** Not yet defined; expected to be driven by `dataset_foundry/config.py` once implemented.

### Agent: Normalizer

- **Purpose:** Convert heterogeneous raw records into the canonical dataset record schema.
- **Key Features/Capabilities (planned):**
  - Shared base contract (`normalizer/base.py`).
  - Source-code-specific normalization (`normalizer/code.py`).
  - Question/answer-pair normalization (`normalizer/qa.py`).
  - Execution/reasoning-trace normalization (`normalizer/traces.py`).
- **How it Works:** Content-type-specific normalizers translate raw loader output into the shape defined by
  the (currently unwritten) `docs/specifications/DATASET_SCHEMA.md`, so downstream agents can rely on a
  single consistent record structure.
- **Dependencies/Prerequisites:** None declared yet.
- **Configuration:** Not yet defined.

### Agent: Classifier

- **Purpose:** Attach domain and task-type labels to normalized records.
- **Key Features/Capabilities (planned):**
  - Domain classification (`classifier/domain.py`).
  - Task-type classification (`classifier/task.py`).
- **How it Works:** Labels produced here are expected to drive downstream routing/filtering decisions, such
  as which export profile (SFT, DPO, RAG, evaluation) a record is eligible for.
- **Dependencies/Prerequisites:** None declared yet.
- **Configuration:** Not yet defined.

### Agent: Chunker

- **Purpose:** Split normalized content into semantically coherent chunks rather than fixed-size token
  windows, per the "semantic chunking over fixed token chunking" engineering principle.
- **Key Features/Capabilities (planned):**
  - Shared base contract (`chunker/base.py`).
  - AST-aware chunking for source code (`chunker/ast.py`).
  - Conversation-turn-aware chunking (`chunker/conversation.py`).
  - Markdown-structure-aware chunking (`chunker/markdown.py`).
  - Execution-trace-aware chunking (`chunker/trace.py`).
- **How it Works:** A chunking strategy is selected based on content type so each chunk boundary respects
  the structure of the content (e.g. function/class boundaries in code, headings in markdown), rather than
  cutting at an arbitrary token count.
- **Dependencies/Prerequisites:** Likely a code-aware parser (for AST chunking) and a markdown parser; none
  are pinned yet in `requirements.txt`.
- **Configuration:** Expected to be specified in `docs/specifications/CHUNKING.md` (currently empty).

### Agent: Dedupe

- **Purpose:** Remove duplicate records before they reach quality scoring and export.
- **Key Features/Capabilities (planned):**
  - Exact-match deduplication (`dedupe/exact.py`).
  - Semantic/embedding-similarity deduplication (`dedupe/semantic.py`).
- **How it Works:** Exact dedupe is expected to use hashing/string-equality; semantic dedupe is expected to
  compare embeddings or another similarity signal to catch near-duplicates that exact matching would miss.
- **Dependencies/Prerequisites:** Semantic dedupe will likely require an embedding model/library; none
  pinned yet.
- **Configuration:** Not yet defined.

### Agent: License Gate

- **Purpose:** Enforce "license validation before dataset composition" so incompatible or disallowed
  sources cannot be combined into an output dataset.
- **Key Features/Capabilities (planned):**
  - License validation (`license_gate/validator.py`).
  - License compatibility checks between sources and target dataset license (`license_gate/compatibility.py`).
- **How it Works:** Each record's declared license is expected to be checked against a compatibility policy
  before the record is allowed into a composed dataset, blocking or flagging violations.
- **Dependencies/Prerequisites:** None declared yet.
- **Configuration:** Expected to be specified in `docs/specifications/LICENSE_POLICY.md` (currently empty).

### Agent: Quality Scorer

- **Purpose:** Quantify dataset/record quality so downstream stages and consumers can filter or rank by it.
- **Key Features/Capabilities (planned):**
  - Quality metrics computation (`quality/metrics.py`).
  - Aggregate scoring (`quality/scorer.py`).
- **How it Works:** Individual metrics are expected to be computed per record/dataset and combined into a
  single quality score, supporting the "quality scored" success criterion in `CLAUDE.md`.
- **Dependencies/Prerequisites:** None declared yet.
- **Configuration:** Not yet defined.

### Agent: Exporter

- **Purpose:** Serialize the final, validated dataset into standard, reusable formats.
- **Key Features/Capabilities (planned):**
  - JSON Lines export (`exporter/jsonl.py`).
  - Parquet export (`exporter/parquet.py`).
  - Hugging Face `datasets`-compatible export (`exporter/huggingface.py`).
- **How it Works:** Consumes the pipeline's final record set and the target export profile (SFT/DPO/RAG/
  evaluation, under `dataset_foundry/profiles/`) to write output in the requested format(s).
- **Dependencies/Prerequisites:** Parquet export will need `pyarrow` (or similar); Hugging Face export will
  need the `datasets` library. Neither is pinned yet in `requirements.txt`.
- **Configuration:** Expected to be specified in `docs/specifications/EXPORT_PROFILES.md` (currently empty).

### Agent: Lineage Tracker

- **Purpose:** Guarantee "evidence and lineage for every transformation" so any output record can be traced
  back to its original source and every step applied to it.
- **Key Features/Capabilities (planned):**
  - Lineage graph construction (`lineage/graph.py`).
  - Historical transformation log (`lineage/history.py`).
- **How it Works:** Every transformation performed by another agent is expected to be recorded as a node/
  edge (or log entry), producing a fully auditable trail from raw source to exported record.
- **Dependencies/Prerequisites:** None declared yet.
- **Configuration:** Not yet defined.

### Agent: Registry

- **Purpose:** Provide the configuration-driven catalog other agents consult instead of hardcoding
  dataset-specific logic.
- **Key Features/Capabilities (planned):**
  - Known-dataset catalog (`registry/datasets.py`).
  - Known-license catalog (`registry/licenses.py`).
  - Export-profile catalog (`registry/profiles.py`).
- **How it Works:** Acts as a lookup layer so pipeline agents remain generic and dataset-agnostic.
- **Dependencies/Prerequisites:** None declared yet.
- **Configuration:** Not yet defined.

### Agent: Pipeline Orchestrator

- **Purpose:** Run the configured agents in sequence and produce a reproducible, versioned result.
- **Key Features/Capabilities (planned):**
  - Stage sequencing (`dataset_foundry/pipeline.py`).
  - Immutable manifest generation (`dataset_foundry/manifest.py`) capturing configuration, versions, and
    lineage for reproducibility.
  - A command-line entry point (`dataset_foundry/cli/`) for invoking runs.
- **How it Works:** Reads a pipeline configuration, invokes Loader → Normalizer → Classifier → Chunker →
  Dedupe → License Gate → Quality Scorer → Exporter (consulting the Registry and recording Lineage
  throughout), and writes an immutable manifest describing the run.
- **Dependencies/Prerequisites:** None declared yet.
- **Configuration:** Expected to be driven by `dataset_foundry/config.py` and a user-supplied pipeline
  configuration file (format not yet specified).

## 4. Usage Examples

### Example 1: Asking the Dataset Foundry Assistant to design a schema

- **Prompt:** "Design a Pydantic schema for a Q&A dataset record that includes provenance and license
  fields."
- **Expected Behavior:** The assistant proposes a typed Pydantic model, explains its field choices, flags
  any assumptions (e.g. license field format), and suggests accompanying validation tests — rather than
  silently hardcoding values.

### Example 2: Asking the Dataset Foundry Assistant to review data quality

- **Prompt:** "Review this JSONL sample for duplicates, missing fields, and license inconsistencies."
- **Expected Behavior:** The assistant inspects the sample, reports specific issues found (with row/field
  references), and recommends concrete remediation steps or validation checks — asking for clarification if
  the schema or licensing intent is ambiguous.

### Example 3 (planned interface — not yet implemented): Running the pipeline

```bash
# Illustrative target usage only. dataset_foundry/cli is currently an empty
# scaffold, so this command does not work yet.
dataset-foundry run --config pipeline.yaml
```

- **Expected Output/Behavior (once implemented):** The Pipeline Orchestrator would load raw data, run it
  through each pipeline agent, and write an exported dataset plus an immutable manifest describing the run.

### Example 4 (works today): Running the CI quality gates locally

```bash
python -m pytest
python -m mypy .
```

- **Expected Output/Behavior:** `pytest` and `mypy` are the two CI checks (see `.github/workflows/ci.yml`)
  that currently execute without requiring valid `pyproject.toml` project metadata. `ruff check .`, `ruff
  format --check .`, and `pip install -e .` currently fail — see [Troubleshooting](#7-troubleshooting--faq).

## 5. Getting Started

### Installation/Setup

1. Clone the repository and check out the branch you intend to work on.
2. Create a virtual environment using Python 3.11 or 3.12 (the versions exercised by
   `.github/workflows/ci.yml`).
3. Install the quality-gate tooling used in CI: `pip install pytest pytest-cov ruff mypy bandit pip-audit`.
   (`requirements.txt` is currently empty, so there are no pinned runtime dependencies to install yet.)
4. Read `README.md` and `CLAUDE.md` for the project vision and engineering principles before making changes.

### First Steps

1. Pick a pipeline agent to implement, starting with one that already has a corresponding (currently empty)
   test file — `tests/test_loader.py`, `tests/test_normalizer.py`, `tests/test_chunker.py`,
   `tests/test_license_gate.py`, or `tests/test_pipeline.py` — since these indicate the initial
   implementation priority.
2. Check `docs/specifications/` and `docs/adr/` for the relevant specification or decision record; if it is
   still empty, write the specification/ADR first, per "specifications before implementation."
3. Use the Dataset Foundry Assistant (via Copilot) to help draft the schema/contract, then the
   implementation, then accompanying unit tests.

## 6. Advanced Usage / Customization

- **Plugin-first architecture:** New loaders, normalizers, chunkers, classifiers, or exporters are intended
  to be added as new modules implementing the relevant stage's base interface (e.g. `loader/base.py`,
  `normalizer/base.py`, `chunker/base.py`), then made discoverable through the Registry
  (`dataset_foundry/registry/`) rather than by editing existing stage code.
- **Configuration-driven behavior:** Once `dataset_foundry/config.py` is implemented, dataset-specific
  behavior should be expressed as configuration rather than code changes, per the "no hardcoded
  dataset-specific logic" coding standard.
- **Extending the AI coding agent:** Additional Copilot custom agents can be added as new
  `*.agent.md` files under `.github/agents/`; each is independent and should be given a distinct,
  descriptive name.

## 7. Troubleshooting / FAQ

- **`pip install -e .` fails with a `TOMLDecodeError`.** `pyproject.toml` does not currently contain valid
  project metadata (it currently holds CI step descriptions rather than `[project]`/`[build-system]`
  tables), so it cannot be parsed as TOML. This also causes `ruff check .`, `ruff format --check .`, and
  `pytest`'s own config discovery to fail. This is a pre-existing scaffolding gap, not something introduced
  by this document; if you hit it, that is expected until `pyproject.toml` is populated with real project
  metadata.
- **`mypy .` prints a `pyproject.toml` parse warning but still succeeds.** Mypy tolerates the invalid
  `pyproject.toml` and falls back to defaults, so it can still analyze the (currently empty) source files.
- **Why are most modules empty?** The repository intentionally scaffolds its architecture before writing
  implementation, per "architecture before implementation" and "specifications before implementation" in
  `CLAUDE.md`. Check `docs/adr/` and `docs/specifications/` for the latest design decisions before
  implementing a stage.
- **Where is the Copilot agent configured?** `.github/agents/dataset-foundry-assistant.agent.md`. Treat it
  as Copilot tooling configuration rather than application code.
- **No license is declared yet.** See [License](#9-license) below before reusing any code from this
  repository.

## 8. Contributing

`CONTRIBUTING.md` is currently an empty placeholder, so there is no repository-specific contribution guide
yet. Until it is filled in, follow the engineering principles already documented in `CLAUDE.md`:

- Keep pull requests small and reviewable.
- Write (or update) a specification in `docs/specifications/` before implementing a pipeline agent.
- Record significant architectural decisions as an ADR in `docs/adr/`.
- Prefer composition over inheritance, use type hints throughout, and model contracts with Pydantic.
- Add unit tests for every pipeline stage you implement.
- Avoid hardcoding dataset-specific logic; prefer configuration-driven behavior.

## 9. License

The repository's `LICENSE` file is currently **empty** — no license has been chosen or published yet.
Until a license is added, do not assume this code is available for reuse, modification, or redistribution;
check with the repository maintainers (`canstralian`) before relying on any licensing assumption.
