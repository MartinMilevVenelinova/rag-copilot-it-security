import pytest
from dataclasses import dataclass

from ragcopilot.retrieval.models import (
    RetrievalFilter,
    RetrievalQuery,
    RetrievedChunk,
    RetrievalTrace,
    RetrievalResult,
)


@dataclass(frozen=True)
class StubChunk:
    chunk_id: str
    meta: dict


def test_query_validation() -> None:
    with pytest.raises(ValueError):
        RetrievalQuery(text="   ", k=5)
    with pytest.raises(ValueError):
        RetrievalQuery(text="hello", k=0)
    q = RetrievalQuery(text="hello", k=3)
    assert q.k == 3


def test_filter_normalization_is_deterministic() -> None:
    f = RetrievalFilter.from_values(doc_type="pdf", tags=[" b ", "a", "a", "", "  "])
    assert f.doc_type == "pdf"
    assert f.tags == ("a", "b")
    assert f.summary() == {"doc_type": "pdf", "tags": ["a", "b"]}


def test_filter_matches_doc_type() -> None:
    f = RetrievalFilter.from_values(doc_type="md")
    assert f.matches_meta({"doc_type": "md"}) is True
    assert f.matches_meta({"doc_type": "pdf"}) is False
    assert f.matches_meta({}) is False


def test_filter_matches_tags_all_required() -> None:
    f = RetrievalFilter.from_values(tags=["a", "b"])
    assert f.matches_meta({"tags": ["a", "b", "c"]}) is True
    assert f.matches_meta({"tags": ["a"]}) is False
    assert f.matches_meta({"tags": "a"}) is False  # string treated as single tag


def test_retrieved_chunk_exposes_chunk_id() -> None:
    c = StubChunk(chunk_id="c1", meta={})
    rc = RetrievedChunk(chunk=c, score=0.5)
    assert rc.chunk_id == "c1"


def test_trace_from_results_contains_expected_pairs() -> None:
    c1 = StubChunk(chunk_id="c1", meta={})
    c2 = StubChunk(chunk_id="c2", meta={})
    r1 = RetrievedChunk(chunk=c1, score=0.9)
    r2 = RetrievedChunk(chunk=c2, score=0.8)

    filt = RetrievalFilter.from_values(doc_type="md", tags=["x"])
    trace = RetrievalTrace.from_results([r1, r2], filt)

    assert trace.selected == (("c1", 0.9), ("c2", 0.8))
    assert trace.filters == {"doc_type": "md", "tags": ["x"]}


def test_retrieval_result_is_immutable_tuple() -> None:
    c = StubChunk(chunk_id="c1", meta={})
    item = RetrievedChunk(chunk=c, score=1.0)
    trace = RetrievalTrace.from_results([item], None)

    res = RetrievalResult(items=(item,), trace=trace)
    assert isinstance(res.items, tuple)
    assert res.items[0].chunk_id == "c1"
