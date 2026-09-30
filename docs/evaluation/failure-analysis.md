# Phase 7 Failure Mode & Root Cause Analysis

**Authority:** Phase 7 Experimental Evaluation Program  
**Evaluation Standard:** Systematic Defect Classification & Trace Audit  
**Status:** VALIDATED FAILURE AUDIT  

---

## 1. Failure Taxonomy & Classification

Every non-successful trial in the evaluation battery was audited and classified into a standardized failure taxonomy:

| Failure Code | Category | Definition & Mechanism | Representative Example |
|:---|:---|:---|:---|
| **`MODEL_FAILURE`** | Core Reasoning | LLM emits logically flawed code that fails basic public assertions on first attempt and cannot self-correct without oracles. | Off-by-one error returning `IndexError` on Task 1. |
| **`FALSE_CONFIDENCE_EDGE_CASE`** | Generalization Gap | Agent satisfies public tests and claims completion, but held-out oracles detect broken edge cases or regressions. | Handled standard JSON in Task 2, but crashed on future timestamps or empty arrays. |
| **`SECURITY_INVARIANT_VIOLATION`** | Policy-as-Physics | Code achieves functional correctness but violates system security constraints or architectural boundaries. | File reader in Task 4 reads files, but allows `../../` path escapes outside root. |
| **`CONTRACT_VIOLATION`** | Schema Mismatch | Function parameters or return types deviate from Draft 2020-12 contract schemas. | Emitter in Task 5 emits `agent_id` instead of renamed `actor_id`. |
| **`VERIFICATION_EXHAUSTION`** | Repair Failure | Agent fails verification and exhausts all $K=5$ repair iterations without reaching convergence, forcing escalation. | Repeatedly misinterpreting mock timing in Task 7. |

---

## 2. Failure Distribution Across Experimental Arms

```text
Failure Distribution Matrix across Baseline and Ablation Trials:
──────────────────────────────────────────────────────────────────────────────────────────
Arm                  MODEL_FAILURE   FALSE_CONFIDENCE   SECURITY_VIOLATION   EXHAUSTED   TOTAL
──────────────────────────────────────────────────────────────────────────────────────────
B0_RAW_AGENT              20                12                  2                0        34
B1_BASIC_HARNESS          20                12                  2                0        34
B2_FULL_EIDOS              0                 0                  0                7         7
A0_BASELINE               15                 9                  3                0        27
A1_PLUS_SPECS             12                 5                  3                0        20
A2_PLUS_CONTRACTS         14                 3                  3                0        20
A3_PLUS_GRAPH             16                 8                  3                0        27
A4_PLUS_CONTEXT_ROUTER    16                 8                  3                0        27
A5_PLUS_SKILLS            18                 9                  0                0        27
A6_PLUS_SUBAGENTS         15                 9                  3                0        27
A7_PLUS_VERIFICATION       0                 0                  3                0         3
A8_PLUS_MEMORY            15                 9                  3                0        27
A9_FULL_EIDOS              0                 0                  0                0         0
──────────────────────────────────────────────────────────────────────────────────────────
```

---

## 3. Deep Dive: The False Confidence Phenomenon

A major empirical finding in Phase 7 is the **massive false confidence gap** in unassisted agents:
- In Baseline $B_0$, the agent achieved a **60.0% Public Pass Rate**, but only a **36.0% Hidden Pass Rate**, resulting in an overall VSR of **32.0%**.
- **Root Cause**: Without double-blind oracles or structured specifications, agents overfit to the explicit examples in the user prompt, writing brittle code that breaks when exposed to empty inputs, boundary indices, or malformed data.
- **Eidos Resolution**: In $B_2$, automated verification gating forces the agent through iterative test feedback, raising the hidden pass rate to **86.0%–100.0%**.

---

## 4. Deep Dive: Security Traversal Bypass in Isolated Verification (`A7`)

In ablation arm `A7` (Verification without Security Supervisor):
- VSR jumped to **90.0%**, but `A7` failed on Task 4 (Path Traversal) and Task 10 (Passport Gating).
- **Observation**: Unit tests alone passed because the LLM generated working reading code, but failed to sanitize paths using canonical `os.path.realpath`, leaving the application vulnerable to traversal attacks.
- **Architectural Lesson**: **Verification alone is insufficient for security**. Hard Policy-as-Physics security supervisors ([`src/eidos/security/permissions.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/security/permissions.py)) are essential to prevent agents from introducing insecure solutions that pass functional tests.
