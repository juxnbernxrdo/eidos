# Formal Hypotheses & Epistemic Decision Criteria

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** System Constitution & Research Agenda (`GAP-001` through `GAP-010`)  
**Status:** ACTIVE RESEARCH HYPOTHESES  

---

## 1. Foundational Research Hypotheses

### Primary Alternative Hypothesis ($H_1$)
> **$H_1$ — An engineering harness properly designed can measurably improve software engineering task outcomes performed by AI agents compared to equivalent configurations without said harness, holding constant, to the maximum extent experimentally possible, the underlying model and available resources.**

### Null Hypothesis ($H_0$)
> **$H_0$ — The incorporation of the engineering intelligence harness does not produce a statistically or practically significant improvement in software engineering task outcomes evaluated under defined experimental conditions.**

---

## 2. Granular Sub-Hypotheses

To dissect the specific causal mechanisms of Eidos, $H_1$ is decomposed into six testable sub-hypotheses:

| Sub-Hypothesis ID | Dimension | Formal Statement | Targeted Metric | Acceptance Threshold |
|:---|:---|:---|:---|:---:|
| **$H_{1.1}$** | **Task Effectiveness** | Eidos full stack ($B_2$) achieves a significantly higher Task Success Rate (VSR) than an unconstrained agent ($B_0$) on SWE tasks. | Task Success Rate (VSR) | $\Delta VSR \ge +30.0$ pp, $p < 0.05$ |
| **$H_{1.2}$** | **Regression Prevention** | Automated oracle verification gating eliminates false confidence and reduces unintended regressions. | Mean Regressions / Trial | $\Delta \text{Regressions} \le -50.0\%$ |
| **$H_{1.3}$** | **Context Token Efficiency** | Heterogeneous graph topological pruning ($k \le 2$) achieves lower token consumption than full file dumping without harming task localization. | Mean Total Tokens | $\Delta \text{Tokens} \le -40.0\%$, Cohen's $d \le -0.8$ |
| **$H_{1.4}$** | **Repair Loop Convergence** | Oracle-guided bounded repair ($K \le 5$) converges on $\ge 80\%$ of repairable failures within $k \le 3$ iterations. | Repair Convergence Rate | $\ge 80.0\%$ resolved in $k \le 3$ |
| **$H_{1.5}$** | **Security Confinement** | Physical path confinement (`os.path.realpath`) and default-deny policies prevent all directory traversal and path escape attempts. | Security Invariant Escape Rate | Exact $0.0\%$ Escape Rate |
| **$H_{1.6}$** | **Component Super-Additivity** | Full Eidos ($A_9$) achieves higher VSR at lower cost than the simple linear sum of isolated ablations ($A_1$ through $A_8$). | Synergy Index | $VSR(A_9) > \max_i(VSR(A_i))$ with $\text{Cost}(A_9) < \text{Cost}(A_7)$ |

---

## 3. Epistemic Decision Framework

At the conclusion of Phase 7, each hypothesis will be adjudicated strictly using standardized epistemic statuses:

- **`SUPPORTED`**: Statistical significance ($p < 0.05$), practical significance (Cohen's $d \ge 0.5$ or relative change $\ge 25\%$), and reproducible across repeated trials without conflicting evidence.
- **`PARTIALLY_SUPPORTED`**: The hypothesis holds for a subset of conditions (e.g. effective on SMALL/MEDIUM tasks, but inconclusive on LARGE/SYSTEM tasks), or exhibits trade-offs (e.g. higher VSR but increased latency).
- **`NOT_SUPPORTED`**: No statistically significant difference ($p \ge 0.05$) or observed degradation compared to baseline.
- **`INCONCLUSIVE`**: High statistical variance, insufficient trial power, or uncontrolled confounders prevent definitive determination.

**Prohibited Vocabulary:**
Under no circumstances will a hypothesis be labeled `PROVEN`, `DISPROVEN`, `GUARANTEED`, or `UNIVERSALLY_TRUE`. All empirical knowledge is bounded by the experimental domain evaluated.
