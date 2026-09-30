# EIDOS Architecture Traceability — Research → Decisions

**Date:** 2026-09-30 | **Status values:** SUPPORTED / PARTIALLY_SUPPORTED / HYPOTHESIS / DESIGN_CHOICE / INSUFFICIENT_EVIDENCE / CONFLICTING_EVIDENCE.
**Rule:** a HYPOTHESIS/DESIGN_CHOICE row is honest, not a failure. `ARCHITECTURE_REVIEW_REQUIRED` flags decisions whose basis changed.

| Architectural Decision (ADR / spec) | Research Evidence | Evidence Strength | Assumptions | Open Question | Status |
|---|---|---|---|---|---|
| ADR-002 SDD phased pipeline (Discovery→Spec→Plan→Implement→Verify→Converge, non-bypassable) | EVD-002 Agentless cost-efficiency; EVD-001 ACI cost; EVD-010 Spec Kit process-only; EVD-011 spec-reasoning <45% | Moderate (pipeline), Low (spec efficacy) | Phases transfer from Python SWE to polyglot Eidos; ceremony acceptable (micro-spec fast-path untested) | Does spec-vs-no-spec move VSR? (GAP-004/EXP-003) | PARTIALLY_SUPPORTED (pipeline) + HYPOTHESIS (spec efficacy) |
| ADR-002 Verification-first + bounded Reflexion K≤5 | EVD-009 oracle necessity; EVD-015 test weakness; EVD-012 formal path | High (oracle necessity) / Low (K=5 value) | K=5 generalizes; last-3 memory suffices; rollback unneeded | Optimal K + semantic stopping? (GAP-006/EXP-004) | PARTIALLY_SUPPORTED — K value is DESIGN_CHOICE |
| ADR-003 Repository Intelligence Graph (AST + epistemic edges) + k≤2 MSC router | EVD-005 RepoGraph +32.8%; EVD-003 U-curve; EVD-016 routing; EVD-019-order (OP-RAG) | High (k≤2 graph help) | Line/entity/CPG granularity interchangeable; tree-sitter multilingual parity; order-preservation suffices | Granularity head-to-head? (GAP-002/EXP-002) | SUPPORTED (principle) / HYPOTHESIS (granularity, Q-transfer CLM-011) |
| ADR-004 Contract-bounded fresh subagents, zero history | EVD-004 (non-code +90.2%, 15× cost); EVD-003 contamination; SRC-100/101 doctrine | Moderate | Code-task transfer; contract schema sufficient; 3-5-way parallelism optimal | Singleton-vs-contract ablation on code (GAP-003/EXP-002) | PARTIALLY_SUPPORTED + CONFLICTING_EVIDENCE (cost) |
| ADR-005 Tripartite memory + cross-project isolation | EVD-017 dialogue-only gains; SRC-029 contamination; SRC-107 project-scoped precedent | Low (SWE transfer) | Sanitization preserves utility; ρ-gate affordable; institutional memory worth cost | Memory on/off + ρ on SWE tasks? (GAP-007/EXP-005) | HYPOTHESIS (utility) + DESIGN_CHOICE (isolation) — over-designed if shipped unconditionally |
| ADR-006 Harness Adapter abstraction (Antigravity/Claude/OpenCode/headless) | EVD-001/002 harness deltas; EVD-015 harness-sensitivity; SRC-105 MCP standard | Moderate | MCP/CLI stable; adapters stay thin; headless mini-SWE-agent is fair baseline | Adapter breakage rate + overhead? (GAP-008) | PARTIALLY_SUPPORTED (need) / DESIGN_CHOICE (interface) |
| ADR-007 Skill gateway (AST+YARA, risk<25) + OS sandbox (Landlock/seccomp/OPA) | EVD-008 risk real; EVD-007 mechanism; EVD-006 sandbox need; SRC-108 T1-T3 | Moderate (risk), Low (threshold/pipeline efficacy) | risk<25 calibrated; semantic pass affordable; Linux-only acceptable | Gate precision/recall + sandbox pen-test (GAP-005/EXP-005) | PARTIALLY_SUPPORTED — risk<25 is DESIGN_CHOICE; sandbox INSUFFICIENT_EVIDENCE as SWE-efficacy |
| ADR-008 Event sourcing + feature passports + crypto anchoring | EVD-015 reproducibility need; SRC-005 EventStream precedent; no controlled efficacy | Low | Logs enable causal ablation; hashes trusted; cost negligible | Do passports change VSR/RR vs plain git? | DESIGN_CHOICE (governance, not efficacy claim) |
| ADR-001 Python-core hybrid runtime | 05_RUNTIME_EVALUATION trade-off matrix; EVD-005/006 ecosystem | Moderate (ecosystem argument) | tree-sitter/NetworkX/Pydantic outweigh Node TUI edge; uv parity holds | Head-to-head bridge prototype | DESIGN_CHOICE |
| Invariants ARCH-001 + 4-drift engine (INVARIANTS_AND_DRIFT_SPEC) | EVD-012 formal path (function-scale); EVD-015 drift need; no repo-scale invariant-synthesis eval | Low | LLM-inferred invariants precise enough; ΔQ<−0.05 calibrated; doc-link graph complete | Invariant precision/recall on 10 OSS repos (GAP-009) | HYPOTHESIS + DESIGN_CHOICE — highest over-design risk if enforced blocking before measurement |
| Controlled self-improvement (`.eidos/evolution/`) | EVD-018 GEPA strong / DGM sandboxed-only; SRC-024-026 | Moderate (GEPA), Low (open-ended) | Metric + val-set exist; human approves institutional writes | GEPA-on-Eidos demo; DGM-style sandbox eval (GAP-010/EXP-006) | HYPOTHESIS (EXPERIMENTAL, gated) — must not ship as autonomous |
| Loop Engineering as principle/architecture | EVD-019 practitioner-only | Low | Vocabulary aligns teams | Formalization + comparison | DESIGN_CHOICE (vocabulary) — NOT a scientific claim |
| H1 threshold (C_threshold crossover) | EVD-014 synthesis; 04 §5.2 qualification | Low | Complexity vector measurable; reasoning-gap stable | Factorial H×M×C (GAP-001/EXP-001) | HYPOTHESIS |

