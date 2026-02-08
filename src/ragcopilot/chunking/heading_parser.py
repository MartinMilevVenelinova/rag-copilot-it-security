from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import re

from .models import Heading


@dataclass(frozen=True)
class Section:
    headings: List[Heading]   # heading stack at this section
    text: str                 # content under the last heading (excluding heading line)
    start_char: int           # offset in full normalized doc text
    end_char: int


_MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)\s*$")


def normalize_text(text: str) -> str:
    # deterministic normalization
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text


def parse_markdown_headings(md_text: str) -> Tuple[str, List[Section]]:
    """
    Returns:
      normalized_full_text, sections[] split by headings.
    Deterministic: same input => same sections.
    """
    full = normalize_text(md_text)
    lines = full.split("\n")

    sections: List[Section] = []
    heading_stack: List[Heading] = []

    # We'll build sections by accumulating content lines after a heading.
    current_start = 0
    current_content_lines: List[str] = []
    current_section_headings: List[Heading] = heading_stack.copy()

    # Track char offsets in the normalized full string
    # We'll compute offsets by iterating lines and maintaining a cursor.
    cursor = 0  # char index at start of current line

    def flush_section(end_cursor: int) -> None:
        nonlocal current_start, current_content_lines, current_section_headings
        text = "\n".join(current_content_lines).strip("\n")
        if text.strip():
            sections.append(
                Section(
                    headings=current_section_headings.copy(),
                    text=text,
                    start_char=current_start,
                    end_char=end_cursor,
                )
            )
        current_content_lines = []
        current_start = end_cursor
        current_section_headings = heading_stack.copy()

    for i, line in enumerate(lines):
        m = _MD_HEADING_RE.match(line)
        line_len = len(line) + (1 if i < len(lines) - 1 else 0)  # include '\n' except last line

        if m:
            # flush previous section up to current cursor
            flush_section(cursor)

            level = len(m.group(1))
            title = m.group(2).strip()

            # update heading stack
            while heading_stack and heading_stack[-1].level >= level:
                heading_stack.pop()
            heading_stack.append(Heading(level=level, title=title))

            # move cursor past this heading line
            cursor += line_len
            current_start = cursor
            current_section_headings = heading_stack.copy()
            continue

        # normal content line
        current_content_lines.append(line)
        cursor += line_len

    # flush trailing section
    flush_section(cursor)

    if not sections:
        # fallback: whole doc as one section (no headings)
        whole = full.strip("\n")
        if whole.strip():
            sections = [Section(headings=[], text=whole, start_char=0, end_char=len(full))]

    return full, sections
