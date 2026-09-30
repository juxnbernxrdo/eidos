# P2-ADR-004 — Tripartite Memory as Opt-In Experimental

**Date:** 2026-09-30 | **Canonical location:** `docs/adr/`
**Re-expresses (new format):** `docs/adr/ADR-005-tripartite-memory-isolation.md` (retained as historical record)

## Status

EXPERIMENTAL

## Context

Dialogue memory improves conversational benchmarks (A-MEM +35%, Mem0 +26% with
−91% p95 latency) but has never been ablated on software-engineering tasks;
contamination cascades are formalized (ρ-metric, MemoryGraft, MINJA lineage);
project-scoped product memory exists with known confusion failure modes
(SRC-107, issue #23341 lineage).

## Problem

Can persistent memory help engineering agents without fossilizing hallucinations
or leaking data across projects?

## Decision

Three tiers — working (ephemeral), project (repo-tracked), institutional
(human-approved) — with write-time admission gates, cascade-rate (ρ) tracking,
and human-gated institutional writes (memory.md). Ships OPT-IN only:
project tier available, institutional default-off (ARR-01). No global memory.

## Alternatives Considered

- Full persistent memory by default — rejected: contamination plus INV-002 risk.
- Stateless-only — rejected as sole mode (discards project conventions); retained
  as the control arm for experiments.

## Research Evidence

EVD-017. Traceability: `research-traceability.md` row 7.

## Evidence Status

RESEARCH_HYPOTHESIS

## Trade-offs

Convention recall and reuse vs contamination risk, storage, and human approval
burden.

## Consequences

Memory writes are treated as validated experiments (EXP-005); ρ becomes an
invariant signal; sanitization-utility trade-off is measured before any
default-on proposal.

## Assumptions

Dialogue gains partially transfer to code tasks; admission gates are affordable;
sanitization preserves utility.

## Open Questions

Memory on/off ΔVSR on multi-session SWE tasks? Admission-threshold (τ)
calibration? (GAP-007)

## Future Experiment

EXP-005 (arm M).

## Phase Boundary

### Phase 2

Architectural decision: tier taxonomy, gating rules, default-off posture.

### Phase 3

Future contract implications: `memory_write` schema, admission-gate interface,
ρ-report shape — to be defined, not defined here.

### Phase 4+

Future specification/implementation/verification implications: store specs,
gate implementation, multi-session ablation; no memory store is specified by
this ADR.
