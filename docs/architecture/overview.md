# Eidos Architecture — Overview (Phase 2 Baseline)

**Status:** ARCHITECTED (conceptual baseline, not implemented, not validated)
**Date:** 2026-09-30 | **Phase:** 2 — Architecture (Phase 3+ not started)

## WHAT — What is Eidos?

Eidos is a portable **Engineering Intelligence layer** that sits between foundation
models and coding-agent harnesses. It provides repository intelligence, specification
governance, context routing, bounded subagents, verification-first execution, and
auditable progress across harnesses (Antigravity, Claude Code, Codex, OpenCode,
Cursor, Hermes).

## WHY — Problems it addresses

1. Raw-model + raw-shell harnesses waste tokens and fail on multi-file tasks (EVD-001, EVD-002).
2. Full-repo context dumps degrade retrieval (EVD-003, EVD-016).
3. Long conversational singletons contaminate context (EVD-004).
4. Unverified skill/tool supply chains are an attack surface (EVD-008).
5. Test-only oracles and leaked benchmarks inflate success claims (EVD-015).
6. Repair without external oracles does not converge (EVD-009).

## HOW — Internal decomposition

```text
                    ┌─────────────────────────┐
                    │       EIDOS CLI         │  domains.md §CLI
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      ORCHESTRATION      │  agents.md + progress.md
                    │  (pipeline state mach.) │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐       ┌────────────────┐       ┌────────────────┐
│ Context       │       │ Repository     │       │ Task / Spec    │
│ Engineering   │◄─────►│ Intelligence   │◄─────►│ Management     │
│ context.md    │ graph │ graph.md       │ refs  │ (Phase 4)      │
└───────┬───────┘       └───────┬────────┘       └───────┬────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐       ┌────────────────┐       ┌────────────────┐
│ Skills        │       │ Graph store    │       │ Contracts      │
│ skills.md     │       │ graph.md       │       │ (Phase 3)      │
└───────────────┘       └────────────────┘       └────────────────┘

        ┌──────────────────────────────────────────────┐
        │              HARNESS ADAPTERS                 │  harness.md
        └──────────────────────┬───────────────────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ Execution / Tools  │  agents.md (CodeAct)
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Verification       │  verification.md
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Evidence / Report  │  progress.md
                    └────────────────────┘

        Cross-cutting: security.md │ memory.md │ evolution.md │ invariants.md
```

Pipeline state machine (adapted from `ARCHITECTURE_PROPOSAL.md` §2, now with explicit states):

```text
DISCOVERY → SPECIFY → PLAN → IMPLEMENT → VERIFY → CONVERGE
                              │  ▲ FAIL (oracle trace)
                              │  └── REPAIR (bounded, K=TBD in Phase 3/EXP-004)
                              └── ESCALATED (human, with diffs) → DONE only on machine evidence
```

## Prior-art classification (from inspection)

| Artifact | Classification | Note |
|---|---|---|
| `docs/research/*` (12 files) | EXISTING / APPROVED research | Phase 1 + reinforcement; basis for all below |
| `docs/architecture/ARCHITECTURE_PROPOSAL.md`, `CLI_AND_REPOSITORY_SPEC.md`, `SCHEMAS_SPECIFICATION.md`, `INVARIANTS_AND_DRIFT_SPEC.md`, `DEPENDENCY_DECISION_RECORDS.md`, `RISK_REGISTER_AND_RESEARCH_GAPS.md` | PROPOSED (pre-baseline concepts) | Referenced, not duplicated; this baseline reclassifies their claims |
| `docs/adr/ADR-001..008` | APPROVED (old format) | Retained; Phase-2 ADRs in `adr/` re-express them with evidence/assumptions/experiments |
| `src/eidos/*`, `tests/*` (17 tests pass), `.eidos/*` | IMPLEMENTED-bootstrap / EXPERIMENTAL | Early code; documents existence only — NOT validated architecture (§27) |
| `CONSTITUTION.md`, `AGENTS.md`, `ARCHITECTURE.md` | APPROVED governance | Unchanged by Phase 2 |

## Reading order

principles.md → domains.md → components.md → data-model.md → graph.md →
context.md → harness.md → agents.md → skills.md → memory.md → progress.md →
verification.md → security.md → evolution.md → documentation.md → invariants.md →
adr/ → research-traceability.md → phase-2-status.md (roadmap + gates).
