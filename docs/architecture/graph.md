# Graph Architecture (Phase 2)

**Status:** ARCHITECTED | Research basis: EVD-005 (line-graph +32.8%), CodexGraph
entity schema, CPG property graphs; granularity OPEN (GAP-002/EXP-002).

## 1. Conceptual model

`G = (V, E)` heterogeneous directed graph. Confidence lives on edges (data-model.md).

### Nodes — REQUIRED (Phase 3 schemas) / PROPOSED / FUTURE

- REQUIRED: `FILE, DIRECTORY, MODULE, CLASS, FUNCTION, TEST, SPEC, TASK, CONTRACT, RULE, SKILL, FINDING`
- PROPOSED: `API, DATABASE, TABLE, COMMIT, SESSION, AGENT, FEATURE`
- FUTURE (only if EXP-002/006 justify cost): statement-level nodes, cross-repo nodes

### Relations (closed set for Phase 3; additions need ADR)

`IMPLEMENTS, DEPENDS_ON, DEFINED_BY, TESTED_BY, DOCUMENTED_BY, MODIFIED_BY,
VIOLATES, SATISFIES, DERIVED_FROM, CONFLICTS_WITH, SUPERSEDES`
(+ `CALLS/REFERENCES/IMPORTS` as закономірні mechanical sub-relations of DEPENDS_ON
if line/entity granularity requires — OPEN, EXP-002).

## 2. Ownership / persistence / update / consistency

- Owner: Graph Builder (write), all domains (read via Querier).
- Persistence: versioned JSON snapshot (`graph/repository_graph.json` lineage;
  format finalized Phase 3). Full history reconstructible from event log.
- Update: incremental on commit/merge (`update` hook concept, Graphify-compatible);
  full rebuild fallback. Staleness is a first-class flag (`graph_freshness`).
- Consistency: EXTRACTED edges are ground truth; INFERRED edges expire unless
  confirmed; `AMBIGUOUS`/conflicting edges quarantined, never silently merged.

## 3. Queries (Phase 3 contracts; semantics fixed now)

- `traverse(seed, k≤2, edge_whitelist)` — default bound (EVD-005: k≥3 = noise).
- `callers / callees / dataflow_slice` — high-level abstractions; raw CPGQL/AST
  never exposed to task agents (lessons: CodexGraph fragility, CPG hallucination).
- `path(a, b) / explain(node) / community(node)` — cohesion + God-node metrics
  advisory only (CLM-011 transfer HYPOTHESIS).

## 4. Limits

- No statement-level graph by default (cost); no cross-repo edges without explicit
  opt-in (INV-002); no INFERRED edge may gate verification (INV-003 corollary).
- 5k+ node visualization is out of scope for agents (human tooling only).
