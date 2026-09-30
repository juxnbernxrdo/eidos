# Phase 7 Research Questions (RQ1 – RQ10)

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** System Architecture & Research Agenda  
**Status:** CANONICAL RESEARCH QUESTIONS  

---

## 1. Overview of Research Inquiry

The empirical evaluation of Eidos is structured around 10 primary Research Questions designed to provide a comprehensive, multi-dimensional assessment of engineering intelligence harnesses:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ RQ1: Effectiveness        ──► Does Eidos improve task success?         │
│ RQ2: Reliability          ──► Does Eidos eliminate regressions/escapes?│
│ RQ3: Efficiency           ──► What is the impact on tokens and latency?│
│ RQ4: Verification Gating  ──► How effective is oracle-guided repair?   │
│ RQ5: Context Routing      ──► What does graph MSC contribute vs dump?  │
│ RQ6: Agent Orchestration  ──► Do task-bounded agents outperform solos? │
│ RQ7: Component Hierarchy  ──► Which components matter most (Ablation)? │
│ RQ8: Robustness           ──► Do benefits hold across task categories? │
│ RQ9: Cost-Effectiveness   ──► Does value exceed engineering overhead?  │
│ RQ10: Failure Modes       ──► Where does Eidos fail or degrade?        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Formulation of Research Questions

### RQ1 — Effectiveness
> **Question:** Does Eidos measurably improve the resolution of software engineering tasks performed by AI agents compared to an equivalent baseline configuration holding the underlying model and toolset constant?  
> **Target Metric:** Task Success Rate / Verification Success Rate (VSR).  
> **Evaluation Method:** Multi-trial comparison between $B_0$ (Raw Agent), $B_1$ (Basic Harness), and $B_2$ (Full Eidos).

### RQ2 — Reliability
> **Question:** Does Eidos reduce semantic errors, regressions in previously working code, contract violations, and verification escapes?  
> **Target Metric:** Regression Rate, Contract Violation Rate, Hidden Test Pass Rate.  
> **Evaluation Method:** Differential test execution on held-out regression oracles.

### RQ3 — Efficiency
> **Question:** What effect does Eidos have on execution time, token consumption, number of iterations, tool calls, and financial cost per resolved task?  
> **Target Metric:** Mean Total Tokens, Mean Latency (ms), Mean Cost ($/task), Cost per Resolved Task.  
> **Evaluation Method:** Token accounting across prompt, completion, and repair cycles.

### RQ4 — Verification & Bounded Repair
> **Question:** Does the automated verification runner and bounded repair loop ($K \le 5$) improve the agent's ability to detect and repair errors prior to declaring task completion?  
> **Target Metric:** Repair Convergence Rate, Iterations-to-Convergence, False-Positive Completion Rate.  
> **Evaluation Method:** Tracking initial test failures, subsequent repair passes, and stopping boundary at $K=5$.

### RQ5 — Context Routing & Repository Intelligence
> **Question:** Does topological graph pruning ($k \le 2$) and boundary pinning in the Context Router improve task resolution while reducing token bloat compared to unpruned context dumping?  
> **Target Metric:** Context Token Size, Information Retention Rate, Task Success under Tight Budgets.  
> **Evaluation Method:** Head-to-head ablation comparing $A_0$ (Unpruned) vs $A_3$ (Graph) vs $A_4$ (Context Router).

### RQ6 — Agent Orchestration
> **Question:** Do contract-bounded subagents with guaranteed fresh context (0 prior turns) produce measurable improvements in accuracy and state preservation compared to long-running singleton agents?  
> **Target Metric:** Cross-turn Context Contamination Rate, Multi-step Task Completion.  
> **Evaluation Method:** Head-to-head comparison of singleton vs subagent pipeline execution on multi-module tasks.

### RQ7 — Component Contributions (Ablation Hierarchy)
> **Question:** Which specific subsystems of the Eidos harness provide the largest observable contribution to task success and efficiency, and which have negligible or redundant effects?  
> **Target Metric:** Marginal $\Delta VSR$ and Marginal $\Delta \text{Tokens}$ across 10 ablation arms ($A_0$ through $A_9$).  
> **Evaluation Method:** Factorial ablation matrix isolating Specs, Contracts, Graph, Router, Skills, Subagents, Verification, and Memory.

### RQ8 — Robustness & Heterogeneity
> **Question:** Do the observed benefits of Eidos remain consistent across different task categories (Bug Fix, Feature, Refactoring, Security, Invariant Fix), code complexity bins (SMALL to SYSTEM), and model families?  
> **Target Metric:** Task-type VSR variance, Complexity bin degradation curve.  
> **Evaluation Method:** Stratified analysis across the 10 benchmark task types.

### RQ9 — Cost-Effectiveness
> **Question:** Does the performance gain achieved by Eidos justify the computational overhead, tool call latency, and metadata infrastructure costs?  
> **Target Metric:** Net Cost per Resolved Task ($/resolved_task = \text{Total Spend} / \text{Resolved Tasks}$).  
> **Evaluation Method:** Economic frontier analysis comparing $B_0$ vs $B_2$.

### RQ10 — Failure Modes & Boundary Limits
> **Question:** Under what conditions, task types, or constraints does Eidos fail to provide an advantage, introduce unnecessary overhead, or degrade execution?  
> **Target Metric:** Failure taxonomy distribution, High-overhead task identification.  
> **Evaluation Method:** Qualitative and quantitative failure mode analysis on all failing trials.
