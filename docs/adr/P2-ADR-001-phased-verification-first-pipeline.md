# P2-ADR-001 — Phased Pipeline with Verification-First Convergence

**Date:** 2026-09-30 | **Canonical location:** `docs/adr/`
**Re-expresses (new format):** `docs/adr/ADR-002-specification-driven-verification-first.md` (retained as historical record)

## Status

ACCEPTED

## Context

Open agent loops burn tokens and drift (EVD-001: ACI agents cost 8–13× RAG);
fixed localize→repair→validate pipelines win on cost-efficiency (EVD-002:
Agentless 32% on SWE-bench Lite at $0.70); repair converges only with external
oracles (EVD-009); test-only oracles inflate success claims (EVD-015).

## Problem

How to structure engineering work so cost stays bounded, phases cannot be
skipped, and DONE is machine-decidable without trusting agent assertions?

## Decision

Non-bypassable `DISCOVERY → SPECIFY → PLAN → IMPLEMENT → VERIFY → CONVERGED`
with `REPAIR` (oracle-fed, bounded) and `ESCALATED` (human + diagnostic diffs)
transitions; CONVERGED ⟺ all verification layers pass (verification.md).
K-bound and spec ceremony stay tunable (EXP-003/EXP-004).

## Alternatives Considered

- Pure autonomous ReAct loop — rejected: EVD-002 cost/drift evidence.
- Human-gate-every-step — rejected as default (friction RSK-07); retained as the
  escalation path, not the steady state.

## Research Evidence

EVD-002 (Agentless), EVD-001 (ACI cost), EVD-009 (oracle necessity),
EVD-015 (oracle weakness). Traceability: `research-traceability.md` rows 1–2.

## Evidence Status

PARTIALLY_SUPPORTED

## Trade-offs

Robustness and cost control vs task generality and specification friction.

## Consequences

Orchestration, contracts, and evaluation all assume phase gates; Phase 3 must
schema-tize gates and transition predicates; Phase 7 ablates C0..C4.

## Assumptions

Pipeline results transfer to polyglot repositories; ceremony is tolerable via a
micro-spec fast-path (untested).

## Open Questions

Spec-vs-no-spec ΔVSR? Optimal K and stopping rule? (GAP-004, GAP-006)

## Future Experiment

EXP-003, EXP-004.

## Phase Boundary

### Phase 2

Architectural decision: phase topology, transition names, CONVERGED predicate shape.

### Phase 3

Future contract implications: gate schemas, `VerificationResult` shape, K-bound
parameter, ESCALATE payload — to be defined, not defined here.

### Phase 4+

Future specification/implementation/verification implications: SDD artefacts per
phase, runner implementation, pre-registered ablation; no executable workflow
is created by this ADR.
