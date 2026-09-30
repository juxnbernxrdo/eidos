# P2-ADR-007 — Event-Sourced Progress, Passports, and Gated Evolution

**Status:** ACCEPTED (governance model) + CONCEPTUAL (passport system, evolution)
**Date:** 2026-09-30 | **Supersedes-format-of:** `docs/adr/ADR-008-*` (retained)

## Context
Reproducibility demands exact traces (EVD-015); EventStream precedent exists
(SRC-005); GEPA-style metric-driven optimization works while open-ended evolution
needs oversight (EVD-018); silent self-modification is the top trust risk (INV-004).

## Problem
How to make progress replayable and improvements possible without ever
self-modifying silently?

## Decision
Append-only hash-chained event log as truth, state as projection (progress.md);
Feature Passport as convergence projection (data-model.md §4, CONCEPTUAL);
evolution strictly via Observation→Proposal→Experiment→Approval→Versioned-Change
with Reflection/Repair allowed, GEPA-Improvement EXPERIMENTAL, Evolution
FORBIDDEN-by-default (ARR-04). Self-reference (Axiom 0) is direction, not capability.

## Alternatives
Mutable state + git-only history (rejected: loses action-level causality needed
for ablations); autonomous self-evolution (rejected: EVD-018 oversight requirement).

## Research Evidence
EVD-015, SRC-005, EVD-018 — traceability rows 8, 11.

## Trade-offs
Auditability vs storage/verbosity; learning vs oversight cost and divergence risk.

## Consequences
`evaluation_run.json` template becomes the benchmark projection; `.eidos/evolution/`
quarantine enforced; full self-reference cycle validation deferred to Phases 6–8.

## Assumptions
Log volume manageable; human approval bandwidth exists; metric + val-set available.

## Open Questions
Passport minimal fields? GEPA-on-Eidos ΔVSR? (GAP-009/010)

## Future Experiment
EXP-001 (as instrument), EXP-006.
