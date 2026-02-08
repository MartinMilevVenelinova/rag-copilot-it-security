from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from ragcopilot.ingestion.models import Manifest, Document, utc_now_iso
from ragcopilot.ingestion.scanner import scan_documents
from ragcopilot.ingestion.manifest_store import read_manifest, write_manifest


@dataclass(frozen=True)
class IngestionResult:
    manifest: Manifest
    new: List[Document]
    modified: List[Document]
    unchanged: List[Document]


def _index_by_doc_id(docs: List[Document]) -> Dict[str, Document]:
    return {d.doc_id: d for d in docs}


def build_manifest(root_dir: Path) -> Manifest:
    docs = scan_documents(root_dir=root_dir)
    return Manifest(
        schema_version="1.0",
        created_at=utc_now_iso(),
        root_uri=root_dir.as_posix(),
        documents=docs,
    )


def ingest(root_dir: Path, manifest_path: Path) -> IngestionResult:
    previous = read_manifest(manifest_path)
    current = build_manifest(root_dir)

    prev_docs = _index_by_doc_id(previous.documents) if previous else {}
    cur_docs = _index_by_doc_id(current.documents)

    new: List[Document] = []
    modified: List[Document] = []
    unchanged: List[Document] = []

    for doc_id, doc in cur_docs.items():
        old = prev_docs.get(doc_id)
        if old is None:
            new.append(doc)
        else:
            if old.content_hash != doc.content_hash:
                modified.append(doc)
            else:
                unchanged.append(doc)

    # Deterministic ordering
    key = lambda d: d.source.uri
    new.sort(key=key)
    modified.sort(key=key)
    unchanged.sort(key=key)

    write_manifest(manifest_path, current)

    return IngestionResult(
        manifest=current,
        new=new,
        modified=modified,
        unchanged=unchanged,
    )
