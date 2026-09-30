# P2-ADR-007 — Event-Sourced Progress, Passports, and Gated Evolution

**Date:** 2026-09-30 | **Canonical location:** `docs/adr/`
**Re-expresses (new format):** `docs/adr/ADR-008-event-sourcing-progress-evidence.md` (retained as historical record)

## Status

ACCEPTED

## Context

Reproducibility demands exact execution traces (EVD-015); EventStream precedent
exists (SRC-005: OpenHands); metric-driven pipeline optimization works while
open-ended evolution requires oversight (EVD-018: GEPA +6pp at 35× fewer
rollouts; DGM sandboxed-only); silent self-modification is the top trust risk
(INV-004).

## Problem

How to make progress replayable and improvement possible without ever
self-modifying silently?

## Decision

Append-only hash-chained event log as truth with state as projection
(progress.md); Feature Passport as the convergence projection (data-model.md §4,
CONCEPTUAL); improvement strictly via
Observation→Proposal→Experiment→Approval→Versioned-Change with Reflection and
bounded Repair allowed, GEPA-style Improvement EXPERIMENTAL, and Evolution
FORBIDDEN-by-default (ARR-04). Self-reference (Axiom 0) is architectural
direction, not a validated capability.

## Alternatives Considered

- Mutable state with git-only history — rejected: loses the action-level
  causality that ablations require.
- Autonomous self-evolution — rejected: EVD-018 oversight requirement and
  Microsoft diminishing-returns warning.

## Research Evidence

EVD-015, SRC-005, EVD-018. Traceability: `research-traceability.md` rows 8, 11.

## Evidence Status

DESIGN_CHOICE

## Trade-offs

Auditability vs log storage and verbosity; learning potential vs oversight cost
and divergence risk.

## Consequences

`evaluation_run.json` becomes the benchmark-grade projection of the log;
`.eidos/evolution/` quarantine is enforced; full self-reference-cycle validation
is deferred to Phases 6–8.

## Assumptions

Log volume is manageable; human approval bandwidth exists; a metric plus
validation set is available for any Improvement work.

## Open Questions

Minimal viable passport fields? GEPA-on-Eidos ΔVSR? (GAP-009, GAP-010)

## Future Experiment

EXP-001 (log as instrument), EXP-006.

## Phase Boundary

### Phase 2

Architectural decision: event hierarchy, fold semantics, passport model,
gated-evolution pipeline, forbidden-by-default posture.

### Phase 3

Future contract implications: `event`, `feature_passport`, `evolution_proposal`,
`evaluation_run` schemas — to be defined, not defined here.

### Phase 4+

Future specification/implementation/verification implications: logger/projector
specs, passport tooling, sandboxed improvement trials; no log store or
evolution runner is implemented by this ADR.
