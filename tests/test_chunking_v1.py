from ragcopilot.chunking import ChunkingConfig, HeadingAwareChunker, ChunkerInput


def test_heading_aware_chunking_preserves_heading_path():
    md = """# Title
Intro text here.

## Install
Step one step two step three.

## Usage
Run the tool and check output.
"""
    cfg = ChunkingConfig(max_tokens=10, overlap_tokens=2, min_tokens=3)
    chunker = HeadingAwareChunker(cfg)

    chunks = chunker.chunk(ChunkerInput(doc_id="doc1", source="file.md", text=md))
    assert len(chunks) > 0

    # at least one chunk should be under Install or Usage
    paths = {c.heading_path for c in chunks}
    assert "Title > Install" in paths
    assert "Title > Usage" in paths


def test_windowing_overlap_is_respected():
    md = """# Title
## BigSection
""" + "word " * 35

    cfg = ChunkingConfig(max_tokens=10, overlap_tokens=2, min_tokens=3)
    chunker = HeadingAwareChunker(cfg)

    chunks = chunker.chunk(ChunkerInput(doc_id="doc2", source="file.md", text=md))
    assert len(chunks) >= 3

    # Overlap check: last 2 words of chunk0 should be first 2 words of chunk1 (approx)
    c0 = chunks[0].text.split()
    c1 = chunks[1].text.split()
    assert c0[-2:] == c1[:2]


def test_deterministic_chunk_ids():
    md = """# T
## S
""" + "alpha beta gamma delta " * 20

    cfg = ChunkingConfig(max_tokens=12, overlap_tokens=3, min_tokens=3)
    chunker = HeadingAwareChunker(cfg)

    a = chunker.chunk(ChunkerInput(doc_id="docX", source="x.md", text=md))
    b = chunker.chunk(ChunkerInput(doc_id="docX", source="x.md", text=md))

    assert [c.chunk_id for c in a] == [c.chunk_id for c in b]
    assert [c.text for c in a] == [c.text for c in b]
