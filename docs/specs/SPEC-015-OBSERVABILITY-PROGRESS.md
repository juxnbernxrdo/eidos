# SPEC-015 — Event-Derived Progress & Observability

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of the progress projection and observability subsystem: ensuring that all progress metrics, dashboards, and completion scorecards are derived strictly from immutable event logs and Git anchors, rejecting unverified agent assertions.

## 3. Scope
Event stream projection, progress calculation, task completion verification, and operational telemetry aggregation.

## 4. Non-Goals
- Does not display speculative or hallucinated health scores.
- Does not trust natural language agent claims of completion.
- Does not send telemetry to unapproved external cloud endpoints.

## 5. Source Requirements
- `REQ-OBS-001`: Event-Derived Progress Reporting
- `REQ-OBS-002`: Comprehensive Operational Telemetry

## 6. Architectural Basis
- `docs/architecture/progress.md`: Progress architecture and event hierarchy.
- `docs/adr/P2-ADR-007`: Event sourcing and evidence-anchored progress.
- `CONSTITUTION.md` Article IV: Testing & Verification-First Mandate.

## 7. Contract Dependencies
- `EVENT-CONTRACT-001`: Event Log Contract schema.
- `CORE-CONTRACT-004`: Session Contract.
- `CORE-CONTRACT-005`: Evidence Contract.

## 8. Behavioral Requirements
The progress engine projects the event stream into queryable progress views:
$$\text{ProjectProgress}(\text{Events}) \to \text{ProgressState}$$
- Task completion percentage is computed strictly as the ratio of `CONVERGED` tasks to total planned tasks.
- If an agent asserts "Done" but no corresponding `VERIFICATION_PASSED` event exists, the task progress is reported as unconverged.
- System metrics (tokens, turn counts, cost, pass rates) are derived deterministically from event payloads.

## 9. Inputs
- Stream of events from `.eidos/progress/events.jsonl`.
- Active project specification and task list.

## 10. Outputs
- Progress view: Active tasks, completed tasks, failed tasks, total cost (USD), total tokens consumed, verified success rate (VSR).

## 11. State Model
Functional projection pipeline:
`Event Stream ──► Filter by Session/Project ──► Aggregate Metrics ──► Compute Verified State`.

## 12. Invariants
- `INV-003`: Progress reports must distinguish agent verbal claims from verified machine completion.
- `INV-005`: Every reported metric must link back to underlying event and evidence identifiers.

## 13. Preconditions
- The event log file must be readable.

## 14. Postconditions
- Projected progress figures must match exact counts of historical events.

## 15. Failure Semantics
If the event log contains unparseable lines or corrupted JSON, the engine reports the error and projects state only up to the last valid line.

## 16. Security Requirements
- Telemetry stays strictly local; no cross-project or remote transmission unless explicitly configured by the developer.

## 17. Observability Requirements
- Emits execution telemetry on projection duration and total events processed.

## 18. Edge Cases
- Session resume: When resuming an earlier session, progress is re-projected from the event log without loss of historical accounting.

## 19. Acceptance Criteria
### `AC-015-01` (Evidence-Gated Completion Metric)
```gherkin
Given a task where an agent emitted a text message stating "Task complete"
When progress is calculated without a machine VERIFICATION_PASSED event
Then the task must be reported as UNCONVERGED in the progress dashboard.
```

### `AC-015-02` (Deterministic Cost and Token Aggregation)
```gherkin
Given a session with 3 tool invocation events consuming 100, 200, and 300 tokens
When session progress is queried
Then total_tokens_consumed must equal exactly 600 tokens.
```

## 20. Verification Strategy
Automated unit tests in `tests/specs/test_observability_progress.py` verifying accurate event aggregation, refusal to trust verbal completion claims, and cost calculation.

## 21. Traceability
- Research: EVD-015
- ADR: `P2-ADR-007`
- Contract: `EVENT-CONTRACT-001`, `CORE-CONTRACT-004`
- Requirements: `REQ-OBS-001`, `REQ-OBS-002`

## 22. Open Questions & Phase 5 Notes
- CLI dashboard visualization formats (`rich` terminal UI vs JSON output) to be finalized in Phase 5.
- Phase 5 note: Progress calculation should be structured as an incremental streaming reducer to handle large event streams efficiently.
