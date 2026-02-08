from pathlib import Path

from ragcopilot.ingestion.service import ingest


def test_ingest_new_then_unchanged_then_modified(tmp_path: Path):
    root = tmp_path / "docs"
    root.mkdir()

    manifest_path = tmp_path / "document_manifest.json"

    # First run -> new
    (root / "a.md").write_text("hello", encoding="utf-8")
    r1 = ingest(root, manifest_path)
    assert len(r1.new) == 1
    assert len(r1.modified) == 0
    assert len(r1.unchanged) == 0

    # Second run -> unchanged
    r2 = ingest(root, manifest_path)
    assert len(r2.new) == 0
    assert len(r2.modified) == 0
    assert len(r2.unchanged) == 1

    # Modify file -> modified
    (root / "a.md").write_text("hello!!", encoding="utf-8")
    r3 = ingest(root, manifest_path)
    assert len(r3.new) == 0
    assert len(r3.modified) == 1
    assert len(r3.unchanged) == 0
