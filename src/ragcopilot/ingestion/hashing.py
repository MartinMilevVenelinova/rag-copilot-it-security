from __future__ import annotations

import hashlib


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_hex_str(text: str) -> str:
    return sha256_hex(text.encode("utf-8"))


def compute_doc_id(source_type: str, source_uri_posix: str) -> str:
    """
    Stable document identifier tied to its source location.
    For filesystem: source_uri_posix should be a POSIX-style relative path.
    """
    return sha256_hex_str(f"{source_type}:{source_uri_posix}")


def compute_fingerprint(doc_id: str, content_hash: str) -> str:
    """
    Stable fingerprint for a specific version/state of a document.
    """
    return sha256_hex_str(f"{doc_id}:{content_hash}")
