# Interface → Contract Readiness Map (Phase 2)

**Status:** ARCHITECTED | This matrix is NOT a contract. It is a **readiness map
for Phase 3**: what Phase 2 settled, what is conceptually known, and what Phase 3
must still decide. Per-interface audits (§7) follow the table.

| Interface | Phase 2 Responsibility | Inputs Conceptually Known | Outputs Conceptually Known | Invariants | Open Decisions | Phase 3 Contract Required |
|---|---|---|---|---|---|---|
| HarnessAdapter | Harness portability boundary; dispatch + trace collection | Task contract, workspace fingerprint, capability matrix | Execution id, structured result, full observation trace | INV-001 (no provider coupling in Core); least-privilege; no self-certification | Per-harness specifics; MCP-vs-CLI overhead; install-scope | YES |
| ContextRouter | Deliberate context selection; MSC assembly | Task contract, graph neighborhood, rules, token budget | MSC payload (signatures, pinned contracts, provenance tags) | P8 (never maximize); EXTRACTED > INFERRED; quarantine by default | k-bound, ranking weights, escalation signal, cache policy | YES |
| GraphStore | Repo-knowledge abstraction; provenance-preserving queries | Repo snapshot, traversal seeds, edge whitelist | Ranked subgraphs, paths, communities (advisory), provenance per edge | EXTRACTED = ground truth; INFERRED expirable, never gates verification; INV-002 (no cross-repo edges w/o opt-in) | Granularity (line/entity/CPG-slice); update cadence; 5k+ node handling | YES |
| Verifier | Layered verification; bounded repair; escalation | Task, patch, policy set (tests/types/lint/contracts/invariants/security/drift) | VerificationResult per layer; repair trace; CONVERGED/ESCALATED verdict | INV-003 (claims ≠ evidence); repair requires external oracle | K-bound; per-layer thresholds; semantic stopping; judge quality | YES |
| EventLog | Append-only persistence; replay; anchoring for audit + ablation | Events (actor/action/input/output/evidence/result/git-state) | Projected state, passports, evaluation_run.json | Append-only (corrections are new events); HEAD-anchored; P10 | Retention/volume policy; anchor technology; passport minimal fields | YES |

## §7 audits

### HarnessAdapter
- **Problem solved:** host-harness portability without leaking specifics into Core
  (P1/P2, INV-001). **Evidence:** EVD-001/002 (harness moves outcomes); SRC-105
  (MCP standard). **Hypothesis part:** MCP/CLI stability; headless fairness.
- **Common:** dispatch, output/trace collection, capability declaration, MCP stdio.
  **Harness-specific:** Antigravity brain-artifacts, Claude hooks/compaction,
  OpenCode LSP/TUI, Codex/Cursor cloud boundaries, Hermes daemon (harness.md).
- **Phase 3 must resolve:** capability-matrix schema, dispatch/trace shapes,
  conformance suite, install-scope policy (EXP-007 inputs).

### ContextRouter
- **Problem solved:** retrieval collapse under full-repo dumps (EVD-003) and
  conditional RAG-vs-LC regimes (EVD-016). **Evidence:** EVD-003, EVD-016.
- **MSC meaning:** target nodes full + neighbors pruned to signatures/types/
  contract comments; source-order assembly; contracts pinned at boundaries;
  escalation only on explicit `unanswerable`.
- **Still open:** k-bound value, ranking weights, escalation signal definition,
  cache-breakpoint policy (EXP-002). **Phase 3 contract:** `route` signature,
  MSC payload shape, provenance-tag vocabulary.

### GraphStore
- **Experimentally implemented part:** early AST builder/querier
  (`src/eidos/graph/engine.py`, `intelligence/` — EXPERIMENTAL bootstrap, 17
  tests green; NOT the architecture).
- **Architecture-only part:** epistemic edge semantics, REQUIRED/PROPOSED/FUTURE
  taxonomy, high-level query abstractions, incremental-update + freshness model.
- **Provenance preserved:** per-edge EXTRACTED/INFERRED/USER_CONFIRMED/
  AGENT_PROPOSED with confidence; quarantine for conflicts.
- **Conceptual operations:** `extract / traverse / query / provenance / path /
  explain / community`. **Phase 3 must define:** snapshot schema, traversal
  signature, freshness flag, update-hook contract (granularity decided by EXP-002).

### Verifier
- **Conceptual layers:** tests, static types, lint, contracts, invariants,
  security, drift (verification.md) with Verification-vs-Validation split.
- **Experimentally implemented:** early test/type/lint runner
  (`src/eidos/verification/runner.py`) and invariant checker
  (`src/eidos/intelligence/invariants.py`) — bootstrap, uncalibrated.
- **Pending:** contracts/invariants/security/drift layers as contracts; K-bound;
  semantic stopping; judge-quality study.
- **Still open:** all thresholds (K, risk, ΔQ, coverage) — DESIGN_CHOICE pending
  EXP-004/006 (ARR-02/03). **Phase 3 contract:** `VerificationResult` shape,
  CONVERGED predicate, ESCALATE payload.

### EventLog
- **Append:** hash-chained, immutable; corrections are new SUPERSEDES events.
- **Replay:** `S_t = Fold(S_0, [e_1..e_t])`; `state.json` is a projection,
  `events.jsonl` the truth.
- **Anchor:** Git-HEAD binding per event; cryptographic evidence refs for
  benchmark-grade runs (`evaluation_run.json`).
- **Relation to Progress:** log is the store; Projector, Passports, and Reports
  are projections (progress.md).
- **Phase 3 must formalize:** `event` schema, fold semantics, retention policy,
  anchor technology, passport minimal fields. Early logger
  (`src/eidos/progress/logger.py`) is bootstrap, not the contract.
