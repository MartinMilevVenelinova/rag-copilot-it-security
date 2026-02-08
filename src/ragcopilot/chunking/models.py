from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib


@dataclass(frozen=True)
class Heading:
    level: int              # 1..6
    title: str              # raw heading text


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    source: str                    # e.g., file path or URL
    chunk_id: str                  # deterministic
    index: int                     # 0..N-1 deterministic order

    text: str

    # structure
    headings: List[Heading] = field(default_factory=list)   # stack from H1..Hx
    heading_path: str = ""                                 # "H1 > H2 > H3"

    # traceability (best-effort; offsets are in the normalized text used for chunking)
    start_char: int = 0
    end_char: int = 0

    # optional: helpful for filtering / retrieval
    meta: Dict[str, Any] = field(default_factory=dict)

    def fingerprint(self) -> str:
        """
        Stable fingerprint of the chunk content + structural context.
        Useful for caching and regression tests.
        """
        h = hashlib.sha1()
        h.update(self.doc_id.encode("utf-8"))
        h.update(b"\n")
        h.update(self.source.encode("utf-8"))
        h.update(b"\n")
        h.update(self.heading_path.encode("utf-8"))
        h.update(b"\n")
        h.update(self.text.encode("utf-8"))
        return h.hexdigest()


def make_deterministic_chunk_id(doc_id: str, source: str, heading_path: str, index: int, text: str) -> str:
    """
    Deterministic ID: same doc+source+heading_path+index+text => same chunk_id.
    """
    h = hashlib.sha1()
    h.update(doc_id.encode("utf-8"))
    h.update(b"|")
    h.update(source.encode("utf-8"))
    h.update(b"|")
    h.update(heading_path.encode("utf-8"))
    h.update(b"|")
    h.update(str(index).encode("utf-8"))
    h.update(b"|")
    h.update(text.encode("utf-8"))
    return h.hexdigest()
