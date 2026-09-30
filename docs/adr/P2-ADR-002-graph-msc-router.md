# P2-ADR-002 — Repository Graph with k≤2 MSC Routing

**Date:** 2026-09-30 | **Canonical location:** `docs/adr/`
**Re-expresses (new format):** `docs/adr/ADR-003-repository-graph-ast-networkx.md` (retained as historical record)

## Status

ACCEPTED

## Context

Mid-context retrieval degrades sharply (EVD-003: U-curve); line-level repo graphs
add +32.8% mean relative resolution (EVD-005: RepoGraph); RAG-vs-long-context is
conditional on model, length, and task (EVD-016); order preservation is cheap and
effective (OP-RAG lineage in EVD-016).

## Problem

How to give agents enough repository structure without dumping the repository
into context?

## Decision

Heterogeneous graph (graph.md: REQUIRED/PROPOSED/FUTURE nodes, 11-relation closed
set, EXTRACTED-ground-truth semantics) plus MSC router (k≤2 traversal, signature
pruning, source-order assembly, boundary-pinned contracts, Self-Route escalation).
High-level query abstractions only (`traverse`, `callers`, `dataflow_slice`, `path`).

## Alternatives Considered

- Full-repo long-context — rejected: EVD-003/EVD-016 (effective use 10–20%).
- Pure lexical RAG — rejected: multi-hop failure (BABILong lineage in EVD-016).
- Raw CPGQL/AST exposure to task agents — rejected: hallucination and fragility
  (CodexGraph/CPG lessons in EVD-005 context).

## Research Evidence

EVD-005, EVD-003, EVD-016. Traceability: `research-traceability.md` row 3.

## Evidence Status

PARTIALLY_SUPPORTED

## Trade-offs

Localization precision vs graph build/serve cost and staleness management.

## Consequences

Graph freshness becomes a first-class flag; context volume becomes a costed
experimental variable; raw query languages stay hidden behind abstractions.

## Assumptions

Granularities (line/entity/CPG-slice) interchangeable pending test; tree-sitter
multilingual parity; source-order assembly suffices.

## Open Questions

Line vs entity vs CPG-slice? k-bound and order-policy universality? (GAP-002)

## Future Experiment

EXP-002.

## Phase Boundary

### Phase 2

Architectural decision: node/relation taxonomy, epistemic edge semantics, query
abstraction names, MSC assembly policies.

### Phase 3

Future contract implications: graph snapshot schema, `traverse`/`query` signatures,
MSC payload shape, freshness flag — to be defined, not defined here.

### Phase 4+

Future specification/implementation/verification implications: builder/querier
specs, incremental-update implementation, granularity ablation; no graph engine
is specified by this ADR.
