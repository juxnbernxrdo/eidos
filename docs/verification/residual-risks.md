# Phase 6 Residual Risks & Empirical Calibration Register

**Authority:** Eidos Verification Protocol  
**Scope:** Open Experimental Parameters, Architectural Trade-offs, and Calibration Directives for Phase 7  
**Status:** CATALOGUED FOR PHASE 7 EVALUATION  
**Last Updated:** 2026-09-30  

---

## 1. Operating Axiom on Residual Risks

> **"Verification proves that the code functions according to its written specifications. It does not prove that the numerical thresholds chosen in the design are statistically optimal for real-world software engineering."**

Phase 6 certifies that all hard constraints and safety bounds are functional. However, several heuristic thresholds and architectural parameters are designed as **tunable experimental variables** to be evaluated empirically in Phase 7.

---

## 2. Open Empirical Calibration Matrix

| Parameter / Heuristic | Current Baseline | Epistemic Status | Phase 7 Empirical Research Question | Calibration Benchmark |
|:---|:---:|:---:|:---|:---|
| **Max Repair Iterations ($K_{max}$)** | `5` | `DESIGN_DECISION` | Does $K=5$ maximize Verification Success Rate ($\Delta VSR$), or does performance plateau at $K=3$ with lower token spend? | SWE-bench Lite repair trajectories |
| **Risk Scoring Threshold** | `score < 25` | `HYPOTHESIS` | Does a threshold of 25 accurately filter high-risk modifications without causing excessive false-positive escalations? | Synthetic defect injection suite |
| **Graph Traversal Radius ($k_{hop}$)** | `2` | `DESIGN_DECISION` | Does expanding the neighborhood to $k=3$ capture necessary transitive call dependencies, or does it saturate the token budget with irrelevant context? | AST Dependency Coverage Analysis |
| **Token Budget Baseline** | `4,000` tokens | `DESIGN_DECISION` | What is the Pareto frontier between Minimal Sufficient Context size and subagent task completion accuracy? | Multi-file refactoring experiments |
| **Context Pruning Decay** | Topological BFS | `DESIGN_DECISION` | How does topological distance decay compare against hybrid semantic-topological reranking? | Long-horizon context retrieval tests |
| **OS-Level Process Isolation** | Python `subprocess` | `DESIGN_DECISION` | For untrusted adversarial tasks, should userspace sandboxing be backed by Linux cgroups / bubblewrap / Docker? | Adversarial breakout challenge |

---

## 3. Epistemic Demarcation for Phase 7

1. **Deterministic vs Stochastic Layers**:
   - The State Machine, Event Log, Verification Runner, Invariant Checker, and Graph Engine are **100% deterministic** and verified.
   - The LLM generation layer (Subagents, Prompts) is **stochastic**. Phase 7 must measure distribution variance across multiple seeds and model families (e.g. Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro).
2. **False Confidence Risk**:
   - Verification tests prove that the verifier detects failing exit codes and test output traces.
   - Phase 7 must evaluate whether agents can game verification tests (e.g. creating trivial or vacuous assertions).

---

## 4. Handoff Safeguards

No parameter listed in Section 2 may be adjusted in production without recording an Empirical Evaluation Report in Phase 7.
