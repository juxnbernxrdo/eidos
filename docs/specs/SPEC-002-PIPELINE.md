# SPEC-002 — Phased Orchestration Pipeline

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the non-bypassable phased execution pipeline of Eidos. The pipeline coordinates the lifecycle of engineering tasks from initial repository discovery through specification, planning, execution, verification, bounded repair, and convergence or escalation.

## 3. Scope
Phase transitions, stage precondition validation, bounded repair loop execution ($K \le 5$), rollback mechanisms, and escalation dispatch.

## 4. Non-Goals
- Does not run autonomous open-ended agency loops without stage gates.
- Does not perform human code review (delegated to human escalation).
- Does not directly execute shell commands (delegated to SandboxSupervisor / HarnessAdapter).

## 5. Source Requirements
- `REQ-PIPE-001`: Enforced Progression of Phased Engineering Pipeline
- `REQ-PIPE-002`: Strict Upper Bound on Automated Repair Retries
- `REQ-PIPE-003`: Comprehensive Diagnostic Diffs on Escalation

## 6. Architectural Basis
- `docs/architecture/overview.md`: Phased non-bypassable pipeline.
- `docs/adr/P2-ADR-001`: Pipeline architecture with verification-first convergence.
- `docs/research/evidence-registry.md`: EVD-002 (Agentless cost-efficiency vs open loops), EVD-001 (ACI 8-13× cost difference).

## 7. Contract Dependencies
- `CORE-CONTRACT-002`: Task Contract.
- `VERIF-CONTRACT-001`: Verifier Contract and Verdict Payload.
- `CORE-CONTRACT-010`: Feature Passport Contract.

## 8. Behavioral Requirements
The pipeline must strictly enforce the sequential execution sequence:
$$\text{DISCOVERY} \to \text{SPECIFY} \to \text{PLAN} \to \text{EXECUTE} \to \text{VERIFY} \to [\text{REPAIR} \to \text{VERIFY}]^* \to \text{CONVERGED} \mid \text{ESCALATED}$$
No stage can be skipped. If verification fails and repair attempts $< K$, the pipeline rolls back uncommitted changes to the last clean checkpoint, feeds the machine oracle trace to the repair agent, and re-executes verification.

## 9. Inputs
- Task specification conforming to `CORE-CONTRACT-002`.
- Active repository graph and context budget parameters.
- Repair bound parameter $K$ (default: 5, open DESIGN_CHOICE).

## 10. Outputs
- On Success: Stamped Feature Passport with `status: CONVERGED`.
- On Escalation: Diagnostic diff, error trace, and `escalation_payload`.

## 11. State Model
```text
[DISCOVERY] ──► [SPECIFY] ──► [PLAN] ──► [EXECUTE] ──► [VERIFY] ──┬──► [CONVERGED]
                                                          ▲        │
                                                          │        ├──► [REPAIR] (if attempts < K)
                                                          └────────┘
                                                                   │
                                                                   └──► [ESCALATED] (if attempts >= K)
```

## 12. Invariants
- `INV-001`: Pipeline state transitions are independent of any host model or harness.
- `INV-003`: `CONVERGED` state can only be reached if all verification layers pass.

## 13. Preconditions
- The workspace must be in a clean Git working state or on a dedicated worktree branch.
- Task contract must be fully populated with target files and acceptance criteria.

## 14. Postconditions
- On convergence, a new Git commit is anchored with the Feature Passport SHA.
- On escalation, the worktree retains the attempted changes and outputs full diagnostic diffs.

## 15. Failure Semantics
If an unhandled exception or crash occurs during execution, the pipeline halts immediately, captures terminal stderr, marks the task as `FAILED`, and logs an event.

## 16. Security Requirements
- Each stage must run under declared capability grants.
- Escalation payloads must redact secrets or sensitive environment credentials.

## 17. Observability Requirements
- Emits structured progress events at the entry and exit of each phase:
  `TASK_INITIALIZED`, `VERIFICATION_STARTED`, `REPAIR_ATTEMPTED`, `TASK_CONVERGED`, `TASK_ESCALATED`.

## 18. Edge Cases
- Task cancellation by operator: Pipeline halts gracefully, discards working changes, and transitions to `CANCELLED`.
- Flaky tests: Verifier layer conducts pre-screen checks before entering repair loops.

## 19. Acceptance Criteria
### `AC-002-01` (Non-Bypassable Gating)
```gherkin
Given a task in the DISCOVERY stage
When an operator or subagent attempts to trigger EXECUTE directly
Then the pipeline must reject the transition and remain in DISCOVERY.
```

### `AC-002-02` (Repair Loop Bounding at $K$)
```gherkin
Given a task executing its 5th verification attempt with K=5
When the verifier emits a failure verdict
Then the pipeline must transition to ESCALATED without attempting a 6th repair cycle.
```

### `AC-002-03` (Diagnostic Diff on Escalation)
```gherkin
Given a task transitioning to ESCALATED
When the pipeline emits the escalation payload
Then the payload must contain a valid unified git diff and human-readable failure summary.
```

## 20. Verification Strategy
Integration tests simulating synthetic task failures, checking phase step transitions and enforcement of the $K=5$ retry limit.

## 21. Traceability
- Research: EVD-001, EVD-002, EVD-009
- ADR: `P2-ADR-001`
- Contract: `CORE-CONTRACT-002`, `VERIF-CONTRACT-001`, `CORE-CONTRACT-010`
- Requirements: `REQ-PIPE-001`, `REQ-PIPE-002`, `REQ-PIPE-003`

## 22. Open Questions & Phase 5 Notes
- Dynamic calculation of $K$ based on task complexity remains an open research item (`EXP-004`).
- Phase 5 note: The pipeline engine must maintain clean separation from harness-specific dispatchers.
