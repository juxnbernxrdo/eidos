# SPEC-005 — Storage-Agnostic Repository Graph Engine

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of the Repository Graph Store: representing codebase structure, governance specifications, and epistemic relationships as a heterogeneous directed property graph.

## 3. Scope
Node and edge management, epistemic provenance preservation, neighborhood traversal ($k \le 2$), call graph queries, snapshot serialization, and freshness tracking.

## 4. Non-Goals
- Does not lock Eidos to a single database engine (storage-agnostic).
- Does not visualize graphs for humans (CLI exports JSON; visualization is external).
- Does not permit unverified LLM inferences to overwrite AST ground truth.

## 5. Source Requirements
- `REQ-GRAPH-001`: Storage-Agnostic Heterogeneous Graph
- `REQ-GRAPH-002`: Epistemic Provenance on Graph Edges
- `REQ-GRAPH-003`: Bounded Neighborhood Queries ($k \le 2$)

## 6. Architectural Basis
- `docs/architecture/graph.md`: Conceptual model, node taxonomy, 11-relation closed set.
- `docs/adr/P2-ADR-002`: Graph router with $k \le 2$ bounding.
- `docs/research/evidence-registry.md`: EVD-005 (+32.8% resolution via RepoGraph), EVD-013 (graph modularity).

## 7. Contract Dependencies
- `GRAPH-CONTRACT-001`: Graph Store Contract schema (`schemas/contracts/graph/graph-store.schema.json`).
- `CORE-CONTRACT-005`: Evidence Contract.

## 8. Behavioral Requirements
The graph store maintains $G = (V, E)$. Nodes represent software and governance entities across 21 types. Edges represent directed relations across 11 closed types. 
- AST-extracted edges carry `epistemic_provenance: EXTRACTED` and `confidence: 1.0`.
- LLM-inferred edges carry `epistemic_provenance: INFERRED` and confidence $< 1.0$.
- Inferred edges conflicting with extracted facts must be recorded as `CONFLICTS_WITH` and quarantined.

## 9. Inputs
- Structural AST parsing events and file change deltas.
- High-level query requests: `traverse`, `callers`, `callees`, `dataflow_slice`, `path`, `explain`.

## 10. Outputs
- Subgraphs, node ego-neighborhoods, and paths.
- Graph snapshots conforming to `schemas/contracts/graph/graph-store.schema.json`.

## 11. State Model
Tracks freshness relative to the underlying repository Git commit:
- `FRESH`: In sync with current Git HEAD commit.
- `STALE`: Working directory modified since last graph extraction.
- `REBUILD_REQUIRED`: Branch switch or merge conflict detected.

## 12. Invariants
- `INV-001`: Graph extraction is pure AST/compiler analysis; no model provider dependencies.
- `INV-002`: Zero edges connect to files or entities outside the repository workspace root.
- `INV-009`: `EXTRACTED` ground-truth facts always take precedence over `INFERRED` edges.

## 13. Preconditions
- Files targeted for extraction must be valid UTF-8 source files within the workspace.

## 14. Postconditions
- Query results must return only nodes and edges reachable within the requested hop limit ($k \le 2$).

## 15. Failure Semantics
Syntax errors in source files do not crash the engine; unparseable files are recorded with `Finding` nodes of category `BUG` and severity `HIGH`.

## 16. Security Requirements
- Read-only queries must never mutate repository files.
- Queries cannot traverse filesystem symlinks pointing outside the repository workspace root.

## 17. Observability Requirements
- Emits telemetry for total node count, edge count, graph density, and God-node degree centralities on snapshot creation.

## 18. Edge Cases
- Circular dependencies: Traversal algorithms must maintain a visited set to prevent infinite recursion.
- Massive repositories: Nodes $> 5000$ prune neighborhood queries strictly to direct $k=1$ callers/callees.

## 19. Acceptance Criteria
### `AC-005-01` (Heterogeneous Node and Edge Validation)
```gherkin
Given a Python file with a class and function
When the graph engine extracts the file AST
Then it creates File, Class, and Function nodes connected by DEFINED_BY edges with EXTRACTED provenance and confidence=1.0.
```

### `AC-005-02` (Epistemic Precedence Over Inference)
```gherkin
Given an EXTRACTED DEFINED_BY edge between File and Function
When an agent proposes an INFERRED relation asserting the function is defined elsewhere
Then the graph engine records the conflict as CONFLICTS_WITH and preserves the EXTRACTED edge as ground truth.
```

### `AC-005-03` (Hop-Bounded Neighborhood Traversal)
```gherkin
Given a graph with a dependency chain of length 5 (A -> B -> C -> D -> E)
When a traverse query is executed from seed A with k_hops=2
Then the returned subgraph contains only {A, B, C} and excludes {D, E}.
```

## 20. Verification Strategy
Automated unit tests in `tests/specs/test_graph_store.py` verifying cyclic graph traversals, epistemic provenance preservation, and snapshot schema validation.

## 21. Traceability
- Research: EVD-005, EVD-013
- ADR: `P2-ADR-002`
- Contract: `GRAPH-CONTRACT-001`
- Requirements: `REQ-GRAPH-001`, `REQ-GRAPH-002`, `REQ-GRAPH-003`

## 22. Open Questions & Phase 5 Notes
- Final backend choice (in-memory NetworkX vs persistent SQLite/DuckDB) is a Phase 5 implementation decision.
- Incremental update performance under large git diffs to be benchmarked in Phase 7 (`EXP-002`).
