from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Protocol, Sequence

from .models import RetrievedChunk, RetrievalFilter, RetrievalQuery


class EmbeddingProvider(Protocol):
    """
    Produces vector embeddings for text.

    Interface only — implementation lives elsewhere.
    """

    def embed(self, text: str) -> Sequence[float]:
        ...


class VectorIndex(ABC):
    """
    Abstract vector index for similarity search.
    """

    @abstractmethod
    def upsert(
        self,
        *,
        chunks: Iterable[object],
        vectors: Iterable[Sequence[float]],
    ) -> None:
        """
        Insert or update chunks with their vectors.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        *,
        vector: Sequence[float],
        k: int,
        filters: RetrievalFilter | None = None,
    ) -> Sequence[RetrievedChunk]:
        """
        Return top-k similar chunks for the given vector.
        """
        raise NotImplementedError


class Retriever(ABC):
    """
    High-level retrieval interface.
    """

    @abstractmethod
    def retrieve(
        self,
        query: RetrievalQuery,
    ) -> Sequence[RetrievedChunk]:
        raise NotImplementedError
