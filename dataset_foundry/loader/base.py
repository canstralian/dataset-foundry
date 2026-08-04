"""Base plugin interface for dataset loaders.

Loaders fetch raw content from a source (local, GitHub, Hugging Face, etc.)
and yield ``Record`` instances. New source types are added by implementing
this interface, not by branching inside the pipeline (plugin-first
architecture).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

from dataset_foundry.types import Record


class BaseLoader(ABC):
    """Abstract base class for all dataset loaders."""

    def __init__(self, uri: str, **options: object) -> None:
        self.uri = uri
        self.options = options

    @abstractmethod
    def load(self) -> Iterator[Record]:
        """Yield Record instances loaded from ``self.uri``."""
        raise NotImplementedError
