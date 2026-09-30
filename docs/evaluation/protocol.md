# Phase 7 Execution Protocol Specification

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** Standardized Experimental Operating Procedure (SOP)  
**Status:** BINDING SOP  

---

## 1. Step-by-Step Trial Execution Protocol

Each individual trial of a benchmark task under any experimental arm must execute through a standardized, immutable 7-step sequence:

```text
┌────────────────────────────────────────────────────────┐
│ Step 1: Pre-Trial Environment Sanitization             │
├────────────────────────────────────────────────────────┤
│ Step 2: Ephemeral Workspace Generation                │
├────────────────────────────────────────────────────────┤
│ Step 3: Seed Locking & Execution Queue Shuffling       │
├────────────────────────────────────────────────────────┤
│ Step 4: Experimental Arm Dispatch (Subject Run)        │
├────────────────────────────────────────────────────────┤
│ Step 5: Multi-Tier Double-Blind Oracle Evaluation      │
├────────────────────────────────────────────────────────┤
│ Step 6: Telemetry & Economic Cost Accounting          │
├────────────────────────────────────────────────────────┤
│ Step 7: Immutable JSON Run Artifact Persistence        │
└────────────────────────────────────────────────────────┘
```

---

## 2. Granular Protocol Specification

### Step 1: Pre-Trial Environment Sanitization
- Clear all temporary caches, `.pytest_cache`, and residual `.pyc` files.
- Verify Git working tree status.
- Scrub environment variables to prevent host token leakage.

### Step 2: Ephemeral Workspace Generation
- Create an isolated directory structure (`tmp_path`).
- Populate the workspace with `task.initial_files`.
- Verify file hashes match ground-truth initialization vectors.

### Step 3: Seed Locking & Queue Shuffling
- Generate trial-specific pseudo-random seed: $s_i = \text{seed}_{\text{base}} + i \times 17$.
- Populate the execution queue $(Task_j, Arm_k, Seed_i)$ and permute via Fisher-Yates shuffle to eliminate systematic order bias.

### Step 4: Experimental Arm Dispatch
- Execute the designated arm ($B_0$, $B_1$, $B_2$, or $A_0$..$A_9$) within the workspace.
- Enforce token ceilings ($8,000$ tokens) and execution timeouts ($60$s).
- Record raw tool calls, stdio streams, prompt tokens, and completion tokens.

### Step 5: Multi-Tier Double-Blind Oracle Evaluation
- **Tier 1 (Public Oracles)**: Execute `task.public_tests`. Record `public_tests_passed`.
- **Tier 2 (Hidden Oracles)**: Execute held-out `task.hidden_tests`. Record `hidden_tests_passed`.
- **Tier 3 (Invariants)**: Audit structural imports via AST and run security supervisor checks. Record `invariant_passed`.
- **Composite Outcome**: Set `success = Tier1 and Tier2 and Tier3`.

### Step 6: Telemetry & Economic Cost Accounting
- Compute regression count against existing tests.
- Record elapsed wall-clock latency (ms).
- Calculate financial cost in USD using standardized pricing ($3.00 / 1M prompt, $15.00 / 1M completion).

### Step 7: Immutable Run Artifact Persistence
- Package all trial results into an `EvaluationRun` data structure.
- Compute parametric and non-parametric summary statistics, 95% confidence intervals, Cohen's d effect sizes, and permutation test p-values.
- Write JSON artifact to `.eidos/evaluation/runs/{run_id}.json`.
