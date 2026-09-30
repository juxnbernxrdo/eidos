# Phase 7 Evaluation Handoff Specification

**Document ID:** `EIDOS-HANDOFF-PHASE-6-TO-7`  
**From:** Phase 6 (Verification)  
**To:** Phase 7 (Evaluation)  
**Status:** READY FOR EVALUATION INITIALIZATION  
**Date:** 2026-09-30  

---

## 1. Scope & Objective of Handoff

Phase 6 has established that Eidos is **VERIFIED**: every line of code, contract, specification, and invariant functions deterministically according to its written requirements.

Phase 7 (**Evaluation**) is tasked with answering the scientific research question:
> **"Does Eidos's deterministic, contract-bounded, graph-routed architecture achieve statistically superior task convergence ($\Delta VSR$), reduced token waste, and lower regression rates compared to baseline unconstrained agentic systems?"**

---

## 2. Inventory of Handed-Over Capabilities

The following 15 verified capabilities are delivered to Phase 7 with 100% test coverage and Feature Passports:

1. **Deterministic Core State Machine (`SPEC-001`)**: Pure fold $S_t = \text{Fold}(S_0, [e_1 \dots e_t])$ with event replay.
2. **Deterministic Orchestration Pipeline (`SPEC-002`)**: Non-bypassable verification gating and bounded repair loop ($K_{max} = 5$).
3. **Formal Task Management (`SPEC-003`)**: Strongly typed task lifecycle states and dependency tracking.
4. **Context Router (`SPEC-004`)**: Minimal Sufficient Context assembly with topological pruning and boundary pinning.
5. **Heterogeneous Graph Engine (`SPEC-005`)**: 21 node types, 11 edge relations, and epistemic precedence (`EXTRACTED` > `INFERRED`).
6. **Unified Verification Runner (`SPEC-006`)**: Oracle diagnostic trace capture and automated failure localization.
7. **Append-Only Event Log (`SPEC-007`)**: POSIX-locked JSONL event stream anchored to Git HEAD commit.
8. **Security Sandbox Supervisor (`SPEC-008`)**: Policy-as-Physics default-deny, realpath confinement, and multi-provider secret scrubbing.
9. **Host Harness Abstraction (`SPEC-009`)**: Headless execution adapter with complete trace collection and zero host leaks.
10. **Contract-Bounded Subagents (`SPEC-010`)**: Star topology subagents with guaranteed fresh context (0 prior turns) and CodeAct execution.
11. **Gated Memory Infrastructure (`SPEC-011`)**: Default-disabled opt-in memory with strict project isolation.
12. **Skill Gateway (`SPEC-012`)**: SHA-256 lockfile pinning and malicious pattern filtering.
13. **Feature Passports (`SPEC-013`)**: 12-dimensional continuous traceability bridges across all 15 features.
14. **Human-in-the-Loop Evolution Pipeline (`SPEC-014`)**: Cryptographically gated architecture mutation proposals.
15. **Objective Observability Projector (`SPEC-015`)**: Evidence-gated progress metrics and deterministic token cost accounting.

---

## 3. Recommended Phase 7 Experimental Protocols

### Experiment 1: Verification Success Rate ($\Delta VSR$) & Convergence Efficiency
- **Objective**: Measure task completion and verification convergence on SWE-bench Lite tasks.
- **Control Group**: Baseline unconstrained CodeAct / ReAct agent without Eidos context routing or bounded repair.
- **Treatment Group**: Eidos full stack with Context Router and Verification Gated Repair.
- **Metrics**: Pass@1, Pass@$K$, Total Tokens Consumed, Total Execution Wall-clock Time.

### Experiment 2: Repair Loop Parameter Calibration ($K_{max}$)
- **Objective**: Calibrate $K_{max} \in \{1, 2, 3, 5, 7\}$ to identify the point of diminishing returns in repair iteration.
- **Hypothesis**: Repairs beyond $k=3$ yield marginal $\Delta VSR$ increases (<5%) while increasing cost exponentially.

### Experiment 3: Context Window Efficiency (Minimal Sufficient Context vs Full Prompting)
- **Objective**: Measure token consumption and attention degradation when feeding full repository context vs topological graph pruning ($k \le 2$).
- **Metrics**: Token reduction percentage, hallucination rate, context retrieval precision/recall.

### Experiment 4: Multi-Model Portability & Invariance
- **Objective**: Execute Eidos across diverse LLM backends:
  - Claude 3.5 Sonnet
  - GPT-4o
  - Gemini 1.5 Pro
- **Evaluation**: Verify that Eidos state transitions and security boundaries remain invariant to model differences.

---

## 4. Governance Constraints for Phase 7

1. Phase 7 **must not modify** contracts or specifications.
2. Phase 7 findings must be labeled using epistemic tags: `OBSERVATION`, `EXPERIMENTAL_RESULT`, `INTERPRETATION`, or `VALIDATED_RESULT`.
3. If an experiment reveals poor empirical performance for a parameter (e.g. $K=5$), the proposal to adjust it must be submitted through the Phase 8 Evolution Pipeline (`SPEC-014`).

---

## 5. Phase 7 Readiness Declaration

Phase 6 Verification is complete. The system is structurally sound, deterministically repeatable, and ready for empirical scientific evaluation.
