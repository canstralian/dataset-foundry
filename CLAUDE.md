# CLAUDE.md

## Mission and current posture

RIF Dataset Foundry aims to produce reproducible, versioned, evidence-backed datasets from heterogeneous sources. The project is a **pre-alpha architecture scaffold**, not a working ingestion-to-export pipeline. Read [README.md](README.md) before modifying the repository. Do not describe proposed functionality or passing packaging checks as implemented domain behavior.

These are repository-local working instructions. Re-check files, PRs, and CI at the actual base and head SHAs; this status inventory was prepared against `main` at `d213ee3689cd92dbabafc28ce5fcaa5e71f0b728` and must be updated when its facts change.

## Source-of-truth inventory

| Path | Verified state and authority |
| --- | --- |
| [README.md](README.md) | Exists; project vision, intended workflow and candid scaffold status. Goals are not implementation evidence. |
| [pyproject.toml](pyproject.toml) | Exists; setuptools metadata, distribution `dataset-foundry` version `0.0.0`, Python `>=3.11`, dev tools. This does not settle future runtime/model dependencies. |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | Exists; actual Python 3.11/3.12 install, QA, security and test commands. GitHub Actions on the exact commit is execution authority. |
| [docs/specifications/DATASET_SCHEMA.md](docs/specifications/DATASET_SCHEMA.md) | Exists but **empty — schema/record/manifest implementation BLOCKED** pending an approved contract. |
| [docs/specifications/LICENSE_POLICY.md](docs/specifications/LICENSE_POLICY.md) | Exists but **empty — licence-policy implementation BLOCKED** pending an approved contract; unresolved evidence must never be silently accepted. |
| [docs/specifications/CHUNKING.md](docs/specifications/CHUNKING.md) | Exists but **empty — chunking implementation BLOCKED** pending an approved strategy, boundaries and tests. |
| [docs/specifications/EXPORT_PROFILES.md](docs/specifications/EXPORT_PROFILES.md) | Exists but **empty — SFT/DPO/RAG/evaluation mapping BLOCKED** pending each approved output contract. |
| [docs/architecture/DATASET_FOUNDRY.md](docs/architecture/DATASET_FOUNDRY.md) and [docs/architecture/PIPELINE.md](docs/architecture/PIPELINE.md) | Both exist but are **empty — architecture and stage transitions not ratified**. |
| [docs/adr/ADR-0001.md](docs/adr/ADR-0001.md) | Exists but **empty — no ADR decision can be cited from it**. |
| [docs/examples/PIPELINE.md](docs/examples/PIPELINE.md) | Exists but **empty — no executable example is available**. |
| [tests/](tests/) | Five named pipeline-stage test files exist but are zero-byte placeholders on this base. No meaningful stage coverage may be claimed. |
| [.github/agents/dataset-foundry-assistant.agent.md](.github/agents/dataset-foundry-assistant.agent.md) | Agent definition exists on `main`; its activation, branch workflow and effective enforcement have not been verified. |
| [.gitignore](.gitignore) | This proposed change adds Python/cache/build exclusions. Ignore rules do not retroactively untrack committed files. |

Do not link to `docs/PROJECT_MANIFEST.md`, `docs/ARCHITECTURE.md`, or `docs/runbooks/` as existing sources: they are not present in this base. No initialized `.specify/` workspace or completed Spec Kit feature packet has been verified.

## Specification-first operating rule

1. Read the relevant real specification, architecture document and ADR before implementing a domain behavior. **An empty document is a blocked contract, not permission to invent its contents.** Work on clarifying that document may proceed; implementation of its dependent behavior must wait for human approval.
2. Define user scenarios, inputs and outputs, invariants, positive/negative/boundary/failure acceptance cases, provenance and rights decisions, and reproducibility expectations. Significant design choices require a reviewed ADR before implementation.
3. Prefer small, reviewable, config-driven changes and composition. Preserve source originals, carry evidence and lineage across transitions, and retain rejection reasons. Do not add dataset-specific hidden behavior or represent a placeholder as a feature.
4. License/provenance admission must fail closed: missing, incompatible, conflicting, or unresolved evidence must not silently authorize composition, export, or publication. Do not assert legal permissions from a publicly accessible URL alone.
5. Keep technical and governance documentation in sync with code. When a spec, ADR, tooling repair or stage merges, update its state in this inventory in the **same PR**. Re-check against the actual base; do not mark a proposed document as ratified by its mere existence.

These block rules apply to the corresponding domain feature, not to independent narrowly scoped maintenance, documentation, or packaging verification.

