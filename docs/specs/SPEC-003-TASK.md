# SPEC-003 — Task Lifecycle & Bounded Transitions

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the complete lifecycle, state machine, preconditions, and transition rules for atomic, contract-bounded units of engineering work (Tasks) in Eidos.

## 3. Scope
Task state representation, transition validation, turn count accounting, target file bounding, and terminal state resolution.

## 4. Non-Goals
- Does not author specification documents (handled in Spec domain).
- Does not implement tool execution (handled by Execution/Sandbox domain).

## 5. Source Requirements
- `REQ-TASK-001`: Contract-Bounded Task Dispatch
- `REQ-TASK-002`: Deterministic Task State Transitions

## 6. Architectural Basis
- `docs/architecture/agents.md`: Subagent unit and bounded agency.
- `docs/adr/P2-ADR-003`: Contract-bounded subagents and CodeAct execution.
- `CONSTITUTION.md` Article IX: Contract-bounded subagents and fresh context guarantee.

## 7. Contract Dependencies
- `CORE-CONTRACT-002`: Task Contract schema (`schemas/contracts/core/task.schema.json`).
- `CORE-CONTRACT-003`: Agent Contract schema.
- `CORE-CONTRACT-008`: Capability & Permission Contract.

## 8. Behavioral Requirements
A task must strictly encapsulate its objective, target files, allowed tools, and acceptance criteria. It progresses through ten discrete lifecycle states:
```text
[CREATED] ──► [PLANNED] ──► [READY] ──► [RUNNING] ──► [VERIFYING] ──► [CONVERGED]
                                 │          ▲              │
                                 │          └── [REPAIRING]◄
                                 ▼                         │
                            [CANCELLED]               [FAILED] / [ESCALATED]
```
Transitions must be validated against explicit preconditions and postconditions. Uncontracted transitions fail closed.

## 9. Inputs
- Task payload conforming to `CORE-CONTRACT-002`.
- State change trigger event with operator or agent credentials.

## 10. Outputs
- Success: Updated Task record with new status and transition evidence.
- Error: `CONTRACT_VIOLATION` with task state remaining unchanged.

## 11. State Model
- `CREATED`: Task instantiated with ID, spec reference, and title.
- `PLANNED`: Target files, allowed tools, and criteria populated.
- `READY`: Assigned agent and capability grants locked; ready for dispatch.
- `RUNNING`: Dispatched to subagent/harness; turn counter actively incrementing.
- `VERIFYING`: Execution output received; verifier runner actively evaluating.
- `REPAIRING`: Local verification failed; oracle trace fed back for bounded repair.
- `CONVERGED`: All verification layers passed; passport stamped. (Terminal)
- `FAILED`: Unrecoverable execution error or syntax crash. (Terminal)
- `ESCALATED`: Exceeded retry bounds ($K$) or breached security constraint. (Terminal)
- `CANCELLED`: Aborted by human operator. (Terminal)

## 12. Invariants
- `INV-002`: Target files must reside strictly within the workspace root.
- `INV-003`: Task cannot transition to `CONVERGED` without a passing `VerificationResult`.

## 13. Preconditions
- Transition to `RUNNING` requires assigned agent and verified workspace cleanliness.
- Transition to `REPAIRING` requires `convergence_attempts < K`.

## 14. Postconditions
- On reaching `CONVERGED`, `convergence_attempts` is frozen and completion timestamp is recorded.

## 15. Failure Semantics
Attempting an invalid transition (e.g. `CREATED → RUNNING` without planning) immediately raises `CONTRACT_VIOLATION`.

## 16. Security Requirements
- Allowed tools list is strictly enforced: attempting to call a tool outside `allowed_tools` triggers `PERMISSION_DENIED`.
- Turn count is capped ($\le 50$, default 30) to prevent runaway execution loops.

## 17. Observability Requirements
- Emits structured telemetry on every transition: `task_id`, `from_state`, `to_state`, `trigger_actor`, `timestamp`.

## 18. Edge Cases
- Subagent hang / timeout: Task supervisor forcibly terminates execution after `timeout_seconds` and transitions task to `FAILED`.
- Multi-lane race: Tasks executed on parallel Git worktrees have distinct state objects.

## 19. Acceptance Criteria
### `AC-003-01` (Bounded Scope Validation)
```gherkin
Given a task payload with empty target_files or allowed_tools
When validation against CORE-CONTRACT-002 is executed
Then the task must be rejected before entering READY state.
```

### `AC-003-02` (Valid Lifecycle State Progression)
```gherkin
Given a task in READY state
When valid invoke() trigger is dispatched
Then task transitions to RUNNING and turn counter begins at 0.
```

## 20. Verification Strategy
Unit tests in `tests/specs/test_task_lifecycle.py` verifying all valid state paths and testing rejection of all illegal state jumps.

## 21. Traceability
- Research: EVD-004, EVD-009
- ADR: `P2-ADR-003`
- Contract: `CORE-CONTRACT-002`
- Requirements: `REQ-TASK-001`, `REQ-TASK-002`

## 22. Open Questions & Phase 5 Notes
- Phase 5 note: Task status transitions must be executed via atomic operations to avoid concurrent state races.
