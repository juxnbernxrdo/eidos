# P2-ADR-005 — Harness Adapter Abstraction

**Date:** 2026-09-30 | **Canonical location:** `docs/adr/`
**Re-expresses (new format):** `docs/adr/ADR-006-harness-adapter-abstraction.md` (retained as historical record)

## Status

ACCEPTED

## Context

Harness changes move outcomes at fixed model (EVD-001, EVD-002); MCP is the
neutral tool standard (SRC-105); host APIs drift over time (RSK-04); OSS harness
snapshots verified (SRC-200–SRC-203).

## Problem

How to stay portable across Antigravity, Claude Code, OpenCode, Codex, Cursor,
and Hermes without leaking host specifics into Core?

## Decision

`HarnessAdapter` with REQUIRED methods (`detect`, `capabilities`, `configure`,
`invoke`, `collect_output`, `collect_trace`), OPTIONAL (`install`, thin bridges
only), and DROPPED (`verify` — verification belongs to the Verification domain
per P5; adapters must not self-certify). Host specifics isolated per adapter;
Core and the MCP/CLI boundary stay stable; a headless reference harness serves
fair-model evaluation.

## Alternatives Considered

- Monolithic per-harness forks — rejected: INV-001 and maintenance burden.
- Direct host-API coupling inside Core — rejected: P1/P2 and RSK-04 drift risk.

## Research Evidence

EVD-001, EVD-002, SRC-105. Traceability: `research-traceability.md` row 12.

## Evidence Status

PARTIALLY_SUPPORTED

## Trade-offs

Portability vs breakage-maintenance burden and host-to-host trace-completeness
variance.

## Consequences

Adapter conformance suite; longitudinal breakage log (EXP-007); unobservable
host internals remain UNKNOWN by construction (Honesty Axiom — never inferred
into existence).

## Assumptions

MCP/CLI stability is sufficient; adapters stay thin; headless harness is fair.

## Open Questions

Breakage rate? MCP-vs-CLI overhead? Headless fairness across models? (GAP-008)

## Future Experiment

EXP-007.

## Phase Boundary

### Phase 2

Architectural decision: method verdicts (REQUIRED/OPTIONAL/DROPPED),
common-vs-specific split, observability limits.

### Phase 3

Future contract implications: capability matrix schema, dispatch/trace shapes,
conformance suite — to be defined, not defined here.

### Phase 4+

Future specification/implementation/verification implications: per-adapter specs,
bridge implementation, longitudinal tracking; no adapter is implemented by
this ADR.
