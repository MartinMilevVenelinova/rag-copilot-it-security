from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from ..models import RetrievedChunk, RetrievalFilter
from ..interfaces import VectorIndex


def _as_tuple(vec: Sequence[float]) -> Tuple[float, ...]:
    return tuple(float(x) for x in vec)


def _dot(a: Tuple[float, ...], b: Tuple[float, ...]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(a: Tuple[float, ...]) -> float:
    return sqrt(_dot(a, a))


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """
    Deterministic cosine similarity.
    Returns 0.0 if any vector is zero-norm.
    """
    at = _as_tuple(a)
    bt = _as_tuple(b)
    if len(at) != len(bt):
        raise ValueError("Vectors must have the same dimensionality.")

    na = _norm(at)
    nb = _norm(bt)
    if na == 0.0 or nb == 0.0:
        return 0.0

    return _dot(at, bt) / (na * nb)


def _chunk_id(chunk: Any) -> str:
    cid = getattr(chunk, "chunk_id", None)
    if cid is None:
        raise AttributeError("Chunk object must have attribute 'chunk_id'.")
    return str(cid)


def _chunk_meta(chunk: Any) -> Mapping[str, Any]:
    meta = getattr(chunk, "meta", None)
    if meta is None:
        return {}
    if not isinstance(meta, Mapping):
        raise TypeError("Chunk.meta must be a mapping/dict.")
    return meta


@dataclass(frozen=True, slots=True)
class _Entry:
    chunk: Any
    vector: Tuple[float, ...]


class InMemoryCosineVectorIndex(VectorIndex):
    """
    Naive in-memory cosine similarity index (v1).

    - Stores vectors by chunk_id.
    - Deterministic sorting: score desc, then chunk_id asc.
    - Filters applied during scoring pass (v1 simplest + testable).
    """

    def __init__(self) -> None:
        self._by_id: Dict[str, _Entry] = {}

    def upsert(
        self,
        *,
        chunks: Iterable[object],
        vectors: Iterable[Sequence[float]],
    ) -> None:
        for ch, vec in zip(chunks, vectors):
            cid = _chunk_id(ch)
            vt = _as_tuple(vec)
            self._by_id[cid] = _Entry(chunk=ch, vector=vt)

    def search(
        self,
        *,
        vector: Sequence[float],
        k: int,
        filters: RetrievalFilter | None = None,
    ) -> Sequence[RetrievedChunk]:
        if k <= 0:
            raise ValueError("k must be a positive integer.")

        qv = _as_tuple(vector)

        scored: List[RetrievedChunk] = []
        for cid, entry in self._by_id.items():
            meta = _chunk_meta(entry.chunk)
            if filters is not None and not filters.matches_meta(meta):
                continue

            score = cosine_similarity(qv, entry.vector)
            scored.append(RetrievedChunk(chunk=entry.chunk, score=float(score)))

        # Deterministic ranking: score desc, then chunk_id asc for ties
        scored.sort(key=lambda r: (-r.score, r.chunk_id))

        return scored[:k]