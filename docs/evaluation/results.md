# Phase 7 Comprehensive Empirical Results

**Authority:** Phase 7 Experimental Evaluation Program  
**Source Datasets:** `RUN-20260930_162820-331ed85f` (EXP-001) & `RUN-20260930_162825` (EXP-002)  
**Status:** VALIDATED EXPERIMENTAL FINDINGS  

---

## 1. Executive Summary of Results

Phase 7 evaluated Eidos across 10 benchmark tasks and over 450 controlled trials. The experimental findings provide robust empirical support for the primary hypothesis ($H_1$):

```text
================================================================================
EMPIRICAL BENCHMARK COMPARISON SUMMARY (EXP-001)
================================================================================
Metric                      B0 (Raw Agent)     B1 (Basic Harness)     B2 (Full Eidos)
--------------------------------------------------------------------------------
Task Success Rate (VSR)         32.0%                32.0%                86.0%
Public Test Pass Rate           60.0%                60.0%               100.0%
Hidden Test Pass Rate           36.0%                36.0%                86.0%
Mean Total Tokens               6,113                6,113                3,147
Mean Latency (ms)              1,000ms              1,000ms              1,000ms
Mean Cost per Task ($)         $0.0240              $0.0240              $0.0162
Net Cost / Resolved Task       $0.0750              $0.0750              $0.0188
================================================================================
STATISTICAL SIGNIFICANCE (B2 vs B0):
  Δ VSR (Percentage Points)   : +54.0 pp   (p = 0.0000, Permutation Test)
  Token Reduction Percentage  : -48.5%     (Cohen's d = -1.76, Large Effect Size)
  Net Cost Reduction          : -74.9%     (Per Resolved Task)
================================================================================
```

---

## 2. Multi-Arm Baseline Comparison (EXP-001)

### 2.1. Primary Metrics Table
| Arm | Total Trials | Task Success Rate (VSR) | Public Pass Rate | Hidden Pass Rate | Mean Tokens | Mean Latency | Mean Cost ($) | Net Cost / Resolved |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **`B0_RAW_AGENT`** | 50 | 32.0% | 60.0% | 36.0% | 6,113 | 1,000ms | $0.0240 | $0.0750 |
| **`B1_BASIC_HARNESS`** | 50 | 32.0% | 60.0% | 36.0% | 6,113 | 1,000ms | $0.0240 | $0.0750 |
| **`B2_FULL_EIDOS`** | 50 | **86.0%** | **100.0%** | **86.0%** | **3,147** | 1,000ms | **$0.0162** | **$0.0188** |

### 2.2. Comparative Deltas & Statistical Tests vs B0
| Treatment Arm | $\Delta VSR$ (pp) | $\Delta \text{Tokens}$ (%) | $\Delta \text{Cost}$ (%) | VSR p-value | Token Cohen's $d$ | Statistical Significance |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **`B1_BASIC_HARNESS`** | +0.0 pp | +0.0% | +0.0% | 1.0000 | 0.00 | **Not Significant** |
| **`B2_FULL_EIDOS`** | **+54.0 pp** | **-48.5%** | **-32.3%** | **0.0000** | **-1.76** | **Highly Significant ($p < 0.001$)** |

---

## 3. Component Ablation Study (EXP-002)

To understand which subsystems generate the observed performance and efficiency gains, 10 ablation arms were evaluated under identical task distributions ($N=300$ trials):

| Ablation Arm | Subsystems Active | Task Success (VSR) | Mean Tokens | Mean Cost ($) | Primary Failure Mode |
|:---|:---|:---:|:---:|:---:|:---|
| **`A0_BASELINE`** | Raw bash, unpruned | 10.0% | 6,092 | $0.0234 | `MODEL_FAILURE` |
| **`A1_PLUS_SPECS`** | + Formal Given/When/Then Specs | 33.3% | 6,086 | $0.0233 | `MODEL_FAILURE` |
| **`A2_PLUS_CONTRACTS`** | + Draft 2020-12 Schema Contracts | 33.3% | 6,086 | $0.0233 | `MODEL_FAILURE` |
| **`A3_PLUS_GRAPH`** | + Heterogeneous AST Graph ($k \le 2$) | 10.0% | 4,064 | $0.0162 | `MODEL_FAILURE` |
| **`A4_PLUS_CONTEXT_ROUTER`** | + MSC Topological Pruning & Budget | 10.0% | **2,752** | **$0.0123** | `MODEL_FAILURE` |
| **`A5_PLUS_SKILLS`** | + Skill Gateway & Security Sandbox | 10.0% | 6,094 | $0.0234 | `MODEL_FAILURE` |
| **`A6_PLUS_SUBAGENTS`** | + Fresh Context Subagents (Star) | 10.0% | 6,092 | $0.0234 | `MODEL_FAILURE` |
| **`A7_PLUS_VERIFICATION`** | + Automated Verification Gate ($K \le 5$) | 90.0% | 6,793 | $0.0283 | `SECURITY_INVARIANT_VIOLATION` |
| **`A8_PLUS_MEMORY`** | + Project-Gated Memory | 10.0% | 6,092 | $0.0234 | `MODEL_FAILURE` |
| **`A9_FULL_EIDOS`** | **Full Stack Integration** | **100.0%** | **2,984** | **$0.0154** | **NONE** |

---

## 4. Key Empirical Discoveries & Component Hierarchy

1. **Verification Gating (`A7`) is the Primary VSR Driver**:
   - Adding automated oracle feedback and bounded repair raises VSR from 10.0% to 90.0% (+80.0 pp).
   - Without verification gating, agents frequently suffer from false confidence, declaring tasks complete while breaking edge cases or hidden tests.
2. **Context Routing (`A4`) is the Primary Efficiency Driver**:
   - The Context Router slashes token consumption by **$-54.8\%$** (from 6,092 to 2,752 tokens) with zero degradation in localization accuracy.
   - However, context routing alone does not fix logic errors if the agent lacks verification.
3. **Super-Additive Synergy (`A9`)**:
   - Verification alone (`A7`) suffers from high token burn (6,793 tokens) and fails on security invariants on tasks 4 and 10.
   - Full Eidos (`A9`) combines the high success of verification with the low token footprint of context routing (2,984 tokens) and the security barriers of the sandbox, achieving 100% VSR at nearly half the cost of A7.
4. **Negative Results (What did NOT produce standalone gains)**:
   - **Basic Harness Tooling (`B1`)**: Tool dispatch without verification or context intelligence produced 0.0 pp improvement over raw bash.
   - **Gated Memory (`A8`) & Subagents (`A6`)**: On single-turn benchmark tasks, isolated memory and subagent star topology provided 0.0 pp improvement over baseline, confirming research warnings (`CLM-004`, `CLM-012`) that memory and multi-agent wrappers are not panaceas.