## Commands actually used by CI

The following command invocations are copied from [.github/workflows/ci.yml](.github/workflows/ci.yml), not hypothetical project tooling. Its `Install dependencies` step tries the editable dev install and falls back to the base install; it also installs `requirements.txt` or `requirements-dev.txt` when present and installs the core QA tools.

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]" || python -m pip install -e .
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m pip install pytest pytest-cov ruff mypy bandit pip-audit
```

The two requirements commands above are conditional on file existence in CI; the last command is displayed on one line for readability, whereas CI continues it with shell backslashes. Do not assume an unlisted requirements file exists.

```bash
ruff check .
ruff format --check .
mypy .
bandit -q -r .
pip-audit
pytest -q --maxfail=1 --disable-warnings \
  --cov=. \
  --cov-report=term-missing \
  --cov-report=xml
```

Use these checks locally where available, but report **passing** only when GitHub Actions has executed the relevant check against the exact proposed commit. A successful wheel/editable install or a package smoke test is not proof of loader, licence, chunking, exporter or pipeline correctness. Do not remove or skip QA/security gates to force a green result.

## Unresolved decisions — do not silently select defaults

| Topic | Current evidence / required decision |
| --- | --- |
| Contract-model library | Previous instructions named Pydantic, but current runtime dependencies are empty. Decide whether/where Pydantic is required in a spec/ADR before introducing it. |
| CLI entry point | No declared project script or executable CLI contract in `pyproject.toml`. Decide interface, invocation and errors before implementation. |
| Chunking | Structure-aware or semantic segmentation is a goal, but algorithm, boundaries, context retention, determinism and evaluation are not approved. |
| Rights policy | Licence evidence, intended-use compatibility, human review, escalation and reassessment semantics require the licence specification. Default to non-admission on uncertainty. |
| Dataset identity | Record/manifest schemas, canonicalization, digest/version policy, storage and replay are not approved. |
| Copilot agent / branch workflow | An agent definition exists on `main`; confirm intended branch ownership, integration and review process separately. File presence does not establish runtime behavior or mandatory enforcement. |
| Publication/export | No approved destination-authority, export profiles or release gate. No automatic remote publication. |

## Non-negotiable guardrails

- Do not claim tests, security scans, reproducibility or policy compliance without supporting execution/evidence tied to the exact revision.
- Do not write directly to `main`, self-approve, auto-merge, force-push, bypass review, or weaken, skip, mute, remove or loosen tests, lint, formatting, typing, dependency audits, security scanners or policy gates to obtain green CI.
- Do not commit passwords, tokens, credentials, sensitive dataset content, local virtual environments, bytecode, caches, `*.egg-info/`, build or coverage outputs. `.gitignore` helps avoid new accidental files; check `git status`/the PR diff because tracked artifacts remain tracked.
- No undocumented network ingestion, remote publishing, changing permissions, repository settings, releases, deployments or infrastructure as a side effect of a documentation or scaffold change.
- Record source rights, provenance, transformations and rejected outcomes; intent or a download link is not authority to use data.
- Limit changes to the approved scope; make assumptions and uncertainty explicit and give rollback instructions.

## Definition of done

A feature is done only when: its specification (and required ADR) is non-empty and approved; implementation matches measurable acceptance criteria; tests cover positive, negative, boundary and failure cases for each affected stage (or clearly justify why a case is inapplicable); provenance, admission, rejection, lineage and output evidence are demonstrable as appropriate; the diff is scoped and reviewable; and **exact-head CI** evidence for every required check is attached or its gap clearly stated. A human must review and approve the merge. Documentation-only PRs must validate their claims and links, but do not count as implemented domain capabilities.

## Tooling gaps to keep visible

- `.pre-commit-config.yaml` is empty; no pre-commit enforcement is established.
- `.gitignore` prevents accidental new local artifacts after this change, but neither validates source content nor untracks existing files.
- Empty `lint.yml` and `release.yml` workflow placeholders exist on this base. Their separate cleanup is under review; do not portray them as functioning gates or change them to conceal failures.
- CI covers the commands listed above but does not, by itself, demonstrate a dedicated secret scanner, formal spec validation, full domain coverage or an initialized Spec Kit workflow.
- The current base CI test stage fails with the zero-byte test placeholders. A separate draft package smoke-test PR is not merged into this baseline and cannot be cited as current `main` domain validation.

**Maintenance rule:** Every PR that resolves one of these gaps must update the corresponding status here, with the matching code, file or exact-commit evidence. Do not let this file become an aspirational status report.
