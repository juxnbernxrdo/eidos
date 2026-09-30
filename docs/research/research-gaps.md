# EIDOS Research Gaps

**Date:** 2026-09-30. Each gap: problem, current/missing evidence, why it matters, proposed experiment, metrics, expected decision.

## GAP-001 — Leakage-free H×M×C factorial for H1 threshold
- **Problem:** Does standard-model-in-Eidos beat frontier-in-raw-bash beyond C_threshold? No single pinned factorial exists.
- **Current:** EVD-001/002/005/014 (suggestive, era-bound, cross-paper). **Missing:** same-harness, pinned-model, timestamp-gated H×M×C run.
- **Why:** Decides whether H1 is real and where it holds; guards all efficacy claims.
- **Experiment:** EXP-001 (SWE-Verified + Multi-SWE-bench + Commit0 slice; H∈{raw,generic,eidos-ablations} × M∈{standard,frontier} × complexity bins; T=0/seed-locked; `evaluation_run.json`).
- **Metrics:** VSR, RR, TE, CS, TTI, $/task, human interventions. **Decision:** VALIDATE/RESTRICT/REJECT H1 per bin.

## GAP-002 — Graph granularity + k-bound + order policy
- **Problem:** Line vs entity vs CPG nodes; k≤2 vs k=3; order-preserved vs score-sorted chunks — no head-to-head on one harness.
- **Current:** EVD-005 (line +32.8%), CodexGraph entity, CPG 43% open Lite, OP-RAG order. **Missing:** shared-harness comparison + token/latency costs.
- **Experiment:** EXP-002. **Metrics:** VSR, localization acc, tokens, build time, p95. **Decision:** lock default granularity + document when to escalate.

## GAP-003 — Contract-subagent vs singleton vs orchestrator-workers on code
- **Problem:** EVD-004 transfer is non-code; cost 15× unknown for SWE.
- **Current:** SRC-102, SRC-100/101, EVD-003. **Missing:** code ablation with effort-scaling + parallelism sweep.
- **Experiment:** EXP-002 arm B. **Metrics:** VSR, tokens, time, TTI. **Decision:** default delegation policy + parallelism cap.

## GAP-004 — SDD spec efficacy
- **Problem:** Does machine-checked spec-before-code move VSR/RR, and at what ceremony cost?
- **Current:** EVD-010/011/012. **Missing:** spec-vs-no-spec (+micro-spec fast-path) ablation.
- **Experiment:** EXP-003. **Metrics:** VSR, RR, spec-drift rate, authoring time, RSK-07 friction. **Decision:** mandatory vs fast-path vs advisory specs.

## GAP-005 — Skill gate calibration + sandbox pen-test
- **Problem:** risk<25 uncalibrated; flag base-rates collapse with context (99.5%); sandbox overhead/escape unknown.
- **Current:** EVD-007/008, SRC-108 T1-T3. **Missing:** precision/recall on labeled skill corpus + repo-aware scan; Landlock/seccomp pen-test + overhead.
- **Experiment:** EXP-005. **Metrics:** precision/recall, install latency, escape rate, policy-breakage. **Decision:** lock threshold + mandatory vs advisory gates.

## GAP-006 — Repair bound K + stopping criteria + judge quality
- **Problem:** K=5 unjustified; semantic vs test stopping uncompared; judge-only loops may degrade.
- **Current:** EVD-009, SRC-303/304/302. **Missing:** K-sweep with best-so-far rollback + SHP/LoopGain comparison + human-vs-LLM judge.
- **Experiment:** EXP-004. **Metrics:** convergence, RR, tokens, false-stop rate. **Decision:** lock K + stopping rule per artifact type (testable vs prose).

## GAP-007 — Memory utility + contamination control
- **Problem:** Dialogue gains may not transfer; contamination cascade unmeasured for code.
- **Current:** EVD-017, SRC-029, SRC-107. **Missing:** memory on/off multi-session SWE ablation with ρ tracking + sanitization-utility trade-off.
- **Experiment:** EXP-005 arm M. **Metrics:** multi-session VSR, ρ, retrieval precision, approval burden. **Decision:** ship project-only/gated/full vs remove.

## GAP-008 — Adapter breakage + MCP/CLI overhead
- **Problem:** External harness drift (RSK-04) unquantified; MCP vs CLI cost unknown.
- **Current:** SRC-105 standard, OSS snapshots. **Missing:** breakage log + latency/overhead + headless-fairness check.
- **Experiment:** EXP-007 (longitudinal). **Metrics:** breakage events, dispatch latency, trace completeness. **Decision:** interface freeze + conformance suite.

## GAP-009 — Invariant synthesis precision + drift-threshold calibration
- **Problem:** LLM-inferred invariants may hallucinate; ΔQ<−0.05, doc-link completeness unvalidated.
- **Current:** EVD-012 function-scale only. **Missing:** precision/recall vs ground truth on 10 OSS repos + drift-threshold ROC.
- **Experiment:** EXP-006 arm I. **Metrics:** precision/recall, false-block rate, ΔQ ROC, DOC/SPEC/ARCH/CONTRACT-drift accuracy. **Decision:** advisory vs blocking per invariant class.

## GAP-010 — Controlled improvement (GEPA) vs open-ended evolution (DGM)
- **Problem:** Promise (GEPA +6pp @35× fewer; DGM 20%→50%) vs oversight requirement unresolved for Eidos.
- **Current:** EVD-018. **Missing:** GEPA-on-Eidos-pipeline demo; sandboxed DGM-style eval with human veto measurement.
- **Experiment:** EXP-006 arm E. **Metrics:** ΔVSR per rollout, veto rate, escape attempts, cost. **Decision:** allow GEPA-bounded optimization; keep evolution gated/off by default.

## Over-design triage (Evidence-backed / Experimental / Speculative)

- **Evidence-backed (ship):** phased pipeline, k≤2 graph router + MSC, CodeAct exec, oracle-gated repair, event log, Python-core hybrid.
- **Experimental (ship gated + EXP):** contract subagents, skill gate + sandbox, tripartite project memory, GEPA tuning, invariants advisory.
- **Speculative (do not ship as default):** institutional cross-project memory, open-ended self-evolution, blocking auto-inferred invariants, Loop Engineering as scientific claim, C_threshold as fact.
