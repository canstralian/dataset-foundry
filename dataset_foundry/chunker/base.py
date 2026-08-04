"""Base plugin interface for semantic chunkers.

Per repository principle "semantic chunking over fixed token chunking",
chunkers split a Record into meaningful Chunk units based on structure
(AST, markdown headings, conversation turns) rather than arbitrary token
windows.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

from dataset_foundry.types import Chunk, Record


class BaseChunker(ABC):
    """Abstract base class for all semantic chunkers."""

    @abstractmethod
    def chunk(self, record: Record) -> Iterator[Chunk]:
        """Yield Chunk instances derived from ``record``."""
        raise NotImplementedError
