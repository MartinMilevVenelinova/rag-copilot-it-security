# System Principles — RAG Copilot (Enterprise-grade)

## 1) Evidence First
- No answer is treated as authoritative unless supported by retrieved evidence.
- Citations are mandatory, not optional.
- Fluent text is not a success metric; traceability is.

## 2) Strict Mode as a Safety Rail
- Strict Mode is designed to prevent high-confidence wrong answers.
- If evidence is insufficient, return a clear refusal:
  - “Not found in knowledge base.”
- Strict Mode should be predictable and auditable.

## 3) Local-first, Vendor-Optional
- Default runtime avoids paid external LLM APIs.
- Keep components replaceable:
  - model runtime, embeddings, vector storage, and UI should be swappable.
- Avoid lock-in and keep interfaces clean.

## 4) Security by Design
- Least privilege access model (admin vs user)
- Audit logs for sensitive actions (ingestion, version changes, exports)
- Defensive defaults (no broad data exposure)

## 5) Privacy & Data Governance
- Tickets and operational docs may contain sensitive data.
- Prefer sanitization and explicit ingestion policies.
- Ensure traceable handling of document versions and retention.

## 6) Reproducibility & Versioning
- Every answer should be traceable to:
  - document versions and index version
  - retrieval configuration and mode
- Support regression detection via evaluation and version comparisons.

## 7) Observability & Accountability
- Track:
  - query volume and trends
  - “not found” rate
  - source usage distribution
  - latency (later)
- Observability exists to drive improvements and reduce risk.

## 8) Operational Usefulness
- Optimize for support/security workflows:
  - runbooks, checklists, ticket templates, audit exports.
- The system should reduce ambiguity and improve consistency.

## 9) Human-in-the-loop Knowledge Improvement
- The system should highlight:
  - stale documents
  - conflicting guidance
  - missing coverage (gaps)
- It should support improvement cycles rather than pretending to be complete.

## 10) Continuous Evaluation
- Quality must be measurable.
- Changes to chunking/ranking/prompts require evaluation runs.
- Prefer fewer answers over incorrect answers in critical contexts.
