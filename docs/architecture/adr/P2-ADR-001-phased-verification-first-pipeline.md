# P2-ADR-001 — Phased Pipeline with Verification-First Convergence

**Status:** ACCEPTED (structure) + EXPERIMENTAL (spec-efficacy, K-bound)
**Date:** 2026-09-30 | **Supersedes-format-of:** `docs/adr/ADR-002-*` (retained)

## Context
Open agent loops burn tokens and drift (EVD-001 cost 8–13×); fixed localize→repair→
validate pipelines win on cost-efficiency (EVD-002); repair converges only with
external oracles (EVD-009); test-only oracles inflate claims (EVD-015).

## Problem
How to structure engineering work so cost stays bounded, phases can't be skipped,
and DONE is machine-decidable without trusting agent assertions?

## Decision
Non-bypassable `DISCOVERY → SPECIFY → PLAN → IMPLEMENT → VERIFY → CONVERGED`
with `REPAIR` (oracle-fed, bounded) and `ESCALATED` (human + diffs) transitions;
CONVERGED ⟺ all verification layers pass (verification.md). K-bound and spec
ceremony stay tunable (EXP-003/004).

## Alternatives
Pure autonomous ReAct loop (rejected: EVD-002 cost/drift); human-gate-every-step
(rejected: friction RSK-07; kept as escalation path, not default).

## Research Evidence
EVD-002 (Agentless), EVD-001 (ACI cost), EVD-009 (oracle necessity), EVD-015
(oracle weakness) — see research-traceability.md row 1–2.

## Trade-offs
Robustness/cost vs generality and spec friction.

## Consequences
Orchestration, contracts, and evaluation all assume phase gates; Phase 3 must
schema-tize gates; Phase 7 ablates C0..C4.

## Assumptions
Transfer to polyglot repos; ceremony tolerable via micro-spec fast-path.

## Open Questions
Spec-vs-no-spec ΔVSR? Optimal K + stopping rule? (GAP-004/006)

## Future Experiment
EXP-003, EXP-004.
