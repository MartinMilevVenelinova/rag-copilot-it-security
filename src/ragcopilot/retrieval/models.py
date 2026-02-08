from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Optional, Sequence, Tuple


Chunk = Any  # v1: keep models decoupled from the concrete chunk implementation


@dataclass(frozen=True, slots=True)
class RetrievalFilter:
    """
    Basic filters supported in v1.

    - doc_type: exact match on chunk meta field "doc_type"
    - tags: requires all filter tags to be present in chunk meta field "tags"
    """
    doc_type: Optional[str] = None
    tags: Tuple[str, ...] = ()

    def summary(self) -> dict:
        return {
            "doc_type": self.doc_type,
            "tags": list(self.tags),
        }

    @staticmethod
    def _normalize_tags(tags: Iterable[str]) -> Tuple[str, ...]:
        # Deterministic normalization: unique + sorted
        cleaned = {t.strip() for t in tags if t and t.strip()}
        return tuple(sorted(cleaned))

    @classmethod
    def from_values(
        cls,
        doc_type: Optional[str] = None,
        tags: Optional[Iterable[str]] = None,
    ) -> "RetrievalFilter":
        norm_tags = cls._normalize_tags(tags or [])
        return cls(doc_type=doc_type, tags=norm_tags)

    def matches_meta(self, meta: Mapping[str, Any]) -> bool:
        if self.doc_type is not None:
            if meta.get("doc_type") != self.doc_type:
                return False

        if self.tags:
            meta_tags = meta.get("tags") or []
            if isinstance(meta_tags, str):
                meta_tag_set = {meta_tags}
            else:
                meta_tag_set = {str(t) for t in meta_tags}

            # v1 rule: chunk must contain ALL requested tags
            for t in self.tags:
                if t not in meta_tag_set:
                    return False

        return True


@dataclass(frozen=True, slots=True)
class RetrievalQuery:
    text: str
    k: int = 5
    filters: Optional[RetrievalFilter] = None

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("RetrievalQuery.text must be a non-empty string.")
        if not isinstance(self.k, int) or self.k <= 0:
            raise ValueError("RetrievalQuery.k must be a positive integer.")


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    chunk: Chunk
    score: float

    @property
    def chunk_id(self) -> str:
        # We require chunks to expose chunk_id for deterministic tie-breaks.
        cid = getattr(self.chunk, "chunk_id", None)
        if cid is None:
            raise AttributeError("Chunk object must have attribute 'chunk_id'.")
        return str(cid)


@dataclass(frozen=True, slots=True)
class RetrievalTrace:
    """
    Captures how retrieval selected results.

    selected: ordered list of (chunk_id, score) for returned chunks.
    filters: normalized filter summary (if any).
    """
    selected: Tuple[Tuple[str, float], ...] = ()
    filters: dict = field(default_factory=dict)

    @classmethod
    def from_results(
        cls,
        results: Sequence[RetrievedChunk],
        filters: Optional[RetrievalFilter],
    ) -> "RetrievalTrace":
        selected = tuple((r.chunk_id, float(r.score)) for r in results)
        return cls(
            selected=selected,
            filters=(filters.summary() if filters else {}),
        )


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    items: Tuple[RetrievedChunk, ...]
    trace: RetrievalTrace
