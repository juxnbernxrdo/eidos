# Verification Governance Framework

**Authority:** Eidos System Constitution Article IV & Phase 6 Mandate  
**Scope:** Verification Protocol, Epistemic Discipline, and Quality Gate Governance  

---

## 1. Definitional Separation

To avoid epistemic contamination, Eidos establishes strict boundaries between three distinct engineering activities:

| Dimension | Core Question | Governing Phase | Primary Output |
|:---|:---|:---:|:---|
| **Verification** | *"Does the implementation fulfill the normative specifications and contracts?"* | **Phase 6** | `VerificationResult` (`PASS` / `FAIL`) |
| **Evaluation** | *"How well does Eidos perform under controlled experimental conditions?"* | **Phase 7** | Empirical Metrics ($\Delta VSR$, Cost, Latency) |
| **Validation** | *"Does the system actually solve the user's underlying software engineering problem?"* | **Phase 7+** | Production Case Studies & Scientific Proof |

**Crucial Mandate:** Passing Phase 6 verification does **not** prove that Eidos outperforms existing agentic frameworks; it merely proves that Eidos functions deterministically according to its written specifications.

---

## 2. Epistemic Classification

All statements, log entries, and findings in Phase 6 must be tagged with explicit epistemic categories:

1. `FACT`: Machine-verified truth (e.g. Git commit hash, test assertion pass, AST node count).
2. `EVIDENCE`: Reproducible trace, command output, or recorded artifact backing a claim.
3. `OBSERVATION`: Raw measurement or terminal output before interpretive analysis.
4. `INTERPRETATION`: Analytical inference explaining an observation.
5. `HYPOTHESIS`: Unverified empirical conjecture (e.g. "K=5 is optimal for repair").
6. `DESIGN_DECISION`: Deliberate architectural choice registered in an ADR.
7. `UNKNOWN`: Unverified or uncalibrated parameter.

**Forbidden Transformations:**
- `HYPOTHESIS → FACT` (without Phase 7 experimental evaluation)
- `IMPLEMENTED → VERIFIED` (without Phase 6 machine evidence)
- `VERIFIED → VALIDATED` (without empirical user validation)
- `TEST PASSED → SCIENTIFICALLY SUPERIOR`

---

## 3. The 14 Verification Levels

Verification is executed across 14 discrete levels:

```text
┌────────────────────────────────────────────────────────┐
│ Level 1: Syntax & Packaging                            │
├────────────────────────────────────────────────────────┤
│ Level 2: Static Typing & Linting                       │
├────────────────────────────────────────────────────────┤
│ Level 3: Unit Verification & Boundary Cases            │
├────────────────────────────────────────────────────────┤
│ Level 4: Contract Schema Conformance (Draft 2020-12)   │
├────────────────────────────────────────────────────────┤
│ Level 5: Specification Acceptance Criteria (Given/When)│
├────────────────────────────────────────────────────────┤
│ Level 6: State Machine Determinism & Replay            │
├────────────────────────────────────────────────────────┤
│ Level 7: Architectural Invariant Checking              │
├────────────────────────────────────────────────────────┤
│ Level 8: Security Sandbox & Default-Deny Confinement   │
├────────────────────────────────────────────────────────┤
│ Level 9: Heterogeneous Graph Relational Semantics      │
├────────────────────────────────────────────────────────┤
│ Level 10: Context Routing & Minimal Sufficient Context │
├────────────────────────────────────────────────────────┤
│ Level 11: Contract-Bounded Subagent Isolation          │
├────────────────────────────────────────────────────────┤
│ Level 12: Host Harness Adapters & Trace Streaming      │
├────────────────────────────────────────────────────────┤
│ Level 13: Append-Only Event Log & Progress Projection  │
├────────────────────────────────────────────────────────┤
│ Level 14: Feature Passport 12-Dimensional Traceability │
└────────────────────────────────────────────────────────┘
```

---

## 4. Verification Repair Rules

When a verification procedure emits `FAIL`:
1. **Analyze Failure**: Identify root cause against the normative specification.
2. **Reparation Scope**: Repair the physical code strictly to satisfy the normative requirement.
3. **No Requirement Dilution**: Never relax an acceptance criterion, delete a requirement, or loosen a contract schema to make a test pass.
4. **Mandatory Reverification**: The entire verification battery must be re-run after every repair.
5. **Traceability**: All repairs must be documented in `docs/verification/repair-log.md` with commit SHA and evidence.
6. **Escalation**: If a defect reveals an irreconcilable conflict between Contract and Specification, halt repair, label as `IMPLEMENTATION_BLOCKED_BY_CONTRACT_SPEC_CONFLICT`, and escalate.

---

## 5. Phase 6 Gate Decision Criteria

The Quality Gate evaluates:
- **`PASS`**: All 14 verification levels report `PASS` with 0 blocking defects and 0 invariant violations.
- **`CONDITIONAL_PASS`**: All critical contracts, security controls, and invariants pass, but non-blocking experimental parameters (e.g. $K=5$, risk $< 25$) remain open pending Phase 7 calibration.
- **`BLOCKED`**: One or more critical verification checks fail, or architectural drift is detected.
