# Definition of Done (DoD) & Review Policy

## Purpose
This document defines when work is considered **Done** in this repository and how changes are reviewed. The goals are:
- consistent quality and traceability
- reproducible outcomes (especially for evidence-first RAG)
- clear expectations for contributors and reviewers

---

## Definition of Done (applies to Issues, PRs, and Milestones)

A task is **Done** when all applicable criteria below are satisfied.

### 1) Scope & Requirements
- [ ] The change matches the issue scope (no hidden scope creep).
- [ ] Acceptance Criteria are met (from the issue template or PR description).
- [ ] Out-of-scope items are not included (or are moved into a separate issue).

### 2) Quality & Consistency
- [ ] Code/doc style is consistent with the repository conventions.
- [ ] Naming and structure follow existing patterns.
- [ ] No unfinished work is left without tracking (TODOs must link to an issue).

### 3) Verification / Testing
**At least one** verification method must exist when applicable:
- [ ] Unit tests added/updated, **or**
- [ ] Integration tests added/updated, **or**
- [ ] Manual verification steps documented (with expected output)

If tests are not applicable:
- [ ] The PR explains why tests are not applicable.

### 4) Documentation
- [ ] Documentation is updated if behavior/UX/output formats changed.
- [ ] If architecture/flows are affected, `docs/architecture.md` is updated.
- [ ] New CLI commands/config options are documented (when the MVP exists).

### 5) Evidence-First Contract (RAG-specific)
If the change touches retrieval, citations, strict mode, prompts, or output formatting:
- [ ] Mandatory citations for non-trivial answers are preserved.
- [ ] Citations are ranked and reference stable chunk/doc identifiers.
- [ ] Strict Mode behavior is preserved: returns **Not found** when evidence is insufficient.
- [ ] Thresholds/parameters are documented (defaults + rationale).

### 6) Security & Privacy
- [ ] No secrets or sensitive data are committed.
- [ ] Input/output handling is considered (prompt injection, unsafe content, data leakage).
- [ ] Security-sensitive changes are labeled `risk:security` and receive extra review.

### 7) Performance (when applicable)
- [ ] No obvious performance regressions (index build, retrieval latency, memory).
- [ ] Perf-sensitive changes are labeled `risk:perf` and include measurements when possible.

### 8) Project Hygiene
- [ ] PR links to the issue(s) it addresses (e.g., `Closes #123`).
- [ ] Milestone/labels/status are correct.
- [ ] The change is small and focused (or clearly split into multiple PRs).

---

## Review Policy

### PR Requirement
- Prefer PRs for changes (even for docs) to keep a clear history.
- Each PR should address **one logical change**.

### Approvals
- **Normal changes:** at least **1 approval** (self-review is fine for a solo repo; still follow the checklist).
- **Security-sensitive (`risk:security`) or breaking changes:** require **2 approvals** (or an explicit review note documenting the security reasoning).

### Reviewer Checklist
Reviewers should confirm:
- scope matches the issue
- acceptance criteria met
- docs/tests updated when applicable
- evidence-first contract not violated

---

## Milestone Completion Rule
A milestone can be marked **Done** when:
- all P0/P1 issues are closed, and
- remaining items are either completed or explicitly moved to the next milestone with rationale.

---

## Notes (Phase 0)
This repository is currently in **Phase 0 (docs-only)**. Some DoD items (tests, CLI docs, performance checks) will become mandatory once the MVP is runnable. Until then, focus on:
- clarity
- traceability
- professional repo hygiene
