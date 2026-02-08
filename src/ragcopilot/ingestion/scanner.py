from __future__ import annotations

from pathlib import Path
from typing import List, Sequence
import mimetypes

from ragcopilot.ingestion.models import Document, Source
from ragcopilot.ingestion.hashing import (
    sha256_hex,
    compute_doc_id,
    compute_fingerprint,
)


DEFAULT_EXTENSIONS: Sequence[str] = (".md", ".txt", ".pdf")
DEFAULT_EXCLUDE_DIRS: Sequence[str] = (".git", "__pycache__", ".venv")


def _is_excluded(path: Path, exclude_dirs: Sequence[str]) -> bool:
    return any(part in exclude_dirs for part in path.parts)


def _to_posix_relative(root: Path, file_path: Path) -> str:
    return file_path.relative_to(root).as_posix()


def _guess_mime_type(file_path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(file_path))
    return mime or "application/octet-stream"


def scan_documents(
    root_dir: Path,
    include_extensions: Sequence[str] = DEFAULT_EXTENSIONS,
    exclude_dirs: Sequence[str] = DEFAULT_EXCLUDE_DIRS,
) -> List[Document]:
    if not root_dir.exists() or not root_dir.is_dir():
        raise ValueError(f"Invalid root directory: {root_dir}")

    documents: List[Document] = []

    files = [
        p
        for p in root_dir.rglob("*")
        if p.is_file()
        and p.suffix.lower() in include_extensions
        and not _is_excluded(p, exclude_dirs)
    ]

    # Deterministic order
    files.sort(key=lambda p: _to_posix_relative(root_dir, p))

    for file_path in files:
        rel_posix = _to_posix_relative(root_dir, file_path)
        source = Source(source_type="filesystem", uri=rel_posix)

        content = file_path.read_bytes()
        content_hash = sha256_hex(content)

        doc_id = compute_doc_id(source.source_type, source.uri)
        fingerprint = compute_fingerprint(doc_id, content_hash)

        stat = file_path.stat()

        documents.append(
            Document(
                doc_id=doc_id,
                source=source,
                content_hash=content_hash,
                fingerprint=fingerprint,
                size_bytes=int(stat.st_size),
                mtime_epoch=int(stat.st_mtime),
                mime_type=_guess_mime_type(file_path),
                metadata={},
            )
        )

    return documents
