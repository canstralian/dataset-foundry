"""Base plugin interface for dataset normalizers.

Normalizers transform raw Records into a consistent representation
(e.g. cleaning whitespace, standardizing QA pairs, formatting code) prior
to chunking.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from dataset_foundry.types import Record


class BaseNormalizer(ABC):
    """Abstract base class for all dataset normalizers."""

    @abstractmethod
    def normalize(self, record: Record) -> Record:
        """Return a normalized copy of ``record``."""
        raise NotImplementedError
