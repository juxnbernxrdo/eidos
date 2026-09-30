# Verifier Contract (`VERIF-CONTRACT-001`)

**Contract ID:** `VERIF-CONTRACT-001`  
**Version:** 1.0.0  
**Status:** ACCEPTED  
**Owner Domain:** Verification  
**Machine Schema:** [`verifier.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/verification/verifier.schema.json)  
**Architecture Basis:** [P2-ADR-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-001-phased-verification-first-pipeline.md), [verification.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/verification.md), [EVD-009](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [EVD-012](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [EVD-015](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md)

---

## 1. Purpose & Verification-First Mandate

The `Verifier` contract defines the multi-layered verification protocol that determines whether code changes satisfy the definition of `DONE`.

### Foundational Principle (Constitution Art. IV & INV-003):
> **Agent completion claims are NOT evidence.** Verbal assertions like "I have completed the task" have zero evidential weight. Transition to `CONVERGED` occurs if and only if all active verification layers pass with machine-verifiable evidence.

---

## 2. Formal Verification & Repair Loop

The verification lifecycle enforces a bounded state machine:

```text
               ┌────────────────┐
               │   IMPLEMENT    │
               └───────┬────────┘
                       │ submit patch
               ┌───────▼────────┐
               │     VERIFY     │
               └───────┬────────┘
                       │
       ┌───────────────┴───────────────┐
       │ all layers pass               │ failure detected
┌──────▼────────┐               ┌──────▼────────┐
│  CONVERGED    │               │ attempts < K? │
│ (Passport Stamped)            └──────┬────────┴─┐
└───────────────┘                      │ yes      │ no (or unrepairable)
                               ┌───────▼────────┐ ┌──────▼────────┐
                               │     REPAIR     │ │   ESCALATE    │
                               │ (Oracle Trace) │ │(Human + Diff) │
                               └───────┬────────┘ └───────────────┘
                                       │ retry
                                       └──────────► (re-enter VERIFY)
```

### The Oracle Necessity Law (EVD-009):
Automated repair without an **external machine oracle** (compiler error, stack trace, unit test assertion failure, or static type diagnostic) is strictly prohibited. Unfocused "verbal self-reflection" without execution feedback degenerates into random sampling and burns tokens without convergence.

---

## 3. Seven Verification Layers

A candidate patch is evaluated against up to seven distinct machine-checkable layers:

| Layer | Verification Target | Oracle Type | Gate Condition |
|---|---|---|---|
| **1. Tests** | Unit, integration, and regression suites | Test runner stdout/stderr, exit codes | 0 failed, 0 errors |
| **2. Static Types** | `mypy`, `pyright`, `tsc` strict checks | Type checker diagnostics | 0 type errors |
| **3. Lint / Standards** | `ruff`, `eslint` style and safety rules | Linter rule violations | 0 violations |
| **4. Contracts** | JSON Schema validation across inputs/outputs | Schema validator output | 0 schema errors |
| **5. Invariants** | Architectural rules (`INV-001` .. `INV-006`) | Invariant checker AST analyzer | 0 blocking violations |
| **6. Security** | Skill Gateway and Sandbox Supervisor policy | Security policy audit log | 0 security breaches |
| **7. Drift** | `DOC-DRIFT`, `SPEC-DRIFT`, `ARCH-DRIFT`, `CONTRACT-DRIFT`| Drift detection engine diff | Drift within tolerance |

---

## 4. Failure Severity & Repair Eligibility

When a verification layer detects failures, each failure is assigned a severity:
- `CRITICAL`: Immediate blocking failure; requires human escalation if unrepairable.
- `HIGH`: Blocking failure; eligible for bounded repair if an external oracle trace is available.
- `MEDIUM`: Quality warning; must be remediated before final convergence.
- `LOW` / `INFO`: Advisory observation; does not block convergence.

### Repair Eligibility Evaluation:
In `verdict_payload.repair_eligibility`:
- `is_eligible`: `true` if and only if an explicit machine oracle trace is present and `attempt_index < K`.
- `reason`: Explanation of why repair was permitted or rejected.
- `external_oracle_trace`: The exact command, exit code, and captured stderr/stdout to be fed to the repair agent.

---

## 5. Escalation Payload

If `attempts >= K` or the failure is unrepairable:
- `verdict`: `ESCALATED`.
- `escalation_payload`:
  - `reason`: `ATTEMPTS_EXHAUSTED` | `UNREPAIRABLE_INVARIANT` | `SECURITY_BREACH` | `MANUAL_INTERVENTION_REQUESTED`.
  - `diagnostic_diff`: Complete diff of changes attempted during all repair cycles.
  - `failure_summary`: Human-readable root cause summary.
  - `suggested_actions`: Specific remediations suggested for the human engineer.

---

## 6. Open Constants & Thresholds

Per the Phase 2 status and watchlist (ARR-02, ARR-03), the following parameters remain **`OPEN`** as configurable `DESIGN_CHOICE` defaults pending Phase 7 empirical calibration:
- Maximum repair iterations $K$ (default: 5, pending EXP-004).
- Drift tolerance thresholds (pending EXP-006).
- Invariant blocking enforcement (advisory-first until rule calibration).

---

## 7. Architectural Invariants Bound

- **INV-003 (Machine Decidability of Done)**: `CONVERGED` requires 100% pass rate across all active verification layers.
- **INV-005 (Provenance of Evidence)**: The resulting `evidence_id` points to immutable hashed logs anchored to Git `HEAD`.
