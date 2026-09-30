# Open Specification Decisions & Research Watchlist

**Status:** LIVING (Phase 4 Specification Watchlist)  
**Authority:** Architectural Honesty & Research Gaps Registry  
**Constitutional Basis:** CONSTITUTION.md (Article I, Principle P3, Honesty Axiom)

---

## 1. Principles of Open Decisions in Phase 4

In accordance with the Eidos Honesty Axiom:
> **No open research question, empirical constant, or uncalibrated threshold may be artificially closed in Phase 4.**
> Where controlled experimental derivations do not yet exist, parameters are marked as `DESIGN_CHOICE` with documented default fallbacks, awaiting empirical resolution in Phase 7 pre-registered experiments (`EXP-001` through `EXP-007`).

---

## 2. Open Specification Decisions Catalog

| Open Area ID | Subject & Specification | Nature of Gap | Default Policy Fallback | Resolving Experiment |
|---|---|---|---|---|
| `OPEN-DEC-001` | Repair Limit Bound $K$ (`SPEC-002`, `SPEC-006`) | No controlled empirical derivation exists for optimal repair iterations across task classes (`ARR-03`). | $K = 5$ iterations default (`DESIGN_CHOICE`). | `EXP-004` (Reflexion Bounding) |
| `OPEN-DEC-002` | Skill Risk Cutoff Threshold (`SPEC-012`) | ROC curve calibration between false-positive blocking and malicious skill detection is unmeasured on agent skill sets (`ARR-03`). | $\text{risk} < 25$ default (`DESIGN_CHOICE`). | `EXP-005` (Skill Gateway Evaluation) |
| `OPEN-DEC-003` | Context Ranking & Graph Proximity Weights (`SPEC-004`) | Relative weighting between topological distance (k-hop) and semantic query match under token constraints is uncalibrated. | Strict topological distance preference ($k=0$ before $k=1$ before $k=2$) in source order. | `EXP-002` (Graph Granularity & Retrieval) |
| `OPEN-DEC-004` | Graph Storage Engine Selection (`SPEC-005`) | Memory vs latency vs persistence trade-off between NetworkX, SQLite, DuckDB, and Neo4j at $> 5000$ nodes. | Storage-agnostic interface; in-memory NetworkX with JSON snapshot default for Phase 5 bootstrap. | `EXP-002` (Graph Scale & Latency) |
| `OPEN-DEC-005` | Tripartite Memory Admission & Promotion ($\tau$) (`SPEC-011`) | SWE-bench transfer of dialogue memory gains is an unverified hypothesis (`GAP-007`); cascade risk $\rho$ uncalibrated. | Memory is strictly `opt-in only` (`ARR-01`); cross-project promotion requires human approval. | `EXP-005` (Memory Contamination) |
| `OPEN-DEC-006` | Verification Drift Tolerances ($\Delta Q$) (`SPEC-006`) | Mathematical threshold for flagging architectural or documentation drift without causing false-block CI deadlocks. | Advisory-first invariant checks (`ARR-02`); zero blocking pre-calibration. | `EXP-006` (Drift Engine Calibration) |
| `OPEN-DEC-007` | Autonomous Self-Evolution Efficacy (`SPEC-014`) | Open-ended self-evolution outside sandboxes carries divergence and degradation risks (`ARR-04`). | Gated pipeline only; autonomous runtime evolution is strictly `PROHIBITED`. | `EXP-006` (Self-Improvement Benchmarking) |
| `OPEN-DEC-008` | Harness Capability Parity & Overhead (`SPEC-009`) | Performance delta and IPC serialization latency between MCP stdio, CLI subshells, and direct sockets across 6 harnesses. | Capability matrix negotiation; headless harness serves as baseline reference (`EXP-001`). | `EXP-007` (Harness Stability & Parity) |

---

## 3. Policy for Phase 5 Implementers

1. **Configurable Parameters**: Phase 5 developers must implement all items above as **configurable settings** or injected policies, never as hardcoded immutable constants.
2. **Preserve Advisory Defaults**: When implementing verifiers and invariant checkers, blocking gates must remain configurable to respect the advisory-first mandate (`ARR-02`).
3. **No Premature Optimization**: Do not write complex speculative optimization algorithms for open areas until Phase 7 benchmark data provides empirical direction.
