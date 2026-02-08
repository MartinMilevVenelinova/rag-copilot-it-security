from pathlib import Path

from ragcopilot.ingestion.manifest_store import write_manifest, read_manifest
from ragcopilot.ingestion.models import Manifest, Document, Source


def test_manifest_roundtrip(tmp_path: Path):
    path = tmp_path / "document_manifest.json"

    manifest = Manifest(
        schema_version="1.0",
        created_at="2026-01-01T00:00:00+00:00",
        root_uri="data/documents",
        documents=[
            Document(
                doc_id="id",
                source=Source(source_type="filesystem", uri="a.md"),
                content_hash="c" * 64,
                fingerprint="f" * 64,
                size_bytes=1,
                mtime_epoch=123,
                mime_type="text/markdown",
                metadata={"tag": "x"},
            )
        ],
    )

    write_manifest(path, manifest)
    loaded = read_manifest(path)

    assert loaded is not None
    assert loaded.schema_version == "1.0"
    assert loaded.documents[0].source.uri == "a.md"
    assert loaded.documents[0].metadata["tag"] == "x"
