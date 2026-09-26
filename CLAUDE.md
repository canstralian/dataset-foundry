# CLAUDE.md

Operating instructions for AI coding agents in `dataset-foundry`. If this file conflicts
with a request, stop and ask.

## Current posture

RIF Dataset Foundry aims to produce reproducible, versioned, evidence-backed datasets from
heterogeneous sources. It is a **pre-alpha architecture scaffold**, not a working
ingestion-to-export pipeline.

- Read [README.md](README.md) before changing the repository.
- Do not describe proposed functionality or passing packaging checks as implemented behavior.
- This inventory was verified against `main` at `d213ee3689cd92dbabafc28ce5fcaa5e71f0b728`.
  Re-check files, PRs, and CI at the actual base and head commits before relying on it.

## Source-of-truth inventory

| Path | Verified state and authority |
| --- | --- |
| [README.md](README.md) | Vision, intended workflow, candid scaffold status. Goals are not implementation evidence. |
| [pyproject.toml](pyproject.toml) | `dataset-foundry` `0.0.0`, Python `>=3.11`, `dependencies = []`, `dev` extra with QA tools. Does not settle runtime or model dependencies. |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | The only active workflow. GitHub Actions on the exact commit is execution authority. |
| [docs/specifications/DATASET_SCHEMA.md](docs/specifications/DATASET_SCHEMA.md) | **Empty — schema, record, and manifest work BLOCKED.** |
| [docs/specifications/LICENSE_POLICY.md](docs/specifications/LICENSE_POLICY.md) | **Empty — licence-policy work BLOCKED.** |
| [docs/specifications/CHUNKING.md](docs/specifications/CHUNKING.md) | **Empty — chunking work BLOCKED.** |
| [docs/specifications/EXPORT_PROFILES.md](docs/specifications/EXPORT_PROFILES.md) | **Empty — SFT/DPO/RAG/eval mapping BLOCKED.** |
| [docs/architecture/DATASET_FOUNDRY.md](docs/architecture/DATASET_FOUNDRY.md) | **Empty — architecture not ratified.** |
| [docs/architecture/PIPELINE.md](docs/architecture/PIPELINE.md) | **Empty — stage transitions not ratified.** |
| [docs/adr/ADR-0001.md](docs/adr/ADR-0001.md) | **Empty — no ADR decision can be cited.** |
| [docs/examples/PIPELINE.md](docs/examples/PIPELINE.md) | **Empty — no executable example.** |
| [tests/](tests/) | Five zero-byte placeholder files. No stage coverage may be claimed. |
| [.github/agents/dataset-foundry-assistant.agent.md](.github/agents/dataset-foundry-assistant.agent.md) | Agent definition exists. Activation, branch workflow, and enforcement are unverified. |
| [.gitignore](.gitignore) | Excludes Python caches, build output, environments, secrets files, and QA artifacts. Does not untrack already-committed files. |

These paths do **not** exist; never cite them as sources: `docs/PROJECT_MANIFEST.md`,
`docs/ARCHITECTURE.md`, `docs/runbooks/`. No `.specify/` workspace or Spec Kit feature
packet has been verified.

## Repository layout

Every module below is an empty placeholder on the verified base.

| Path | Intended responsibility |
| --- | --- |
| `dataset_foundry/loader/` | Source adapters (local, GitHub, Hugging Face) |
| `dataset_foundry/license_gate/` | Licence and provenance admission |
| `dataset_foundry/normalizer/` | Record normalization (code, QA, traces) |
| `dataset_foundry/dedupe/` | Exact and semantic deduplication |
| `dataset_foundry/chunker/` | Structure-aware chunking (AST, markdown, conversation, trace) |
| `dataset_foundry/classifier/` | Domain and task classification |
| `dataset_foundry/quality/` | Quality metrics and scoring |
| `dataset_foundry/lineage/` | Lineage graph and history |
| `dataset_foundry/profiles/` | Export profiles (SFT, DPO, RAG, eval) |
| `dataset_foundry/exporter/` | Output writers (JSONL, Parquet, Hugging Face) |
| `dataset_foundry/registry/` | Dataset, licence, and profile registries |
| `dataset_foundry/schemas/` | Contract schemas |
| `dataset_foundry/cli/` | Command-line entry point |
| `dataset_foundry/{config,manifest,pipeline,types,constants,exceptions}.py` | Core contracts |

## Specification-first rule

1. Read the governing specification, architecture document, and ADR before implementing
   domain behavior.
2. **An empty document is a blocked contract, not permission to invent its contents.**
   You may draft or clarify the document. Implementation waits for a merged, human-approved spec.
3. Every spec defines: scenarios, inputs and outputs, invariants, acceptance cases
   (positive, negative, boundary, failure), provenance and rights decisions, and
   reproducibility expectations.
4. Significant design choices require a reviewed ADR before implementation.
5. When a spec, ADR, tooling repair, or stage merges, update this file in the **same PR**.
   A document's existence does not mean it is ratified.

**Scope of the block.** These changes are not blocked: documentation, `pyproject.toml`
metadata, CI configuration, and `.gitignore`. Any new or changed code under
`dataset_foundry/` or `tests/` is domain work and is blocked by rule 2.

## Commands

Run from the repository root. Install fail-closed: if the `dev` extra fails, stop and report.

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"

