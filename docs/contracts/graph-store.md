# Graph Store Contract (`GRAPH-CONTRACT-001`)

**Contract ID:** `GRAPH-CONTRACT-001`  
**Version:** 1.0.0  
**Status:** ACCEPTED  
**Owner Domain:** Graph  
**Machine Schema:** [`graph-store.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/graph/graph-store.schema.json)  
**Architecture Basis:** [P2-ADR-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-002-graph-msc-router.md), [graph.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/graph.md), [data-model.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/data-model.md), [EVD-005](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md)

---

## 1. Purpose & Storage-Agnostic Abstraction

The `GraphStore` contract formalizes the repository knowledge graph representing structural, semantic, and epistemic relationships across the software repository.

### Foundational Design Decision:
> The contract is strictly **storage-agnostic**. It defines the node schema, edge taxonomy, epistemic metadata, snapshot serialization, and high-level query signatures without binding Eidos to a concrete storage engine (e.g. NetworkX, SQLite, DuckDB, or Neo4j).

---

## 2. Complete Node Taxonomy

Every entity in the repository graph must belong to one of the following canonical node types:

| Category | Permissible Node Types | Semantic Definition |
|---|---|---|
| **Code Structure** | `File`, `Directory`, `Module`, `Class`, `Function` | AST and filesystem representations of source code units. |
| **System & Infrastructure**| `API`, `Database`, `Dependency` | Interfaces, external packages, and persistent stores. |
| **Verification & Quality** | `Test`, `Finding`, `Evidence` | Automated test suites, static findings, and execution evidence. |
| **Governance & Planning** | `Spec`, `SubSpec`, `Task`, `Contract`, `Rule`, `Feature` | SDD specifications, atomic tasks, schemas, and invariants. |
| **Execution & Agents** | `Agent`, `Skill`, `Session`, `Commit` | Active agents, declared skills, sessions, and Git commits. |

---

## 3. Closed Relation Taxonomy (11 Relations)

Edges represent directed relationships $A \xrightarrow{\text{relation}} B$ within a closed taxonomy:

1. `IMPLEMENTS`: Code entity realizes a `Spec`, `SubSpec`, or `Contract`.
2. `DEPENDS_ON`: Entity imports, calls, or requires another entity.
3. `TESTED_BY`: Code entity covered or verified by a `Test` entity.
4. `DOCUMENTED_BY`: Entity explained by documentation or architectural notes.
5. `DEFINED_BY`: Symbol defined inside a specific `File` or `Module`.
6. `MODIFIED_BY`: Entity changed by a `Commit` or `Task`.
7. `VIOLATES`: Code or change breaches an `Invariant`, `Rule`, or `Contract`.
8. `SATISFIES`: Verification run or patch satisfies a required `Invariant` or `Spec`.
9. `DERIVED_FROM`: Knowledge entity derived from an ancestor or source file.
10. `CONFLICTS_WITH`: Inferred or proposed claim contradicts an extracted fact.
11. `SUPERSEDES`: New version or decision replaces an older predecessor.

---

## 4. Epistemic Provenance & Confidence Model

Every edge carries epistemic provenance to prevent hallucinated relationships:

```text
Edge (Source, Target, Relation)
  ├── epistemic_provenance: EXTRACTED | INFERRED | USER_CONFIRMED | AGENT_PROPOSED
  ├── confidence: float ∈ [0.0, 1.0]
  └── evidence_ref: optional URI or hash to verification trace
```

- **`EXTRACTED`** edges (confidence = 1.0) represent AST-derived truth (e.g. `DEFINED_BY`, direct static `DEPENDS_ON`).
- **`INFERRED`** edges (confidence $< 1.0$) represent heuristic semantic links; they expire on code modification and **may not gate verification**.
- **Quarantine Rule**: Conflicting edges (`CONFLICTS_WITH`) are quarantined and excluded from MSC assembly until resolved.

---

## 5. Snapshots & Freshness Tracking

- **Snapshots**: Serialized via `snapshot` payload, capturing `node_count`, `edge_count`, `git_commit`, and UTC timestamp.
- **Freshness Flag (`graph_freshness`)**:
  - `FRESH`: Graph state corresponds 1:1 with current Git `HEAD`.
  - `STALE`: Filesystem diff detected since last build; incremental update advised.
  - `REBUILD_REQUIRED`: Major structural changes or branch switch; full re-extraction required.

---

## 6. High-Level Query Interface

To prevent fragility and prompt hallucination (lessons from CodexGraph and raw CPGQL), task agents access the graph strictly through high-level query abstractions:

- `traverse(seed_ids, k_hops <= 2, edge_whitelist)`: Bounded neighborhood traversal.
- `callers(function_id)` / `callees(function_id)`: Structural call-graph resolution.
- `dataflow_slice(target_id)`: Focused def-use dependency extraction.
- `path(source_id, target_id)`: Shortest relationship path between two nodes.
- `explain(node_id)` / `community(node_id)`: Advisory structural summary.

---

## 7. Architectural Invariants Bound

- **INV-001 (Model Agnosticism)**: Graph extraction logic is pure AST/compiler analysis, independent of model providers.
- **INV-002 (Cross-Project Isolation)**: Zero cross-repository edges without explicit multi-repo configuration.
- **INV-005 (Provenance Preservation)**: Edge provenance can never be erased or defaulted to EXTRACTED without machine parsing.

---

## 8. Phase 4 Handoff

Phase 4 will specify:
- Tree-sitter and AST parser hook specifications per target language.
- Incremental graph update algorithms and cache invalidation policies.
- Detailed JSON serializations for Graphify interop.
