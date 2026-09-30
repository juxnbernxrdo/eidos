# Research Traceability Matrix (Phase 2)

**Status:** ARCHITECTED | Full chain: `docs/research/evidence-registry.md`
(EVD) → `claims.md` (CLM) → `docs/adr/P2-ADR-XXX` → future EXP. Source details:
`docs/research/sources.md`.

**Status vocabulary (single value per row — corrective governance):**
`SUPPORTED` / `PARTIALLY_SUPPORTED` / `DESIGN_CHOICE` / `RESEARCH_HYPOTHESIS` /
`CONFLICTING_EVIDENCE` / `OPEN`. No row may read SUPPORTED without cited
real evidence; split rows separate what is shown from what is still open.

| Architecture Decision | Research Evidence | Source | Epistemic Status | Assumption | Trade-off | Future Experiment |
|---|---|---|---|---|---|---|
| Phased non-bypassable pipeline | Agentless 32% @ $0.70; ACI cost 8-13× | SRC-003, SRC-002 (EVD-002/001) | PARTIALLY_SUPPORTED | Transfers to polyglot repos; ceremony tolerable | Robustness/cost vs generality, friction (RSK-07) | EXP-003 |
| SDD spec-before-code efficacy | Spec Kit process-only; spec-reasoning <45%; function-scale formal only | EVD-010/011/012 | RESEARCH_HYPOTHESIS | Machine-checked specs move VSR/RR | Ceremony cost vs grounding benefit | EXP-003 |
| Verification-first + bounded repair | Reflexion/Self-Debug w/ oracle; silver-bullet limits | SRC-009/010/012 (EVD-009) | PARTIALLY_SUPPORTED | Oracle-gated repair generalizes | Convergence vs token burn, false stops | EXP-004 |
| Repair bound value (K) | No controlled K derivation exists | — (ARR-03) | OPEN | A single K fits all task classes | Convergence vs burn | EXP-004 |
| k≤2 graph router + MSC (principle) | RepoGraph +32.8% relative; U-curve; Self-Route | SRC-013/008/016 (EVD-005/003/016) | SUPPORTED | Bounded traversal + order preservation suffice | Precision vs build/serve cost | EXP-002 |
| Graph granularity + community-metric transfer | No head-to-head on one harness; Q-transfer unmeasured | GAP-002 (CLM-011) | RESEARCH_HYPOTHESIS | Line/entity/CPG interchangeable | Precision vs cost | EXP-002 |
| Contract subagents, star topology | Multi-agent +90.2% (research task); contamination | SRC-102 (EVD-004) | PARTIALLY_SUPPORTED | Code-task transfer; 3-5 lanes | Focus vs orchestration complexity | EXP-002 |
| Subagent cost scaling | ~15× tokens multi-vs-chat lineage | SRC-102 (EVD-004) | CONFLICTING_EVIDENCE | Cost scales to code tasks | Quality vs 15× tokens | EXP-002 |
| CodeAct action-space paradigm | +20% vs JSON across 17 LLMs | SRC-004 (EVD-006) | SUPPORTED | Programmatic tasks match benchmark regime | Expressiveness vs reviewability | EXP-005 |
| Sandboxed CodeAct inside Eidos | No Eidos sandbox run exists | — | OPEN | Sandbox contains exec without killing utility | Power vs escape surface | EXP-005 |
| OS sandbox + skill gateway (architecture) | Bypassable prompts; 31k-skill scan; repo-aware rates | SRC-204/027/028 (EVD-007/008) | PARTIALLY_SUPPORTED | Linux-first acceptable; pinning scales | Safety vs latency, false blocks | EXP-005 |
| Gateway risk-threshold value (risk<25-style) | No ROC calibration exists | — (ARR-03) | OPEN | A single threshold fits all skill classes | Safety vs false blocks | EXP-005 |
| Tripartite memory utility (SWE) | Dialogue-only gains; ρ-contamination formalized | SRC-022/023/029 (EVD-017) | RESEARCH_HYPOTHESIS | Sanitization preserves utility | Recall vs contamination + approval burden | EXP-005 |
| Event log + passports (governance) | Reproducibility need; EventStream precedent | EVD-015, SRC-005 | DESIGN_CHOICE | Logs enable ablation; cost negligible | Auditability vs storage/overhead | EXP-001 (as instrument) |
| Python-core hybrid runtime | trade-off matrix, ecosystem argument | 05_RUNTIME_EVALUATION | DESIGN_CHOICE | uv parity; TUI edge tolerable | Depth vs startup/DX | Bridge prototype |
| Invariant synthesis + drift thresholds | FormalBench function-scale only | SRC-031 (EVD-012) | RESEARCH_HYPOTHESIS | Synthesis precision sufficient | Safety vs false-block regression | EXP-006 |
| Gated improvement (GEPA-style) | GEPA +6pp @35× fewer rollouts | SRC-024 (EVD-018) | RESEARCH_HYPOTHESIS | Metric + val-set exist | Learning vs oversight cost | EXP-006 |
| Open-ended evolution | DGM sandboxed-only + oversight requirement | SRC-025 (EVD-018) | RESEARCH_HYPOTHESIS | — (forbidden-by-default, ARR-04) | Divergence risk | EXP-006 |
| Harness adapters + MCP | Harness deltas; MCP standard | SRC-002/105 | PARTIALLY_SUPPORTED | MCP/CLI stability | Portability vs breakage maintenance | EXP-007 |
| Loop Engineering vocabulary | Practitioner glossaries only | SRC-300..304 (EVD-019) | DESIGN_CHOICE | Shared language helps | Clarity vs false rigor | Formalization (deferred) |
| H1 threshold claim | Cross-paper synthesis, era-bound | EVD-014 | RESEARCH_HYPOTHESIS | C-vector measurable | — | EXP-001 |
