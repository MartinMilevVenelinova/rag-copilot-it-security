# Roadmap — RAG Copilot (IT / Support / Security)

> Roadmap focused on deliverables and GitHub evidence (issues, PRs, demos, measurable progress).

---

## Phase 0 — Foundation & Documentation (Current)
**Goal:** define a credible enterprise project before implementation.

**Deliverables**
- README (positioning + non-goals)
- Project proposal
- MVP scope + acceptance criteria
- System principles
- Roadmap

---

## Phase 1 — Architecture & Evaluation Design
**Goal:** blueprint the system and define how quality is measured.

**Deliverables**
- `/docs/architecture.md` with component diagram and RAG flow
- Data model spec: metadata, versioning, audit events
- Evaluation plan:
  - initial QA dataset structure and quality rubric
  - baseline metrics (coverage, retrieval precision @k)
- Staleness Radar design (signals and thresholds)

**Exit criteria**
- architecture decisions justified and reviewable
- evaluation plan is repeatable and version-aware

---

## Phase 2 — MVP Build (Core RAG + Strict Mode + Answer Packs)
**Goal:** end-to-end demo: upload → ask → cited answer → strict mode → answer pack → export.

**Deliverables**
- Document ingestion + metadata + indexing
- Retrieval ranking + citation assembly
- Strict Mode thresholds and behavior
- Answer Packs (opt-in)
- Export mode (Markdown)
- Admin baseline (upload/version/analytics)
- Staleness Radar (MVP-light)

**GitHub evidence**
- Epics → issues → PRs with changelog style
- `/demo/` short video: “upload PDF → ask → cited answer → export”

**Exit criteria**
- MVP works reliably on a representative corpus
- strict mode refuses when evidence is missing

---

## Phase 3 — Hardening & Evaluation Loop
**Goal:** improve trust and reduce regressions using metrics.

**Deliverables**
- QA sets for IT / Support / Security
- Evaluation reports (versioned)
- Retrieval improvements:
  - metadata filters (domain/source/date)
  - better ranking strategies (incremental)
- Export to PDF (optional)

**Exit criteria**
- improvements are measurable
- regressions are detectable and documented

---

## Phase 4 — Governance Expansion (Enterprise-lean)
**Goal:** strengthen governance and knowledge lifecycle management.

**Deliverables**
- richer admin analytics and auditing
- improved version comparison (latest vs legacy usage)
- stronger staleness/conflict detection
- structured feedback loop for doc owners

---

## Phase 5 — Deployment & Integrations (Optional)
**Goal:** production-like deployment and optional connectors.

**Deliverables**
- reproducible deployment pipeline
- containerization and CI/CD
- connector strategy as plugins (not hard-coded)
- operational runbook for the system

---

## Planned later (Backlog)
- Coverage Map / heatmaps of topics vs evidence
- advanced hybrid search + reranking
- ticketing system integrations (draft creation workflows)
- incident-response mode templates by severity
