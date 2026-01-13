# Project Proposal — RAG Copilot for IT & Security Knowledge

## 1) Executive Summary
RAG Copilot is an internal assistant for IT/Support/Cybersecurity teams that transforms scattered operational documentation into an auditable, searchable system. Its key differentiator is an **evidence-first** approach: every answer includes **mandatory citations**, ranked sources, and an optional **Strict Mode** that refuses to guess when evidence is insufficient.

Beyond Q&A, RAG Copilot supports **Answer Packs** (opt-in) that produce operational outputs such as step-by-step runbooks, checklists, and ticket response templates—turning knowledge into action.

---

## 2) Problem Statement
Operational knowledge tends to be:
- fragmented across PDFs, wikis, drives, and ticket exports
- inconsistent and frequently outdated
- difficult to audit (“who said this?” “based on what?”)
- locked in tribal knowledge and senior staff

This increases MTTR, reduces consistency in support responses, and creates compliance risk for security operations.

---

## 3) Goals
### Product goals
- Centralize and operationalize internal documentation through evidence-backed retrieval.
- Provide trustworthy answers with citations and explicit uncertainty handling.
- Generate actionable outputs for support and security workflows (Answer Packs).
- Improve knowledge governance with versioning and usage visibility.

### Non-functional goals
- Security-by-design (access control, auditability)
- Observability (metrics for usage and quality)
- Reproducibility (versioned knowledge base and evaluation)

---

## 4) Target Users & Primary Use Cases
- **Helpdesk / Support (L1/L2):** ticket-ready guidance with standard templates and cited procedures
- **SecOps / IR:** playbooks and guidance with traceable evidence
- **IT Ops:** troubleshooting using internal runbooks and approved docs
- **Knowledge owners:** identify stale docs, gaps, and high-impact knowledge areas

---

## 5) Differentiators (why it’s credible and “enterprise-grade”)
1. **Mandatory citations + ranked sources**  
   Answers must be traceable to ingested internal documents.
2. **Strict Mode (fail-safe)**  
   If evidence is weak or missing, the system returns “Not found.”
3. **Answer Packs (opt-in operational outputs)**  
   Converts knowledge into runbooks, checklists, and ticket templates.
4. **Staleness Radar (MVP-light)**  
   Flags likely outdated/conflicting/high-risk documentation.
5. **Continuous evaluation**  
   A repeatable evaluation set measures retrieval quality and regression.

---

## 6) Deployment & Cost Assumption
The project is designed to operate **without paid LLM APIs**, using local inference (e.g., Ollama + open models). The system remains vendor-optional by design, but the default deployment path prioritizes:
- predictable cost
- data control
- internal-only usage

---

## 7) Risks and Mitigations
- **Sensitive data in tickets/docs**  
  Mitigate via ingestion policy, sanitization, and access control.
- **Low-quality documentation leads to poor answers**  
  Mitigate via analytics, “not found” clarity, and update suggestions.
- **Overtrust in generated text**  
  Mitigate via strict mode, citations, and export/audit trace.

---

## 8) Success Metrics (proposal)
- Reduced time-to-resolution on representative scenarios
- Coverage rate (% of queries answered with sufficient evidence)
- Retrieval precision (top-k relevance) on evaluation set
- “Not found” rate within expected bounds (signals gaps)
- Adoption of Answer Packs and template exports
- Number of stale-document flags resolved over time

---

## 9) Deliverables (this phase)
- README (positioning + non-goals)
- MVP scope
- System principles
- Roadmap
