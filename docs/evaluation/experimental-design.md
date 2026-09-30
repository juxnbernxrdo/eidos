# Phase 7 Experimental Design

**Authority:** Phase 7 Experimental Evaluation Program  
**Methodological Basis:** Factorial Multi-Arm Design with Component Ablations  
**Status:** VALIDATED PROTOCOL  

---

## 1. Experimental Architecture

The evaluation is structured into two core experimental protocols:

1. **Protocol 1: Multi-Arm Baseline Comparison (EXP-001)**
   - Compares the unassisted agent against standard tooling and full Eidos.
   - Arms: $B_0$ (Raw Agent), $B_1$ (Basic Harness), $B_2$ (Full Eidos Stack).
   - Sample Size: 10 Tasks $\times$ 3 Arms $\times$ 5 Trials = **150 Trials**.
2. **Protocol 2: Component-Level Factorial Ablation Battery (EXP-002)**
   - Dissects the individual marginal contributions of each architectural module.
   - Arms: $A_0$ through $A_9$ (10 distinct component configurations).
   - Sample Size: 10 Tasks $\times$ 10 Arms $\times$ 3 Trials = **300 Trials**.

---

## 2. Experimental Variables

### 2.1. Independent Variables
- **Harness Architecture**:
  - Unassisted execution (Raw bash commands).
  - Scaffolding wrapper (Basic prompting and tool dispatch).
  - Component ablations (Specs, Contracts, Graph, Router, Skills, Subagents, Verification, Memory).
  - Complete Eidos Policy-as-Physics stack.
- **Task Difficulty**: SMALL, MEDIUM, LARGE, SYSTEM.
- **Task Category**: Bug Fix, Feature Implementation, Refactoring, Security Patch, Contract Repair, Architectural Invariant Fix, Test Repair, Cross-Module Integration, Performance Optimization, System Integration.

### 2.2. Dependent Variables (Outcome Metrics)
- **Primary Effectiveness**: Task Verification Success Rate (VSR — passing both public and held-out oracles).
- **Quality & Reliability**: Public Pass Rate, Hidden Pass Rate, Regression Count, Invariant Violation Count.
- **Resource Efficiency**: Total Tokens, Prompt Tokens, Completion Tokens, Context Size (Tokens), Wall-Clock Latency (ms), Tool Call Count, Financial Cost ($USD).
- **Process Dynamics**: Number of repair loop iterations ($k \in [0, 5]$), Failure classification mode.

### 2.3. Controlled Variables
To ensure fair comparison and isolate the harness as the causal agent:
- **Base Model**: Pinned model family and version (`claude-3-5-sonnet-20241022` / frontier equivalent).
- **Sampling Temperature**: Locked at $T = 0.0$ for deterministic greedy sampling.
- **Initial Repository State**: Exactly identical initial file tree and Git starting commit.
- **Prompt Instructions**: Identical problem description and requirements provided to all arms.
- **Environment**: Linux x86_64, Python 3.14.7 runtime, local process isolation.
- **Token Limits**: Pinned maximum token budgets per task.

---

## 3. Randomization & Bias Controls

To eliminate systematic order effects, warmup caching bias, and temporal server drifts:
1. **Execution Shuffling**: The sequence of $(Task, Arm, Seed)$ trial executions is randomly permuted via Fisher-Yates shuffle using a dedicated master random generator.
2. **Seed Locking**: Every trial is initialized with a distinct, recorded pseudo-random seed ($s_i = \text{base\_seed} + i \times 17$) guaranteeing 100% exact bit-for-bit replayability.
3. **Held-Out Testing (Double Blind Oracles)**: The agent has access only to public task specifications and tests during development. Held-out hidden tests and security invariants are evaluated post-execution to prevent test gaming and false confidence.
