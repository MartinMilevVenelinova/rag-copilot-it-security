from ragcopilot.ingestion.hashing import (
    sha256_hex_str,
    compute_doc_id,
    compute_fingerprint,
)


def test_sha256_hex_str_is_deterministic():
    assert sha256_hex_str("hello") == sha256_hex_str("hello")
    assert sha256_hex_str("hello") != sha256_hex_str("hello!")


def test_doc_id_changes_with_uri():
    doc_id_1 = compute_doc_id("filesystem", "a/b.md")
    doc_id_2 = compute_doc_id("filesystem", "a/c.md")
    assert doc_id_1 != doc_id_2


def test_fingerprint_changes_with_content_hash():
    doc_id = compute_doc_id("filesystem", "a/b.md")

    fp_1 = compute_fingerprint(doc_id, "x" * 64)
    fp_2 = compute_fingerprint(doc_id, "y" * 64)

    assert fp_1 != fp_2
