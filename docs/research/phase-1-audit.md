# EIDOS Phase 1 Audit — Second-Pass Reinforcement

**Date:** 2026-09-30 | **Auditor:** Phase-1 reinforcement pass | **Scope:** `01_RESEARCH_REPORT.md`, `02_EVIDENCE_MATRIX.md` (EV-01..EV-12), `03_REFERENCE_SYSTEMS_ANALYSIS.md` (13 systems), `04_HYPOTHESIS_FORMALIZATION.md`, `05_RUNTIME_EVALUATION_PYTHON_VS_NODE.md`, plus `docs/architecture/*` and `docs/adr/ADR-001..008` as decision consumers.

## Verdict summary

- **Well-supported (keep):** ACI matters (EV-01→EVD-001); phased pipelines beat open loops on cost (EV-02→EVD-002); mid-context degradation (EV-03→EVD-003); repo graphs help (EV-05→EVD-005); CodeAct action space (EV-08→EVD-006); oracle-gated repair (EV-09→EVD-009).
- **Partially supported (qualify):** fresh subagents (EV-04: headline `41%` unverifiable → replace with Anthropic 2025 multi-agent +90.2% research / 15× tokens, non-code); skill risk (EV-07: `14%` figure unrecovered → replace with SkillScan 2026 + repo-aware study); OpenShell policy-as-physics (EV-06: mechanism FACT, SWE-efficacy UNKNOWN, alpha).
- **Poorly supported (reclassify, do not delete):** EV-10 SDD efficacy (`88%` INTERPRETATION→decision is HYPOTHESIS→DESIGN_CHOICE leap); EV-11 community-detection transfer (math FACT, SWE transfer HYPOTHESIS); EV-12 H1 super-additivity + `75%` (no methodology; split phenomenon vs threshold); all v1 `High (90-99%) / Absolute (100%)` confidences (no scoring methodology — removed, replaced by source-quality categories).
- **Missing and now added:** SWE-bench leakage/inflation (SWE-Bench+ 32.67% leak, Verified 22.4%→10.0%; mutation overestimation 20-50%; DeepSWE audit as UNVERIFIED threat model); self-repair limits (Silver-Bullet, CYCLE, Revisit); RAG-vs-LC routing (Self-Route, LaRA, LongContextRAG, BABILong, LongBench v2); memory contamination/admission (ConsistencyGate ρ, MemoryGraft, MINJA, Mem0/A-MEM); GEPA/DSPy vs DGM/Gödel distinction; Agent Skills open standard (Oct/Dec 2025) + MCP donation; CPG/CodexGraph alternative to line-graphs; multilingual/multi-file benchmarks (Multi-SWE-bench, Commit0, CrossCodeEval, RepoEval, SWE-MM); OSS snapshots (Hermes/OpenClaw/OpenCode/SpecKit/OpenShell/SkillSpector/OCR/worktrunk/skills.sh/Graphify); Loop Engineering demotion (practitioner vocabulary, not academic construct).

## What was correct in v1

1. Direction of all five pillars (harness, context/graph, execution, governance, security) matches 2025-26 primary literature.
2. ACI + Agentless + Lost-in-the-Middle + RepoGraph + CodeAct + Reflexion citations are real, correctly attributed, and quantitatively close to papers (modulo §Corrections).
3. Epistemic tagging (FACT/EVIDENCE/INTERPRETATION/HYPOTHESIS/DESIGN DECISION) and EXTRACTED-vs-INFERRED discipline anticipated 2026 skill/memory-security consensus.
4. H0/H1 formalization with confounders (contamination, flaky tests, provider drift, prompt sensitivity) remains the right frame; benchmarks named (SWE-Verified, CrossCodeEval, RepoEval) remain correct, now extended.
5. Runtime evaluation conclusion (Python-core hybrid) is defensible as DESIGN_DECISION, correctly argued on tree-sitter/NetworkX/research-ecosystem grounds.

## What was incomplete

1. No leakage/contamination analysis (now EVD-015/GAP-001).
2. No contradictory results (self-repair limits, RAG-vs-LC conditionality, reasoning-models-narrow-gap, multi-agent cost, memory contamination, skill flag-base-rate with context).
3. No 2025-26 sources: Anthropic effective/context/multi-agent doctrine, Agent Skills spec, MCP donation, GEPA, DGM, A-MEM/Mem0/ConsistencyGate, FormalBench/SpecBench, Multi-SWE-bench/Commit0, CPG/CodexGraph, OpenHands/SWE-smith.
4. OSS analysis (03) had zero benchmark grounding and stale/misattributed entries (OpenCode `anomalyco/opencode` fork vs `sst/opencode`; self-reported precision/token claims unverified).
5. Risk register had 8 risks but no base-rate quantification, no skill-flag persistence analysis, no memory-contamination or provider-drift measurement plan.

## What was wrongly supported (corrections applied, history preserved in claims.md)

| # | v1 claim | Problem | Correction |
|---|---|---|---|
| 1 | EV-04 `41% fresh-subagent gain (Anthropic 2024)` | Figure not recoverable in primary pages | RETIRED → EVD-004 (SRC-102, qualified, non-code) |
| 2 | EV-07 `14% wild skills compromised` | Source not recovered; NVIDIA vuln-rate claims (26.1%/5.2%) unverified | Replaced by SRC-027/028 with persistence analysis |
| 3 | Confidences `99/98/95/94/92/100%` | No objective scoring methodology | Removed; source-quality categories only |
| 4 | EV-10 SDD `88%` → build SDD | Efficacy evidence absent (Spec Kit has no benchmark) | HYPOTHESIS + EXP-003 |
| 5 | EV-11 community detection `Absolute (100%)` → integrate | Math FACT ≠ SWE transfer | Split CLM-011; EXPERIMENTAL |
| 6 | EV-12 H1 `75% empirical backing` | Cross-paper comparison cited as backing | Split CLM-001/014; threshold needs EXP-001 |
| 7 | OpenShell/SkillSpector as production standards | Both alpha; efficacy vs SWE unmeasured | DESIGN_CHOICE + GAP/EXP |
| 8 | 2026 model numbers (if cited) | Aggregator inconsistency | Quarantined U-001; never EVIDENCE |

## Contradictions found (unresolved — see architecture-traceability.md)

- Autonomous ACI agents (SWE-agent) vs fixed pipelines (Agentless): cost/robustness vs generality.
- More context (LC) vs minimal routing (RAG/MSC): conditional on model/length/task (Self-Route/LaRA).
- Multi-agent gains (+90.2% research) vs 15× tokens + orchestration fragility.
- Reflection helps (Reflexion/Self-Debug w/ oracle) vs self-repair ≈ sampling (Silver-Bullet) vs human feedback 1.58×.
- Graph granularity line (RepoGraph) vs entity (CodexGraph) vs property (CPG): no head-to-head on same harness.
- Memory helps dialogue (A-MEM/Mem0) vs contamination cascade (ConsistencyGate/MemoryGraft/MINJA) vs project-scoped precedent (Anthropic memory).
- Reasoning test-time compute narrows single-file gap (04 §5.2 qualification stands) but cannot fetch unretrieved files.
- Skill flag rates collapse 99.5% with repo context (46.8%→0.52% persistence): naive scanning over-blocks.

## Open questions remaining (→ research-gaps.md GAP-001..010, experimental-agenda.md EXP-001..007)

Leakage-free H×M×C factorial; graph granularity; spec efficacy; K-bound + semantic stopping; memory with ρ-gate; skill-gate precision/recall; sandbox penetration + overhead; reasoning-vs-harness crossover (C_threshold); multilingual generalization.
