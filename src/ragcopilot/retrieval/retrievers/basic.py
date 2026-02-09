from __future__ import annotations

from ..interfaces import EmbeddingProvider, Retriever, VectorIndex
from ..models import RetrievalQuery, RetrievalResult, RetrievalTrace


class BasicRetriever(Retriever):
    """
    Baseline retriever (v1):
    - Embed query text
    - Vector search top-k
    - Return RetrievalResult with trace
    """

    def __init__(self, *, index: VectorIndex, embedder: EmbeddingProvider) -> None:
        self._index = index
        self._embedder = embedder

    def retrieve(self, query: RetrievalQuery) -> RetrievalResult:
        qvec = self._embedder.embed(query.text)
        items = tuple(
            self._index.search(
                vector=qvec,
                k=query.k,
                filters=query.filters,
            )
        )
        trace = RetrievalTrace.from_results(items, query.filters)
        return RetrievalResult(items=items, trace=trace)