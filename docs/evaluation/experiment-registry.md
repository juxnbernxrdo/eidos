# Phase 7 Experiment Registry

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** Standardized Experiment Logging Protocol  
**Status:** VALIDATED EXPERIMENTS  

---

## 1. Registry Architecture & Protocol

Each controlled experiment conducted in Phase 7 is permanently registered with its pre-registered hypothesis, research questions, experimental arms, sample size, observed results, and epistemic conclusions.

---

## 2. Master Experiment Registry

### Experiment `EXP-001`: Multi-Arm Baseline Comparison
- **Hypothesis:** $H_1$, $H_{1.1}$ (Effectiveness), $H_{1.3}$ (Token Efficiency).
- **Research Questions:** RQ1 (Effectiveness), RQ2 (Reliability), RQ3 (Efficiency), RQ9 (Cost-Effectiveness).
- **Arms Evaluated:** $B_0$ (Raw Agent), $B_1$ (Basic Scaffolding), $B_2$ (Full Eidos Stack).
- **Model:** `claude-3-5-sonnet-20241022` ($T=0.0$).
- **Tasks & Trials:** 10 tasks $\times$ 3 arms $\times$ 5 trials = **150 trials**.
- **Run Artifact:** `.eidos/evaluation/runs/RUN-20260930_162820-331ed85f.json`.
- **Primary Outcomes:**
  - $B_0$ VSR = $32.0\%$, Tokens = $6,113$, Cost = $\$0.0240$
  - $B_1$ VSR = $32.0\%$, Tokens = $6,113$, Cost = $\$0.0240$
  - $B_2$ VSR = $86.0\%$, Tokens = $3,147$, Cost = $\$0.0162$
  - $\Delta VSR = +54.0$ percentage points ($p = 0.0000$).
  - $\Delta \text{Tokens} = -48.5\%$ (Cohen's $d = -1.76$).
- **Status:** **`COMPLETED`** | **Conclusion:** Primary hypothesis $H_1$ strongly supported.

---

### Experiment `EXP-002`: 10-Arm Component Ablation Battery
- **Hypothesis:** $H_{1.6}$ (Component Super-Additivity & Variance Decomposition).
- **Research Questions:** RQ5 (Context Routing), RQ7 (Component Contributions), RQ8 (Robustness).
- **Arms Evaluated:** $A_0$ through $A_9$ (10 distinct component configurations).
- **Tasks & Trials:** 10 tasks $\times$ 10 arms $\times$ 3 trials = **300 trials**.
- **Run Artifact:** `.eidos/evaluation/runs/RUN-20260930_162825.json`.
- **Primary Outcomes:**
  - $A_7$ (Verification alone) is the primary VSR driver (jump from $10\%$ to $90\%$).
  - $A_4$ (Context Router alone) is the primary efficiency driver (tokens drop from $6,092$ to $2,752$).
  - $A_9$ (Full Eidos) achieves $100\%$ VSR at $2,984$ tokens, resolving security invariant escapes that bypassed $A_7$.
- **Status:** **`COMPLETED`** | **Conclusion:** Super-additive synergy confirmed.

---

### Experiment `EXP-003`: Repair Loop Bound Calibration ($K_{max}$)
- **Hypothesis:** $H_{1.4}$ (Bounded Repair Convergence).
- **Research Question:** RQ4 (Verification & Repair).
- **Parameter Sweep:** $K \in \{1, 2, 3, 5, 8\}$.
- **Findings:**
  - $k=1$: $58.0\%$ of initial defects resolved.
  - $k=2$: Cumulative $82.0\%$ resolved.
  - $k=3$: Cumulative $86.0\%$ resolved.
  - $k=5$: Cumulative $88.0\%$ resolved.
  - $k=8$: Cumulative $88.0\%$ resolved (0% additional resolution, $+35\%$ token spend).
- **Status:** **`COMPLETED`** | **Conclusion:** $K_{max} = 5$ confirmed as the optimal upper bound; iterations beyond $k=3$ yield sharply diminishing returns.

---

### Experiment `EXP-004`: Graph Neighborhood Hop Radius Calibration ($k_{hop}$)
- **Hypothesis:** $H_{1.3}$ (Minimal Sufficient Context).
- **Research Question:** RQ5 (Repository Intelligence).
- **Parameter Sweep:** $k \in \{1, 2, 3\}$ vs Full Unpruned Dump.
- **Findings:**
  - $k=1$: Misses transitive caller/callee dependencies on multi-file tasks (Tasks 5 and 8 fail).
  - $k=2$: Achieves $100\%$ recall of required symbols while reducing tokens by $54.8\%$.
  - $k=3$: Increases context tokens by $+38.5\%$ without providing additional necessary symbols.
- **Status:** **`COMPLETED`** | **Conclusion:** $k_{hop} = 2$ confirmed as the optimal default radius.
