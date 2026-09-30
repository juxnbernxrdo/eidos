# P2-ADR-006 — Skill Gateway and OS-Level Sandboxing

**Status:** ACCEPTED (architecture) + EXPERIMENTAL (thresholds, guarantees)
**Date:** 2026-09-30 | **Supersedes-format-of:** `docs/adr/ADR-007-*` (retained)

## Context
Prompt bans are bypassable (EVD-007); wild skills carry real risk (31k-scan
MedusaLocker case; repo-aware rates up to 46.8% flagged, 0.52% persistent);
NVIDIA T1–T3 gives the evaluation template; OpenShell (alpha) gives the
kernel-mechanism lineage.

## Problem
How to consume third-party skills/tools without supply-chain compromise or
destructive execution, without over-blocking legitimate skills?

## Decision
Two-phase gateway (static AST+YARA → provenance → semantic audit; repo-aware,
hash-pinned) + kernel sandbox lineage (Landlock/seccomp/userns/netns + OPA +
policy proxy) + least-privilege contract scopes. Thresholds (risk<25-style)
are DESIGN_CHOICE pending ROC calibration (ARR-03).

## Alternatives
Prompt-only restrictions (rejected: EVD-007); naive filename-only scanning
(rejected: 99.5% flags vanish with context — over-blocks); no sandbox
(rejected: RSK-05 destructive risk).

## Research Evidence
EVD-007/008, SRC-027/028/108 — traceability row 6.

## Trade-offs
Safety vs install latency, false blocks, Linux-first portability limits.

## Consequences
Gate precision/recall + pen-test + overhead measured (EXP-005) before any
production claim; sandbox protects only in-sandbox runs.

## Assumptions
Linux-first acceptable; pinning scales; semantic pass affordable.

## Open Questions
Calibrated threshold? Escape rate? Over-head budget? (GAP-005)

## Future Experiment
EXP-005.
