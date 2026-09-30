# P2-ADR-005 — Harness Adapter Abstraction

**Status:** ACCEPTED (abstraction) + PROPOSED (per-harness specifics)
**Date:** 2026-09-30 | **Supersedes-format-of:** `docs/adr/ADR-006-*` (retained)

## Context
Harness changes move outcomes at fixed model (EVD-001/002); MCP is the neutral
standard (SRC-105); host APIs drift (RSK-04); OSS harnesses verified at snapshot
level (SRC-200..203).

## Problem
How to stay portable across Antigravity/Claude Code/OpenCode/Codex/Cursor/Hermes
without leaking host specifics into Core?

## Decision
`HarnessAdapter` with REQUIRED (`detect/capabilities/configure/invoke/
collect_output/collect_trace`), OPTIONAL (`install` thin bridges), DROPPED
(`verify` — belongs to Verification). Host specifics isolated per adapter;
Core/MCP-CLI boundary kept stable; headless reference harness for fair eval.

## Alternatives
Monolithic per-harness forks (rejected: INV-001, maintenance); direct host-API
coupling in Core (rejected: P1/P2, RSK-04).

## Research Evidence
EVD-001/002, SRC-105 — traceability row 12.

## Trade-offs
Portability vs breakage-maintenance burden and trace-completeness variance.

## Consequences
Adapter conformance suite; longitudinal breakage log (EXP-007); unobservable host
internals stay UNKNOWN (no inference fabrication).

## Assumptions
MCP/CLI stability sufficient; adapters stay thin.

## Open Questions
Breakage rate? MCP-vs-CLI overhead? Headless fairness? (GAP-008)

## Future Experiment
EXP-007.
