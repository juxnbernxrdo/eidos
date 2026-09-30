# P2-ADR-002 — Repository Graph with k≤2 MSC Routing

**Status:** ACCEPTED (principle) + EXPERIMENTAL (granularity, thresholds)
**Date:** 2026-09-30 | **Supersedes-format-of:** `docs/adr/ADR-003-*` (retained)

## Context
Mid-context retrieval degrades (EVD-003); line-graphs add +32.8% relative
(EVD-005); RAG-vs-LC is conditional on model/length/task (EVD-016); order
preservation is cheap and effective (OP-RAG lineage).

## Problem
How to give agents enough repo structure without dumping the repo into context?

## Decision
Heterogeneous graph (graph.md: REQUIRED/PROPOSED/FUTURE nodes, 11-relation closed
set, EXTRACTED-ground-truth semantics) + MSC router (k≤2 traverse, signature
pruning, source-order assembly, boundary-pinned contracts, Self-Route escalation).
High-level query abstractions only (`traverse/callers/dataflow_slice/path`).

## Alternatives
Full-repo long-context (rejected: EVD-003/016 effective-use 10–20%); pure lexical
RAG (rejected: multi-hop failure, BABILong lineage); raw CPGQL exposure
(rejected: hallucination + fragility).

## Research Evidence
EVD-005, EVD-003, EVD-016 — traceability row 3.

## Trade-offs
Localization precision vs build/serve cost and staleness management.

## Consequences
Graph freshness becomes a first-class flag; context volume is a costed variable.

## Assumptions
Granularities interchangeable pending test; tree-sitter multilingual parity.

## Open Questions
Line vs entity vs CPG? k-bound and order policy universality? (GAP-002)

## Future Experiment
EXP-002.
