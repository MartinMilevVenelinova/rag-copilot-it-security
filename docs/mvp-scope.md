# MVP Scope — RAG Copilot (IT / Support / Security)

## 1) MVP Objective
Deliver a working internal copilot that:
- ingests a bounded set of documents,
- answers questions with **mandatory citations** and source ranking,
- supports **Strict Mode** (“not found” if insufficient evidence),
- provides **opt-in Answer Packs** for operational workflows,
- supports an admin panel for ingestion and basic governance,
- enables **Audit / Export mode** for traceable outputs.

---

## 2) In Scope (MVP)
### Knowledge ingestion
- Upload: PDFs + plain text/Markdown
- Text extraction and normalization
- Minimal metadata:
  - source name, domain (IT/Support/Security), version/date (if available), owner tag (optional)
- Index creation for retrieval

### Retrieval + RAG answering
- Top-k retrieval with ranking
- Answer format includes:
  - citations at statement/section level
  - ranked list of sources used
- **Strict Mode**:
  - if evidence is below threshold → “Not found in knowledge base” (no guessing)

### Answer Packs (opt-in)
When explicitly requested, generate:
- executive summary (brief)
- step-by-step runbook
- checklist
- ticket response template
- optional: risks/impact/rollback notes when relevant

### Audit / Export mode (MVP)
- Export the answer + citations + sources as:
  - Markdown (minimum)
  - (optional later) PDF rendering

### Admin (minimum viable)
- Upload and disable documents (soft delete)
- Basic version handling (upload new version + mark latest)
- Basic analytics:
  - top queries
  - top sources
  - “not found” queries

### Staleness Radar (MVP-light)
Admin-facing flags based on simple signals:
- “mentions EOL/outdated version keywords”
- “older version is used more than latest”
- “conflict suspicion” (same topic tags with contradictory key terms)

> This is intentionally lightweight for MVP.

---

## 3) Suggested filter approach (MVP-friendly)
Filters can be implemented without complexity by relying on metadata:
- Domain: IT / Support / Security
- Source type: runbook / KB / ticket-export / policy
- Date/version: prefer latest by default
- Confidence threshold: strict vs normal

The MVP goal is not advanced policy enforcement, but **user-controllable retrieval scope**.

---

## 4) Out of Scope (MVP)
- Production-grade connectors (ServiceNow/Jira/Confluence/SharePoint)
- SSO/SAML and enterprise IAM
- Multi-tenant architecture
- Auto-editing docs and publishing changes
- Direct ticket creation in external systems
- Coverage heatmaps / topic maps (planned later)

---

## 5) MVP Acceptance Criteria
- Every normal answer includes:
  - at least N citations (configurable)
  - ranked sources
- Strict mode:
  - missing evidence → “Not found” with zero invented content
- Answer Packs:
  - only generated when requested
  - built strictly from retrieved evidence
- Export:
  - answer + citations + sources exported in a reproducible format
- Admin:
  - upload + version + analytics baseline works
- Staleness Radar:
  - produces actionable flags on a sample corpus

---

## 6) Definition of Done (MVP)
A reviewer can:
1) upload a document,  
2) ask a question,  
3) receive an answer with citations,  
4) enable Strict Mode and see “not found” when appropriate,  
5) request an Answer Pack and get operational outputs,  
6) export the answer for ticket/audit use,  
7) view basic admin analytics and staleness flags.
