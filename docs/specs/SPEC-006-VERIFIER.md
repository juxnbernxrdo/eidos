# SPEC-006 — 7-Layer Verification Runner & Bounded Repair Loop

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of the multi-layered Verification Runner: executing machine oracles, evaluating test results, enforcing invariant rules, determining repair eligibility, and certifying convergence or escalation.

## 3. Scope
Execution of verification layers (Tests, Static Types, Lint, Contracts, Invariants, Security, Drift), evaluation of machine oracle feedback, repair trace generation, and convergence gating.

## 4. Non-Goals
- Does not author test cases (handled by developers or subagents).
- Does not perform subjective aesthetic code review.
- Does not grant task completion without machine-verifiable evidence.

## 5. Source Requirements
- `REQ-VERIF-001`: Machine Decidability of Done
- `REQ-VERIF-002`: External Oracle Necessity for Repair
- `REQ-VERIF-003`: Seven-Layer Verification Execution

## 6. Architectural Basis
- `docs/architecture/verification.md`: Layer architecture and loop model.
- `docs/adr/P2-ADR-001`: Phased pipeline with verification-first convergence.
- `docs/research/evidence-registry.md`: EVD-009 (oracle necessity for self-repair), EVD-012 (formal verification), EVD-015 (test suite weaknesses).

## 7. Contract Dependencies
- `VERIF-CONTRACT-001`: Verifier Contract schema (`schemas/contracts/verification/verifier.schema.json`).
- `CORE-CONTRACT-005`: Evidence Contract.
- `CORE-CONTRACT-009`: Invariant Contract.

## 8. Behavioral Requirements
The Verifier runs active verification layers against the target workspace.
$$\text{Verify}(\text{Workspace}, \text{Task}) \to \text{VerificationResult}$$
- If all active layers pass: Emit `verdict: CONVERGED`, stamp passport eligibility, exit 0.
- If any layer fails:
  - If `attempt_index < K` and an external machine oracle output (traceback/diagnostic) exists: Emit `verdict: REPAIR_ELIGIBLE` with `external_oracle_trace`.
  - If `attempt_index >= K` or failure lacks external oracle: Emit `verdict: ESCALATED` with `escalation_payload`.

## 9. Inputs
- Target files and Git commit hash.
- Active layers list (`tests`, `static_types`, `lint`, `contracts`, `invariants`, `security`, `drift`).
- Repair attempt count and maximum retry bound $K$.

## 10. Outputs
- `VerificationResult` conforming to `VERIF-CONTRACT-001`:
  - `layer_results`: Status, counts, and diagnostic messages per layer.
  - `verdict_payload`: `verdict`, `converged`, `repair_eligibility`, `evidence_id`.

## 11. State Model
```text
[EXECUTE] ──► [VERIFY_RUN] ──► [EVALUATE_LAYERS]
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            │ all layers pass                                   │ failures detected
     ┌──────▼──────┐                                     ┌──────▼──────┐
     │  CONVERGED  │                                     │ attempts < K│
     └─────────────┘                                     └──────┬──────┘
                                                                │
                                            ┌───────────────────┴───────────────────┐
                                            │ yes (oracle exists)                   │ no (or no oracle)
                                     ┌──────▼──────┐                         ┌──────▼──────┐
                                     │   REPAIR    │                         │  ESCALATED  │
                                     └─────────────┘                         └─────────────┘
```

## 12. Invariants
- `INV-003`: Agent claims are not evidence. Done ⟺ all machine verification layers pass.
- `INV-005`: Every verification run emits an immutable `evidence_id` anchored to Git HEAD.

## 13. Preconditions
- The workspace must contain executable test suites and valid configuration files.
- The task contract must be in `VERIFYING` state.

## 14. Postconditions
- On `CONVERGED`, all active layers report status `PASS` with 0 failures and 0 blocking violations.
- An immutable evidence record is appended to `.eidos/progress/events.jsonl`.

## 15. Failure Semantics
Execution timeouts during test runs are classified as `VERIFICATION_FAILED` with severity `HIGH`, triggering repair eligibility with the timeout trace.

## 16. Security Requirements
- Tests run inside isolated sandbox processes; network egress is blocked by default.
- Verification commands must not leak secrets or execute unapproved shell scripts.

## 17. Observability Requirements
- Emits telemetry logging elapsed run time per layer, failure counts, and oracle trace byte sizes.

## 18. Edge Cases
- Flaky tests: Flaky test pre-screen runs failing tests up to 3 times before declaring true failure (EVD-015 mitigation).
- Missing test suite: If a task defines no test suite, the verification runner evaluates static types, linters, and invariant checks; `CONVERGED` requires explicit operator sign-off if tests are absent.

## 19. Acceptance Criteria
### `AC-006-01` (Convergence on 100% Pass)
```gherkin
Given a candidate patch with 0 test failures, 0 type errors, and 0 linter violations
When the verifier evaluates all active layers
Then verdict must be CONVERGED and converged must be true.
```

### `AC-006-02` (Repair Eligibility Requires Machine Oracle)
```gherkin
Given a test failure emitting an AssertionError traceback with attempts=1 and K=5
When the verifier evaluates the failure
Then verdict must be REPAIR_ELIGIBLE and external_oracle_trace must contain the exact traceback.
```

### `AC-006-03` (Exhaustion Escalation)
```gherkin
Given a test failure on attempt 5 with K=5
When the verifier evaluates the failure
Then verdict must be ESCALATED with reason ATTEMPTS_EXHAUSTED and repair_eligibility.is_eligible must be false.
```

## 20. Verification Strategy
Integration tests simulating synthetic test failures, type errors, invariant violations, and verifying the $K=5$ escalation threshold.

## 21. Traceability
- Research: EVD-009, EVD-012, EVD-015
- ADR: `P2-ADR-001`
- Contract: `VERIF-CONTRACT-001`, `CORE-CONTRACT-005`, `CORE-CONTRACT-009`
- Requirements: `REQ-VERIF-001`, `REQ-VERIF-002`, `REQ-VERIF-003`

## 22. Open Questions & Phase 5 Notes
- Threshold values for drift tolerances remain open pending Phase 7 calibration (`EXP-006`).
- Phase 5 note: The runner should execute pytest, mypy, and ruff via subprocess sandboxing with strict timeouts.
