# Architecture — RAG Copilot for IT Security (Local-First)

## 1. Purpose & Scope

`rag-copilot-it-security` is an evidence-first Retrieval-Augmented Generation (RAG) assistant designed for IT Security and IT operations work. It runs **local-first** (offline capable), avoids paid LLM APIs by default, and prioritizes **traceable answers** through:

- **Mandatory citations** with ranked sources for every claim.
- **Strict Mode**: when evidence is insufficient, the system returns **“Not found”** rather than guessing.
- **Answer Packs (opt-in)**: exportable, reproducible bundles of answers + supporting evidence + audit metadata.
- **Audit/Export**: tamper-resistant logs and structured exports for compliance and internal review.
- **Staleness Radar (MVP-light)**: warns when retrieved evidence may be outdated or superseded.

This document describes components, data flow, modes, security considerations, and deployment options.

---

## 2. Key Principles

### 2.1 Evidence-First Output Contract
1. Every non-trivial answer must cite **at least one** source chunk.
2. Citations are **ranked** and explain why they were selected.
3. If evidence does not support the claim → **Strict Mode** returns “Not found”.

### 2.2 Local-First by Design
- Default LLM runtime: **Ollama** with open models.
- Local embeddings model.
- Local vector store + local metadata DB.
- No external calls required for core functionality.

### 2.3 Reproducibility
- Each answer is traceable to: dataset version, index version, model versions, retrieval parameters, and chunk IDs.
- Answer Packs capture a complete snapshot to reproduce the output.

---

## 3. System Overview (High-Level)

### 3.1 Primary Runtime Components
- **UI Layer**
  - CLI (primary) and optional Web UI (later)
- **API / Orchestrator**
  - Coordinates retrieval, ranking, generation, strict mode decisions, citations, and exports
- **Knowledge Layer**
  - Ingestion pipeline
  - Chunking + normalization
  - Embedding + indexing
  - Metadata store + vector store
- **Reasoning Layer**
  - Local LLM (Ollama)
  - Optional local reranker (cross-encoder)
- **Governance Layer**
  - Audit logger
  - Export/Answer Pack builder
  - Staleness Radar

### 3.2 Data Stores
- **Vector Store** (embeddings + references to chunk IDs)
- **Document/Chunk Store** (raw docs + normalized text + chunk payloads)
- **Metadata DB** (SQLite/DuckDB) for:
  - document manifests, ingest provenance, chunk map, timestamps, hash digests
  - retrieval traces, answer traces, export records
- **Audit Log** (append-only):
  - JSONL events + optional hash chain for integrity

---

## 4. Data Model (Conceptual)

### 4.1 Document Manifest
A document is represented by a manifest record:
- `doc_id` (stable ID)
- `source_uri` (path / URL / repository ref)
- `ingested_at`
- `content_hash` (SHA-256)
- `title`, `doc_type`, `language`
- `published_at` (if available), `last_modified_at` (if available)
- `license`, `classification` (optional)
- `tags` (e.g., “NIST”, “ISO27001”, “Vendor-X”)

### 4.2 Chunk Record
Each chunk:
- `chunk_id` (stable)
- `doc_id`
- `chunk_text`
- `chunk_hash`
- `offsets` (start/end in normalized text)
- `semantic_section` (heading path)
- `created_at`

### 4.3 Retrieval Trace
A query produces a trace:
- query text + normalized query
- retrieval params (k, filters, hybrid weights)
- candidate list with scores
- reranking scores (if enabled)
- selected citations list

### 4.4 Answer Trace
- strict mode decision
- generated answer
- citations used
- model info (LLM, embedding model versions)
- export / answer pack references

---

## 5. Ingestion & Indexing Pipeline

### 5.1 Supported Inputs (MVP)
- Markdown, TXT, PDF (text extraction), HTML
- Folder ingestion (docs/ directory, security policies, runbooks)
- Optional: Git repo ingestion (readme/docs and selected paths)

### 5.2 Pipeline Stages
1. **Acquire**
   - Collect files, capture file metadata, compute content hash
2. **Normalize**
   - Convert to clean text, normalize whitespace, preserve headings/sections
3. **Chunk**
   - Split by semantic boundaries (headings) + token/window constraints
   - Maintain stable `chunk_id` mapping
4. **Embed**
   - Generate embeddings locally
5. **Index**
   - Write embeddings to vector store
   - Write chunk payloads + manifest to metadata DB
6. **Validate**
   - Ensure chunk coverage, detect duplicates by hash, verify index integrity

---

## 6. Query & RAG Answer Flow

### 6.1 Default RAG Flow
1. **Input**
   - User question + optional constraints (time window, sources, tags)
2. **Query Normalization**
   - detect intent, extract key entities, apply policy filters
3. **Retrieve**
   - vector similarity search
   - optional lexical/hybrid retrieval
4. **Rerank (optional)**
   - local cross-encoder reranker for precision
5. **Select Evidence**
   - choose top N chunks with diversity constraints (avoid same doc only)
6. **Citations Preparation**
   - build citation objects: doc title, section, snippet, chunk_id, rank reasons
7. **Strict Mode Gate**
   - evidence checks; may return “Not found”
8. **Generate**
   - local LLM produces answer constrained to evidence
9. **Post-Process**
   - enforce “claim → citation” rules
10. **Audit**
   - record retrieval + answer trace events
11. **Return**
   - answer + ranked citations + notes (staleness warnings, limitations)

---

## 7. Strict Mode (Not found)

Strict Mode prevents hallucination. It triggers “Not found” when:
- retrieved evidence score is below threshold,
- evidence conflicts or is too ambiguous,
- query requires data not present in the corpus,
- citations cannot be attached to key claims.

Outputs:
- `Not found` as the primary answer
- optional: transparency about what sources were searched
- suggestion on how to add missing evidence (optional)

---

## 8. Answer Packs (Opt-In)

Answer Packs are reproducible bundles for sharing and audits.

They contain:
- question + normalized query
- final answer
- ranked citations + snippets
- retrieval trace (scores, filters, index version)
- model versions (LLM + embeddings)
- timestamps + environment metadata

---

## 9. Audit & Export

Audit captures:
- ingestion events (doc added/updated/removed)
- query events (retrieval trace)
- answer events (strict decision, citations used)
- export events (Answer Pack creation)

Optional integrity:
- hash chaining per event
- signed checkpoints (future)

---

## 10. Staleness Radar (MVP-light)

Staleness Radar warns when evidence might be outdated.

Signals (MVP):
- document age from `published_at` / `last_modified_at`
- “deprecated/superseded” markers in docs
- multiple versions of the same policy in corpus

Output:
- non-blocking warning
- citations that triggered the warning
- suggestion to add newer sources

---

## 11. Security & Privacy (Local-First)

Key risks:
- sensitive data in docs
- prompt injection from retrieved text
- index poisoning

Mitigations:
- secrets scanning (basic)
- source allowlist/denylist
- strict mode + citation coverage
- optional audit integrity (hash chain)

---

## 12. Deployment Profiles

- Local developer mode: Ollama + local stores + CLI
- Team workstation mode: shared read-only corpus, controlled index rebuilds
- Air-gapped mode: preloaded models and index snapshots

---

## 13. MVP Roadmap Alignment

MVP (Milestone M1):
- ingestion + indexing
- retrieval + mandatory ranked citations
- strict mode (“Not found”)

Next:
- audit/export
- answer packs
- staleness radar enhancements