## Active conflicts (SOURCE A → RESULT A / SOURCE B → RESULT B / explanations / experiment)

1. **Autonomy:** SRC-002 (+10.7pp ACI agent) vs SRC-003 (32% fixed pipeline, −80% cost) → explanations: era models, task generality, cost metric → EXP-001 C0..C4 ablation.
2. **Context volume:** SRC-016/034 (LC wins w/ SOTA) vs SRC-008/018 (RAG/MSC wins, effective 10-20%) → explanations: model, length, task type → Self-Route policy EXP-002.
3. **Agents:** SRC-102 (+90.2%, research) vs 15× tokens + fragility → explanations: task decomposability, effort-scaling → EXP-002 code ablation.
4. **Repair:** SRC-009/010 (helps w/ oracle) vs SRC-012/030 (≈sampling w/o oracle; human 1.58×) → explanation: feedback quality → EXP-004 K-sweep + judge study.
5. **Graphs:** SRC-013 (line) vs SRC-014 (entity) vs CPG (property, 43% open-weight Lite) → no shared harness → EXP-002 granularity arm.
6. **Memory:** SRC-022/023 (dialogue gains) vs SRC-029/MemoryGraft/MINJA (contamination) → explanation: admission control → EXP-005 ρ-gated ablation.
7. **Skills:** SRC-028 (46.8% flagged) vs 0.52% persist w/ context → explanation: base-rate + context → EXP-005 gate calibration.
8. **Reasoning vs harness:** 04 §5.2 (reasoning narrows single-file gap) vs EVD-005 (graph still adds pp) → explanation: C_threshold → EXP-001 complexity sweep.

## ARCHITECTURE_REVIEW_REQUIRED (do not auto-change; record why)

- **ARR-01 — Memory:** ship ADR-005 as *opt-in experimental* (project memory only; institutional writes human-gated; ρ tracked) until EXP-005 passes. Reason: EVD-017 SWE-transfer absent + contamination formalized.
- **ARR-02 — Invariants/drift blocking:** ship as *advisory before blocking* until GAP-009 measured. Reason: synthesis precision unknown; false-positive blockage is a regression risk (RSK-07).
- **ARR-03 — K=5 + risk<25 + ΔQ<−0.05 + k≤2-only:** mark all four constants DESIGN_CHOICE with calibration experiments (EXP-004/005/002). Reason: values have no controlled derivation.
- **ARR-04 — Self-evolution:** prohibit open-ended code self-modification outside sandbox+human approval until EXP-006. Reason: DGM requires oversight; Microsoft 2026 diminishing-returns warning.
- **ARR-05 — 2026 model citations:** forbid U-001 numbers in architecture justification until reproduced via `eidos evaluate` pinned harness.
