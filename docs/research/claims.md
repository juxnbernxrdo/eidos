# EIDOS Claims Registry — Knowledge Classification

**Date:** 2026-09-30 | **Rule:** never present HYPOTHESIS→FACT, DESIGN_DECISION→EVIDENCE, IMPLEMENTED→VALIDATED, CORRELATION→CAUSATION.
**Kinds:** FACT / EVIDENCE / OBSERVATION / INTERPRETATION / HYPOTHESIS / DESIGN_DECISION / EXPERIMENTAL_RESULT / VALIDATED_RESULT / UNKNOWN.

| ID | Statement | Kind | Basis (EVD/SRC) | What would promote it |
|---|---|---|---|---|
| CLM-001 | ACI/harness changes produce measurable Δ in task success at fixed model | EVIDENCE (phenomenon) / HYPOTHESIS (Eidos threshold form) | EVD-001, EVD-002, EVD-005 | EXP-001 factorial H×M×C experiment → VALIDATED_RESULT |
| CLM-002 | Deterministic phased pipeline is more cost-efficient than unconstrained autonomous loops | EVIDENCE (era-bound) | EVD-002 (Agentless), EVD-001 (cost 8-13×) | Replicate on 2025-26 models + Verified → VALIDATED_RESULT |
| CLM-003 | Dumping full repo / mid-positioned contracts degrades retrieval | EVIDENCE | EVD-003, EVD-016 | Code-repo replication on frontier models → VALIDATED_RESULT |
| CLM-004 | Fresh contract-bounded subagents outperform long singletons | INTERPRETATION (code) / EVIDENCE (research-task, vendor) | EVD-004 (SRC-102, non-code) | EXP-002 ablation singleton vs contracts on SWE-Verified → EXPERIMENTAL_RESULT |
| CLM-005 | Repo graph (k≤2) improves localization/resolution and reduces tokens | EVIDENCE | EVD-005 (RepoGraph +32.8% rel.) | Eidos ablation C1 vs C2 (EXP-001) → VALIDATED_RESULT |
| CLM-006 | CodeAct execution is the right action space for verify/graph/invariants | EVIDENCE (non-SWE) + DESIGN_DECISION (SWE) | EVD-006 | Sandbox exec benchmark → VALIDATED_RESULT |
| CLM-007 | OS-level sandboxing is necessary (prompts insufficient) | FACT (bypassability) + DESIGN_DECISION (Eidos choice) | EVD-007 | Penetration suite pass + overhead measure → EXPERIMENTAL_RESULT |
| CLM-008 | Skill supply-chain risk is real and requires pre-install gates | EVIDENCE (risk) | EVD-008 | Eidos gate precision/recall eval → EXPERIMENTAL_RESULT |
| CLM-009 | Repair loops work only with external oracles; K≤5 is the right bound | EVIDENCE (oracle necessity) + DESIGN_DECISION (K=5 value) | EVD-009 | K-sweep 1..12 + LoopGain/SHP comparison (EXP-004) → EXPERIMENTAL_RESULT |
| CLM-010 | Explicit SDD specs improve agent outcomes | HYPOTHESIS | EVD-010 (no benchmark), EVD-011 (<45% spec-reasoning), EVD-012 (function-scale) | EXP-003 spec vs no-spec ablation → EXPERIMENTAL_RESULT |
| CLM-011 | Louvain/Leiden + God-node detection improves maintainability decisions | FACT (math) + HYPOTHESIS (SWE transfer) | EVD-013 | Correlation of Q/centrality with defect/regression rate → EXPERIMENTAL_RESULT |
| CLM-012 | Tripartite / persistent memory helps software-engineering agents | HYPOTHESIS | EVD-017 (dialogue-only) | Memory on/off ablation on multi-session tasks + ρ tracking → EXPERIMENTAL_RESULT |
| CLM-013 | Controlled self-improvement is safe and useful | HYPOTHESIS + DESIGN_DECISION (gated form) | EVD-018 (GEPA strong, DGM sandboxed) | GEPA-on-Eidos-pipeline demo + DGM-style sandbox eval → EXPERIMENTAL_RESULT |
| CLM-014 | Loop Engineering is a principle/architecture/methodology | INTERPRETATION (practitioner vocabulary) — NOT a validated construct | EVD-019 | Peer-reviewed formalization + comparative evaluation → at most METHODOLOGY; today: vocabulary |
| CLM-015 | More agents / more context / reflection is always better | UNKNOWN (conflicted; see architecture-traceability §Conflicts) | EVD-004 vs cost; EVD-003/016; EVD-009/012 | Conditional resolution per EXP-001/002/004 |
| CLM-016 | Eidos full stack (C4) dominates ablations C0..C3 | HYPOTHESIS | None yet (no Eidos run) | EXP-001 → EXPERIMENTAL_RESULT |
| CLM-017 | Python-core hybrid runtime is optimal for Eidos | DESIGN_DECISION (trade-off analysis, 05_RUNTIME_EVALUATION) | AST/graph ecosystem argument; no head-to-head build | Prototype both bridges + perf/DX measure → EXPERIMENTAL_RESULT |

## Previous Finding → New Evidence → Updated Interpretation (audit trail, no silent rewrites)

- EV-04 (v1: `41% fresh-subagent gain`, Anthropic 2024): **NOT recovered** in primary doctrine → RETIRED to U-004; replaced by EVD-004 (SRC-102 +90.2% research-eval, 15× tokens, non-code). Interpretation downgraded: INTERPRETATION, cost-bounded.
- EV-12 (v1: `Model×Harness super-additive, 75% empirical backing`): split into CLM-001 (phenomenon, EVIDENCE) + H1-threshold (HYPOTHESIS). `75%/99%/98%` confidence numbers in v1 had **no objective methodology** → removed; replaced by source-quality categories.
- EV-06/EV-07 (v1: OpenShell/SkillSpector as FACT/EVIDENCE with `100%/94%` and `14% wild`): the `14%` figure not recovered in NVIDIA repos; SkillSpector vuln-rate claims (26.1%/5.2%) UNVERIFIED → downgraded per EVD-007/008. Mechanism FACT retained; efficacy колонка UNKNOWN until Eidos eval.
- EV-10 (v1: SDD `88% INTERPRETATION→DESIGN DECISION`): reclassified CLM-010 HYPOTHESIS (EVD-010/011). Spec Kit is process, not efficacy evidence.
- EV-11 (v1: community detection FACT→DESIGN DECISION): split per CLM-011 (math FACT, transfer HYPOTHESIS).
- Added in reinforcement: leakage/inflation (EVD-015), RAG-vs-LC routing (EVD-016), memory contamination (EVD-017), GEPA/DGM distinction (EVD-018), Loop Engineering demotion (EVD-019/CLM-014), 2025-26 model numbers quarantined (U-001).
