# Documentation Architecture (Phase 2)

**Status:** ARCHITECTED | Progressive disclosure retained (Constitution Art. VII).

## AGENTS.md — entry point / navigation / rules router (NOT a monolith)

Routes to: `CONSTITUTION.md`, `docs/architecture/overview.md`, specs, contracts
(Phase 3), rules, skills, security (`security.md`), testing (`verification.md`),
research (`docs/research/`). Keeps zero bloated inline content; violations of
brevity are DOC-DRIFT against this file's own contract (Phase 3).

## CONSTITUTION.md — stable principles (amendable only by explicit human ratification)

Retains Articles 0–IX (self-reference, layering, policy-as-physics, zero-unaudited
skills, verification-first, K-bound, dependency policy, typing, docs sync,
event sourcing, contract-bounded subagents, honesty axiom). Phase 2 adds NO new
article; ARR-01..05 are recorded in `research/architecture-traceability.md` and
`phase-2-status.md` as review items, not constitutional changes.

## This baseline's place

```text
AGENTS.md → CONSTITUTION.md → docs/architecture/overview.md → (this layer) →
docs/adr/ (ADR-001..008 + P2-ADR-001..008, single canonical location) →
Phase 3 contracts → Phase 4 specs
```

Living-documentation rule (Art. VII): any Phase-3 contract change must update the
corresponding architecture page or fail drift. Enforcement mechanism is Phase 6 work.
