"""Core shared type definitions and contracts for Dataset Foundry.

These Pydantic models define the data contracts passed between pipeline
stages (loader -> normalizer -> chunker -> classifier -> dedupe ->
license_gate -> quality -> exporter). Keeping these contracts centralized
ensures every stage can be developed and tested independently
(plugin-first architecture).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    """A single piece of evidence supporting a transformation or record."""

    source: str
    detail: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Record(BaseModel):
    """A single unit of dataset content flowing through the pipeline."""

    id: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    license: str | None = None
    evidence: list[Evidence] = Field(default_factory=list)

    def with_evidence(self, source: str, detail: str) -> "Record":
        """Return a copy of this record with an additional evidence entry."""
        return self.model_copy(
            update={"evidence": [*self.evidence, Evidence(source=source, detail=detail)]}
        )


class Chunk(BaseModel):
    """A semantically chunked unit derived from a Record."""

    id: str
    record_id: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class QualityScore(BaseModel):
    """Quality assessment for a record or chunk."""

    target_id: str
    score: float = Field(ge=0.0, le=1.0)
    metrics: dict[str, float] = Field(default_factory=dict)