ruff check .
ruff format --check .
mypy .
bandit -q -r .
pip-audit
pytest -q --maxfail=1 --disable-warnings --cov=. --cov-report=term-missing --cov-report=xml
```

CI runs these on Python 3.11 and 3.12. How CI's install step differs from the above is
recorded under [Tooling gaps](#tooling-gaps-to-keep-visible).

Local runs are supporting evidence only. Report a check as **passing** only when GitHub
Actions ran it on the exact proposed commit. An install or package smoke test does not
prove loader, licence, chunking, exporter, or pipeline correctness.

## Unresolved decisions — do not select defaults

| Topic | Required decision |
| --- | --- |
| Contract-model library | Runtime dependencies are empty. Pydantic was named previously but is not declared. Adding it needs an ADR plus the `pyproject.toml` change in one PR. |
| CLI entry point | No `[project.scripts]` entry. Decide interface, invocation, and error behavior first. |
| Chunking | Algorithm, boundaries, context retention, determinism, and evaluation are not approved. |
| Rights policy | Evidence, intended-use compatibility, human review, escalation, and reassessment need the licence spec. Default to non-admission. |
| Dataset identity | Record and manifest schemas, canonicalization, digest and version policy, storage, and replay are not approved. |
| Publication and export | No approved destinations, export profiles, or release gate. No automatic remote publication. |
| Copilot agent workflow | Confirm branch ownership, integration, and review process for `.github/agents/`. File presence is not enforcement. |
| Unmerged prototype branch | `copilot/explore-codebase-cli-improvements` holds unapproved code, a divergent `pyproject.toml`, and committed `*.egg-info/` and `__pycache__/`. Do not merge it. Port only reviewed source files, never artifacts, and reconcile metadata with current `pyproject.toml`. |

## Guardrails

**Evidence**
- Do not claim tests, scans, reproducibility, or policy compliance without evidence tied to the exact commit.
- State assumptions and uncertainty explicitly.

**Review and merge**
- Do not commit directly to `main`.
- Do not force-push, self-approve, auto-merge, or bypass review.
- A human reviews and merges every PR.

**Gates**
- Do not remove, skip, mute, or loosen tests, lint, formatting, typing, dependency audits, security scanners, or policy gates.
- If a gate fails, fix the cause or stop and report. Do not add placeholder tests to turn CI green.

**Repository contents**
- Do not commit secrets: passwords, tokens, `.env` files, Hugging Face or GitHub credentials.
- Do not commit sensitive dataset content or generated datasets.
- Do not commit virtual environments, bytecode, caches, `*.egg-info/`, build output, or coverage output.
- Check `git status` and the PR diff before pushing. Tracked artifacts stay tracked despite `.gitignore`.

**Side effects**
- No undocumented network ingestion or remote publishing.
- No changes to permissions, repository settings, releases, deployments, or infrastructure unless that is the approved task.

**Data governance**
- Licence and provenance admission fails closed: missing, incompatible, conflicting, or unresolved evidence never authorizes composition, export, or publication.
- A public URL or download link is not rights evidence.
- Record source rights, provenance, transformations, and rejected outcomes with their reasons.

**Scope**
- Limit changes to the approved scope.
- Include rollback instructions in the PR description.

## Coding standards

These apply once a stage is unblocked.

- Type hints on all public functions and module-level state.
- Composition over inheritance; stage interfaces over concrete classes.
- Immutable data for contracts and manifests.
- Explicit exceptions from `dataset_foundry/exceptions.py`; no bare `except`.
- Configuration and registries drive behavior. No hardcoded source names, paths, or record shapes.
- Preserve source originals. Each transformation records input, effective configuration, decision, output, and failure in lineage.

## Definition of done

A domain feature is done only when all of these hold:

1. Its specification, and any required ADR, is non-empty and approved.
2. The implementation meets measurable acceptance criteria from that spec.
3. Tests cover positive, negative, boundary, and failure cases for each affected stage, or justify why a case does not apply.
4. Provenance, admission, rejection, lineage, and output evidence are demonstrable where relevant.
5. The diff is scoped and reviewable.
6. Exact-head CI evidence for every required check is attached, or each gap is stated.
7. A human has reviewed and approved the merge.

Documentation-only PRs must validate their claims and links. They do not count as implemented capability.

## Tooling gaps to keep visible

CI does not yet enforce everything this file requires.

| Gap | Consequence |
| --- | --- |
| CI install uses `pip install -e ".[dev]" \|\| pip install -e .`, then reinstalls QA tools separately | A broken `dev` extra is masked. Do not copy this pattern. |
| Ruff runs default rules only (no `select`) | Lint passing does not mean the coding standards are met. |
| Mypy is not strict | "Type hints throughout" is not enforced. |
| Coverage has no `--cov-fail-under` | Coverage is reported, never gated. |
| Dev tools are unpinned | Gate results can drift between runs. |
| `.pre-commit-config.yaml` is empty | No pre-commit enforcement. |
| `lint.yml` and `release.yml` are empty | They are not gates. Their cleanup is under separate review; do not edit them to hide failures. |
| No dedicated secret scanner, spec validation, or Spec Kit workflow in CI | Those properties are unverified. |
| Test stage fails on the zero-byte placeholders | Expected on this base. An unmerged smoke-test PR is not `main` validation. |

**Maintenance rule:** A PR that closes a gap, or merges a spec, ADR, or stage, updates the
matching row here in the same PR, with the file or exact-commit evidence. This file must
describe what is true, not what is intended.
