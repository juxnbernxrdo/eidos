# Research Traceability Matrix (Phase 2)

**Status:** ARCHITECTED | Full chain: `docs/research/evidence-registry.md`
(EVD) → `claims.md` (CLM) → Phase-2 ADR → future EXP. Source details:
`docs/research/sources.md`.

| Architecture Decision | Research Evidence | Source | Epistemic Status | Assumption | Trade-off | Future Experiment |
|---|---|---|---|---|---|---|
| Phased non-bypassable pipeline | Agentless 32% @ $0.70; ACI cost 8-13× | SRC-003, SRC-002 (EVD-002/001) | PARTIALLY_SUPPORTED | Transfers to polyglot repos; ceremony tolerable | Robustness/cost vs generality, friction (RSK-07) | EXP-003 |
| Verification-first + bounded repair | Reflexion/Self-Debug w/ oracle; silver-bullet limits | SRC-009/010/012 (EVD-009) | PARTIALLY_SUPPORTED (K=DESIGN_CHOICE) | K + judge generalize | Convergence vs token burn, false stops | EXP-004 |
| k≤2 graph router + MSC | RepoGraph +32.8%; U-curve; Self-Route | SRC-013/008/016 (EVD-005/003/016) | SUPPORTED (principle) / HYPOTHESIS (granularity) | Granularity interchangeable; order suffices | Precision vs build/serve cost | EXP-002 |
| Contract subagents, star topology | Multi-agent +90.2% (research, 15×); contamination | SRC-102 (EVD-004) | PARTIALLY_SUPPORTED + cost conflict | Code transfer; 3-5 lanes | Quality vs 15× tokens, orchestration fragility | EXP-002 |
| CodeAct exec inside sandbox | +20% vs JSON across 17 LLMs | SRC-004 (EVD-006) | EVIDENCE (paradigm) / PROPOSED (Eidos sandbox) | Sandbox contains exec | Power vs escape surface | EXP-005 |
| OS sandbox + skill gateway | Bypassable prompts; 31k-skill scan; repo-aware rates | SRC-204/027/028 (EVD-007/008) | PARTIALLY_SUPPORTED (risk<25 OPEN) | Linux-first acceptable; pinning scales | Safety vs latency, false blocks | EXP-005 |
| Tripartite memory (opt-in) | A-MEM/Mem0 dialogue gains; ρ-contamination | SRC-022/023/029 (EVD-017) | RESEARCH_HYPOTHESIS (SWE) | Sanitization preserves utility | Recall vs contamination + approval burden | EXP-005 |
| Event log + passports | Reproducibility need; EventStream precedent | EVD-015, SRC-005 | DESIGN_CHOICE | Logs enable ablation; cost negligible | Auditability vs storage/overhead | EXP-001 (as instrument) |
| Python-core hybrid | tree-sitter/NetworkX/research ecosystem | 05_RUNTIME_EVALUATION | DESIGN_CHOICE | uv parity; TUI edge tolerable | Depth vs startup/DX | Bridge prototype |
| Invariants advisory-first | FormalBench function-scale only | SRC-031 (EVD-012) | HYPOTHESIS | Synthesis precision sufficient | Safety vs false-block regression | EXP-006 |
| Gated improvement; evolution forbidden | GEPA +6pp @35× fewer; DGM sandboxed | SRC-024/025 (EVD-018) | HYPOTHESIS (EXPERIMENTAL) | Metric + val-set exist | Learning vs oversight cost, divergence | EXP-006 |
| Harness adapters + MCP | Harness deltas; MCP standard | SRC-002/105 | PARTIALLY_SUPPORTED | MCP/CLI stability | Portability vs breakage maintenance | EXP-007 |
| Loop Engineering vocabulary | Practitioner glossaries only | SRC-300..304 (EVD-019) | DESIGN_CHOICE (not science) | Shared language helps | Clarity vs false rigor | Formalization (deferred) |
| H1 threshold claim | Cross-paper synthesis, era-bound | EVD-014 | RESEARCH_HYPOTHESIS | C-vector measurable | — | EXP-001 |
