from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


def utc_now_iso() -> str:
    # deterministic-ish timestamp format (no microseconds)
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class Source:
    source_type: str  # e.g. "filesystem"
    uri: str          # e.g. "policies/incident_response.md" (posix style)


@dataclass(frozen=True)
class Document:
    doc_id: str
    source: Source

    content_hash: str
    fingerprint: str

    size_bytes: int
    mtime_epoch: int  # integer seconds for determinism
    mime_type: str

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Manifest:
    schema_version: str
    created_at: str
    root_uri: str  # e.g. "data/documents" (posix)
    documents: List[Document] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "created_at": self.created_at,
            "root_uri": self.root_uri,
            "documents": [
                {
                    "doc_id": d.doc_id,
                    "source": {
                        "source_type": d.source.source_type,
                        "uri": d.source.uri,
                    },
                    "content_hash": d.content_hash,
                    "fingerprint": d.fingerprint,
                    "size_bytes": d.size_bytes,
                    "mtime_epoch": d.mtime_epoch,
                    "mime_type": d.mime_type,
                    "metadata": d.metadata,
                }
                for d in self.documents
            ],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Manifest":
        docs: List[Document] = []
        for item in data.get("documents", []):
            src = Source(
                source_type=item["source"]["source_type"],
                uri=item["source"]["uri"],
            )
            docs.append(
                Document(
                    doc_id=item["doc_id"],
                    source=src,
                    content_hash=item["content_hash"],
                    fingerprint=item["fingerprint"],
                    size_bytes=int(item["size_bytes"]),
                    mtime_epoch=int(item["mtime_epoch"]),
                    mime_type=item["mime_type"],
                    metadata=dict(item.get("metadata", {})),
                )
            )

        return Manifest(
            schema_version=data["schema_version"],
            created_at=data["created_at"],
            root_uri=data["root_uri"],
            documents=docs,
        )
