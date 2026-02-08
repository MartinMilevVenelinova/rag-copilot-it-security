from pathlib import Path

from ragcopilot.ingestion.scanner import scan_documents


def test_scan_documents_finds_files(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    (docs_dir / "a.md").write_text("hello", encoding="utf-8")
    (docs_dir / "b.txt").write_text("world", encoding="utf-8")

    docs = scan_documents(docs_dir)

    assert len(docs) == 2
    assert docs[0].source.uri == "a.md"
    assert docs[1].source.uri == "b.txt"
