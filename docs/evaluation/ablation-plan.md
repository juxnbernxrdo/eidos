# Component Ablation Study Plan (A0 – A9)

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** Factorial Component Sensitivity Analysis  
**Status:** VALIDATED ABLATION PROTOCOL  

---

## 1. Motivation & Scientific Objective

Comparing only $B_0$ vs $B_2$ can confirm whether the entire system produces an effect, but cannot determine **which specific subsystems are responsible** for the outcome.

To eliminate "monolithic credit assignment" and test for architectural bloat, Phase 7 executes a **10-Arm Component Ablation Battery** ($A_0$ through $A_9$):

```text
A0: Baseline (Unassisted)
 ├── A1: + Specifications (Given/When/Then Acceptance Criteria)
 ├── A2: + Contracts (Draft 2020-12 Pydantic Data Schemas)
 ├── A3: + Graph Engine (Heterogeneous AST Dependency Graph)
 ├── A4: + Context Router (Topological Pruning & Token Budgeting)
 ├── A5: + Skills & Sandbox (Lockfile Pinning & Realpath Confinement)
 ├── A6: + Subagents (Fresh Context Star Topology)
 ├── A7: + Verification Gating (Automated Oracles & Bounded Repair K<=5)
 ├── A8: + Gated Memory (Opt-in Project Memory)
 └── A9: Full Eidos Stack (Super-additive Integration)
```

---

## 2. Formal Ablation Arm Definitions

| Arm ID | Architectural Treatment Added to Baseline | Subsystems Engaged | Primary Target Metric | Expected Mechanism |
|:---:|:---|:---|:---:|:---|
| **`A0`** | **None** (Raw Baseline) | Direct model prompt | Baseline | Unassisted performance floor |
| **`A1`** | **+ Formal Specifications** | Given/When/Then ACs | VSR, Generalization | Clarifies edge cases and expected failure states |
| **`A2`** | **+ Formal Contracts** | Schema models & type checking | Contract Violations | Enforces input/output interface types |
| **`A3`** | **+ Repository Graph** | AST dependency indexing ($k \le 2$) | Context Precision | Captures multi-file dependencies |
| **`A4`** | **+ Context Router (MSC)** | Topological pruning + budget | Token Consumption | Slashes prompt tokens by eliminating irrelevant files |
| **`A5`** | **+ Skills & Sandbox** | Security supervisor & realpath | Security Invariants | Blocks path escapes and malicious injections |
| **`A6`** | **+ Task-Bounded Subagents** | Fresh context (0 prior turns) | Turn Degradation | Prevents attention dilution over multi-step workflows |
| **`A7`** | **+ Verification Gating** | Oracle runner + repair ($K \le 5$) | Task Success (VSR) | Detects failures and guides iterative repair |
| **`A8`** | **+ Project Memory** | Project-isolated memory | Repetitive Tasks | Recalls previous fix patterns |
| **`A9`** | **Full Eidos Integration** | All subsystems active | System VSR & Net Cost | Synergistic integration of all controls |

---

## 3. Factorial Interaction Analysis

The ablation protocol tests for non-linear component interactions:

### Interaction 1: Graph Engine $\times$ Context Router
$$\text{Tokens}(A_4) \ll \text{Tokens}(A_3) < \text{Tokens}(A_0)$$
- Hypothesis: A raw graph without pruning ($A_3$) reduces tokens moderately by providing structure, but the combination of graph topology + pruning + boundary pinning in the Context Router ($A_4$) yields non-linear token compression ($\ge 50\%$).

### Interaction 2: Specifications $\times$ Verification Gating
$$VSR(A_9) > VSR(A_7) > VSR(A_1) > VSR(A_0)$$
- Hypothesis: Specifications ($A_1$) inform the agent of requirements, but without verification ($A_7$), agents still hallucinate or introduce edge-case defects. Verification ($A_7$) catches errors, but without specifications, repairs may thrash. In combination ($A_9$), repair iterations converge rapidly with minimal token waste.
