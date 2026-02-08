from __future__ import annotations

from typing import List
from dataclasses import dataclass

from .config import ChunkingConfig
from .heading_parser import parse_markdown_headings
from .models import Chunk, Heading, make_deterministic_chunk_id


def heading_path(headings: List[Heading]) -> str:
    if not headings:
        return ""
    return " > ".join([h.title for h in headings])


def tokenize(text: str) -> List[str]:
    # Deterministic "tokenizer" for v1: whitespace split
    return [t for t in text.split() if t]


def detokenize(tokens: List[str]) -> str:
    return " ".join(tokens)


def window_tokens(tokens: List[str], max_tokens: int, overlap_tokens: int) -> List[List[str]]:
    if max_tokens <= 0:
        raise ValueError("max_tokens must be > 0")
    if overlap_tokens < 0:
        raise ValueError("overlap_tokens must be >= 0")
    if overlap_tokens >= max_tokens:
        raise ValueError("overlap_tokens must be < max_tokens")

    windows: List[List[str]] = []
    step = max_tokens - overlap_tokens
    i = 0
    n = len(tokens)

    while i < n:
        windows.append(tokens[i : i + max_tokens])
        i += step

    return windows


@dataclass(frozen=True)
class ChunkerInput:
    doc_id: str
    source: str
    text: str               # markdown or plain text (v1 handles markdown headings)
    doc_meta: dict | None = None


class HeadingAwareChunker:
    def __init__(self, config: ChunkingConfig):
        self.cfg = config

    def chunk(self, inp: ChunkerInput) -> List[Chunk]:
        full_norm, sections = parse_markdown_headings(inp.text)

        out: List[Chunk] = []
        global_index = 0

        for sec in sections:
            sec_text = sec.text
            if self.cfg.normalize_whitespace:
                sec_text = " ".join(sec_text.split())

            toks = tokenize(sec_text)
            if not toks:
                continue

            hp = heading_path(sec.headings)
            windows = window_tokens(toks, self.cfg.max_tokens, self.cfg.overlap_tokens)

            # Post-process: merge tiny last window
            if len(windows) >= 2 and len(windows[-1]) < self.cfg.min_tokens:
                windows[-2] = windows[-2] + windows[-1]
                windows.pop()

            # Build chunks
            running_char = 0  # best-effort offsets inside sec_text
            for w in windows:
                chunk_text = detokenize(w)
                # approximate offsets by searching forward (deterministic)
                start = sec_text.find(chunk_text, running_char)
                if start == -1:
                    # fallback: monotonic best effort
                    start = running_char
                end = start + len(chunk_text)
                running_char = end

                chunk_id = make_deterministic_chunk_id(
                    doc_id=inp.doc_id,
                    source=inp.source,
                    heading_path=hp,
                    index=global_index,
                    text=chunk_text,
                )

                meta = dict(inp.doc_meta or {})
                meta.update(
                    {
                        "heading_path": hp,
                        "heading_levels": [h.level for h in sec.headings],
                        "heading_titles": [h.title for h in sec.headings],
                        "section_start_char": sec.start_char,
                        "section_end_char": sec.end_char,
                    }
                )

                out.append(
                    Chunk(
                        doc_id=inp.doc_id,
                        source=inp.source,
                        chunk_id=chunk_id,
                        index=global_index,
                        text=chunk_text,
                        headings=sec.headings,
                        heading_path=hp,
                        start_char=start,
                        end_char=end,
                        meta=meta,
                    )
                )
                global_index += 1

        return out
