# P2-ADR-006 — Skill Gateway and OS-Level Sandboxing

**Date:** 2026-09-30 | **Canonical location:** `docs/adr/`
**Re-expresses (new format):** `docs/adr/ADR-007-security-sandbox-openshell-skillspector.md` (retained as historical record)

## Status

ACCEPTED

## Context

Prompt-only prohibitions are bypassable (EVD-007); wild skill packages carry
measured supply-chain risk (31k-skill scan with MedusaLocker case; repo-aware
rates up to 46.8% flagged, 0.52% persistent with context); NVIDIA T1–T3 gives
the evaluation template (SRC-108); OpenShell (alpha) gives the kernel-mechanism
lineage.

## Problem

How to consume third-party skills and tools without supply-chain compromise or
destructive execution — and without over-blocking legitimate skills?

## Decision

Two-phase gateway (static AST+YARA → provenance check → semantic audit;
repo-aware, hash-pinned) plus kernel-sandbox lineage (Landlock/seccomp/userns/
netns, OPA, policy proxy) plus least-privilege contract scopes (security.md,
skills.md). Numeric thresholds (risk<25-style) are DESIGN_CHOICE pending ROC
calibration (ARR-03).

## Alternatives Considered

- Prompt-only restrictions — rejected: EVD-007 bypassability.
- Filename-only naive scanning — rejected: 99.5% of flags vanish with repo
  context (over-blocks legitimate skills).
- No sandbox — rejected: RSK-05 destructive-filesystem risk.

## Research Evidence

EVD-007, EVD-008, SRC-027, SRC-028, SRC-108.
Traceability: `research-traceability.md` row 6.

## Evidence Status

PARTIALLY_SUPPORTED

## Trade-offs

Safety vs install latency, false-block rate, and Linux-first portability limits.

## Consequences

Gate precision/recall, penetration resistance, and overhead must be measured
(EXP-005) before any production-grade claim; the sandbox protects only
in-sandbox runs.

## Assumptions

Linux-first acceptable; hash/owner pinning scales; semantic pass affordable.

## Open Questions

Calibrated risk threshold? Escape rate? Overhead budget? (GAP-005)

## Future Experiment

EXP-005.

## Phase Boundary

### Phase 2

Architectural decision: gateway stages, sandbox mechanism lineage, boundary
stack, least-privilege posture.

### Phase 3

Future contract implications: `skill_manifest` schema, `sandbox_policy` schema,
gateway verdict shape — to be defined, not defined here.

### Phase 4+

Future specification/implementation/verification implications: gateway and
supervisor specs, scanner/pen-test implementation, gate calibration; no scanner
or sandbox is implemented by this ADR.
