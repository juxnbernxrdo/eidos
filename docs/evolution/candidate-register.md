# Evolution Candidate Register (EVO-001 – EVO-003)

**Authority:** Phase 8 Evolution Governance  
**Source Baseline:** Phase 7 Handoff (`EIDOS-HANDOFF-PHASE-7-TO-8`)  
**Status:** CANONICAL CANDIDATE REGISTER  

---

## 1. Registered Evolution Candidates

```text
┌────────────────────────────────────────────────────────────────────────┐
│ EVO-001: Adaptive Early-Stopping on Repair Loops      ──► [ACCEPTED]   │
│ EVO-002: Multi-Session Project Memory Gating          ──► [PLANNED v1.1│
│ EVO-003: Polyglot Graph Parsing (Tree-Sitter)         ──► [PLANNED v1.2│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Granular Candidate Profiles

### Candidate `EVO-001`: Dynamic Adaptive Early-Stopping on Repair Loops
- **Target Subsystem:** [`src/eidos/orchestration/pipeline.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/orchestration/pipeline.py)
- **Empirical Motivation:** Phase 7 Experiment `EXP-003` established that repair iterations beyond $k=3$ yield $<10\%$ marginal task resolution, but consume $45\%$ of completion tokens. Specifically, when an agent repeats the identical syntax or logic failure across two consecutive attempts, running to $K=5$ leads to thrashing.
- **Proposed Solution:** Implement cycle detection in `execute_bounded_repair_loop`. If `oracle_trace[k] == oracle_trace[k-1]`, trigger early escalation to `PipelineStage.ESCALATED` with reason `REPETITIVE_ERROR_CYCLE_DETECTED`.
- **Target Metrics:** Token savings on unfixable tasks: $\approx 45.0\%$; Latency reduction: $\approx 40.0\%$.
- **Governance Status:** **`ACCEPTED`** (Ratified in Phase 8).

---

### Candidate `EVO-002`: Long-Horizon Multi-Session Project Memory Gating
- **Target Subsystem:** [`src/eidos/memory/manager.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/memory/manager.py)
- **Empirical Motivation:** In Phase 7 Ablation `EXP-002`, the isolated memory arm ($A_8$) yielded $0.0$ pp improvement on single-turn benchmark tasks because memory was empty at task start.
- **Proposed Solution:** Extend memory manager to index historical repair patches and recurring test failures across multiple consecutive sessions, while maintaining strict project isolation.
- **Target Metrics:** Multi-session repair convergence speed ($\Delta TTI \le -30\%$).
- **Governance Status:** **`SCHEDULED_FOR_V1.1`** (Awaiting multi-session benchmark suite).

---

### Candidate `EVO-003`: Polyglot Graph Parsing Adapter
- **Target Subsystem:** [`src/eidos/intelligence/parser.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/intelligence/parser.py) & [`src/eidos/graph/engine.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/graph/engine.py)
- **Empirical Motivation:** Phase 7 External Validity analysis identified that the AST extractor currently supports only Python standard syntax.
- **Proposed Solution:** Integrate Tree-Sitter grammar bindings to parse TypeScript (`.ts`, `.tsx`), Rust (`.rs`), and Go (`.go`) into Eidos's closed 21 node types and 11 edge relations.
- **Target Metrics:** Polyglot repository indexing accuracy ($>95\%$ symbol extraction).
- **Governance Status:** **`SCHEDULED_FOR_V1.2`** (Requires dependency decision record for tree-sitter bindings).
