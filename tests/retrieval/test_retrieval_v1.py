from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ragcopilot.retrieval.index.in_memory import InMemoryCosineVectorIndex
from ragcopilot.retrieval.models import RetrievalFilter, RetrievalQuery
from ragcopilot.retrieval.retrievers.basic import BasicRetriever


@dataclass(frozen=True)
class StubChunk:
    chunk_id: str
    meta: dict


class StubEmbedder:
    def __init__(self, mapping: dict[str, Sequence[float]]) -> None:
        self._mapping = mapping

    def embed(self, text: str) -> Sequence[float]:
        return self._mapping[text]


def test_returns_exactly_top_k() -> None:
    idx = InMemoryCosineVectorIndex()
    chunks = [
        StubChunk("c1", {"doc_type": "md", "tags": ["a"]}),
        StubChunk("c2", {"doc_type": "md", "tags": ["a", "b"]}),
        StubChunk("c3", {"doc_type": "pdf", "tags": ["b"]}),
    ]
    # Query vector = [1, 0]
    vectors = [
        [1, 0],   # c1 sim 1.0
        [0.8, 0], # c2 sim 1.0 (same direction)
        [0, 1],   # c3 sim 0.0
    ]
    idx.upsert(chunks=chunks, vectors=vectors)

    retriever = BasicRetriever(index=idx, embedder=StubEmbedder({"q": [1, 0]}))
    res = retriever.retrieve(RetrievalQuery(text="q", k=2))

    assert len(res.items) == 2
    assert [it.chunk.chunk_id for it in res.items] == ["c1", "c2"]


def test_tie_break_determinism_chunk_id_asc() -> None:
    idx = InMemoryCosineVectorIndex()
    # Both vectors are identical direction => same cosine score
    c_a = StubChunk("a10", {"doc_type": "md", "tags": []})
    c_b = StubChunk("a02", {"doc_type": "md", "tags": []})
    idx.upsert(chunks=[c_a, c_b], vectors=[[1, 0], [1, 0]])

    retriever = BasicRetriever(index=idx, embedder=StubEmbedder({"q": [1, 0]}))
    res = retriever.retrieve(RetrievalQuery(text="q", k=2))

    # same score, order by chunk_id asc => a02 then a10
    assert [it.chunk.chunk_id for it in res.items] == ["a02", "a10"]


def test_filter_doc_type() -> None:
    idx = InMemoryCosineVectorIndex()
    c1 = StubChunk("c1", {"doc_type": "md", "tags": ["a"]})
    c2 = StubChunk("c2", {"doc_type": "pdf", "tags": ["a"]})
    idx.upsert(chunks=[c1, c2], vectors=[[1, 0], [1, 0]])

    retriever = BasicRetriever(index=idx, embedder=StubEmbedder({"q": [1, 0]}))
    f = RetrievalFilter.from_values(doc_type="md")
    res = retriever.retrieve(RetrievalQuery(text="q", k=5, filters=f))

    assert [it.chunk.chunk_id for it in res.items] == ["c1"]


def test_filter_tags_all_required() -> None:
    idx = InMemoryCosineVectorIndex()
    c1 = StubChunk("c1", {"doc_type": "md", "tags": ["a"]})
    c2 = StubChunk("c2", {"doc_type": "md", "tags": ["a", "b"]})
    c3 = StubChunk("c3", {"doc_type": "md", "tags": ["b"]})
    idx.upsert(chunks=[c1, c2, c3], vectors=[[1, 0], [1, 0], [1, 0]])

    retriever = BasicRetriever(index=idx, embedder=StubEmbedder({"q": [1, 0]}))
    f = RetrievalFilter.from_values(tags=["a", "b"])
    res = retriever.retrieve(RetrievalQuery(text="q", k=10, filters=f))

    assert [it.chunk.chunk_id for it in res.items] == ["c2"]


def test_trace_contains_expected_scores_and_ids() -> None:
    idx = InMemoryCosineVectorIndex()
    c1 = StubChunk("c1", {"doc_type": "md", "tags": ["x"]})
    c2 = StubChunk("c2", {"doc_type": "md", "tags": ["x"]})
    idx.upsert(chunks=[c1, c2], vectors=[[1, 0], [0, 1]])

    retriever = BasicRetriever(index=idx, embedder=StubEmbedder({"q": [1, 0]}))
    f = RetrievalFilter.from_values(doc_type="md", tags=["x"])
    res = retriever.retrieve(RetrievalQuery(text="q", k=2, filters=f))

    assert [it.chunk.chunk_id for it in res.items] == ["c1", "c2"]
    assert res.trace.selected[0][0] == "c1"
    assert res.trace.filters == {"doc_type": "md", "tags": ["x"]}