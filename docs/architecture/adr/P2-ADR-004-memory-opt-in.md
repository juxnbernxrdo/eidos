# P2-ADR-004 — Tripartite Memory as Opt-In Experimental

**Status:** EXPERIMENTAL (utility) + ACCEPTED (isolation rules)
**Date:** 2026-09-30 | **Supersedes-format-of:** `docs/adr/ADR-005-*` (retained)

## Context
Dialogue memory helps chat (A-MEM +35%, Mem0 +26%/−91% p95) but never ablated on
SWE tasks; contamination cascades formalized (ρ-metric, MemoryGraft, MINJA);
project-scoped memory has product precedent with known confusion failure modes.

## Problem
Can persistent memory help engineering agents without fossilizing hallucinations
or leaking across projects?

## Decision
Three tiers (working/project/institutional, memory.md) with write-time admission
gates, ρ tracking, and human-gated institutional writes. Ships OPT-IN only:
project tier available, institutional default-off (ARR-01). No global memory.

## Alternatives
Full persistent memory by default (rejected: contamination + INV-002 risk);
stateless-only (rejected: discards project conventions; kept as control arm).

## Research Evidence
EVD-017 — traceability row 7.

## Trade-offs
Recall/convention reuse vs contamination, storage, and approval burden.

## Consequences
Memory writes are validated experiments (EXP-005); ρ is an invariant signal;
sanitization-utility trade-off measured before any default-on proposal.

## Assumptions
Dialogue gains partially transfer; gates affordable; sanitization preserves utility.

## Open Questions
Memory on/off ΔVSR multi-session? τ calibration? (GAP-007)

## Future Experiment
EXP-005 (arm M).
