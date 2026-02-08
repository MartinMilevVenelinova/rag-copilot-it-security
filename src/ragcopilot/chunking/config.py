from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkingConfig:
    max_tokens: int = 320
    overlap_tokens: int = 40
    min_tokens: int = 60

    keep_heading_lines: bool = False   # v1: usually false; headings stored in metadata not embedded in text
    normalize_whitespace: bool = True
