# SPEC-001 — Core State Reducer & Event Fold Engine

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the deterministic state management kernel of Eidos. The core state of the repository, active tasks, and session progress is formally defined and computed strictly as a pure left-fold of immutable historical events over an initial state.

## 3. Scope
Pure state folding function, event application transitions, snapshot checkpointing, and replay reconstruction. Pure computation; zero direct filesystem, network, or external process I/O.

## 4. Non-Goals
- Does not implement file persistence (delegated to EventLog).
- Does not evaluate test assertions or execute code.
- Does not run LLM prompts or heuristic algorithms.

## 5. Source Requirements
- `REQ-CORE-001`: Event-Sourced Deterministic State Reconstruction
- `REQ-CORE-002`: Fail-Closed Rejection of Invalid State Transitions

## 6. Architectural Basis
- `docs/architecture/progress.md`: State fold formula $S_t = \text{Fold}(S_0, [e_1 \dots e_t])$.
- `docs/adr/P2-ADR-007`: Event sourcing, passports, and append-only auditability.
- `CONSTITUTION.md` Article II: Core domain logic pure, deterministic, and free of I/O.

## 7. Contract Dependencies
- `EVENT-CONTRACT-001`: Event log schema and event structure definition.
- `CORE-CONTRACT-001`: Project contract structure.
- `CORE-CONTRACT-002`: Task contract structure and status enums.

## 8. Behavioral Requirements
The state reducer must behave as a pure mathematical function:
$$\text{Reduce}: (S_{t-1}, e_t) \to S_t$$
Given an initial baseline state $S_0$ and a chronological sequence of valid events $[e_1, e_2, \dots, e_t]$, replaying the events through the reducer must always yield the exact same state representation $S_t$.

## 9. Inputs
- Current State $S_{t-1}$ (valid state dictionary conforming to project/task definitions).
- Event $e_t$ conforming to `EVENT-CONTRACT-001` (`event_id`, `timestamp`, `event_type`, `actor`, `payload`, `git_commit`, `provenance`).

## 10. Outputs
- Success: New state $S_t$.
- Failure: Typed domain error `CONTRACT_VIOLATION` or `INVALID_INPUT` with state remaining strictly at $S_{t-1}$.

## 11. State Model
The state object contains:
- `project`: Project metadata, lifecycle state, active harness.
- `active_session`: Session ID, operator, token consumption, cost.
- `tasks`: Dictionary of tasks mapped by `task_id` with current status and attempts.
- `last_event_id`: Monotonic ID of the last successfully applied event.
- `git_head`: Current Git commit SHA anchor.

## 12. Invariants
- `INV-001`: Core reducer logic has zero dependencies on any model provider.
- `INV-007`: Historical event reduction is monotonic; re-applying an already applied event raises `CONTRACT_VIOLATION`.

## 13. Preconditions
- Event $e_t$ must pass schema validation against `schemas/contracts/events/event-log.schema.json`.
- Event sequence timestamp and ID must be strictly greater than or equal to `last_event_id`.

## 14. Postconditions
- $S_t.\text{last\_event\_id} == e_t.\text{event\_id}$.
- $S_t.\text{git\_head} == e_t.\text{git\_commit}$.

## 15. Failure Semantics
If $e_t$ contains an unknown event type or requests an illegal state transition (e.g. attempting to mark an unverified task as CONVERGED), the reducer must raise an explicit `CONTRACT_VIOLATION` exception and abort the fold without corrupting $S_{t-1}$.

## 16. Security Requirements
- The reducer operates in-process with zero network or filesystem privileges.
- Replaying events cannot execute tool commands or trigger subagents.

## 17. Observability Requirements
- Emits reduction metrics: number of folded events, processing duration (microseconds), and SHA-256 digest of resulting state $S_t$.

## 18. Edge Cases
- Empty event stream: `Fold(S_0, [])` returns $S_0$ identically.
- Replaying millions of events: Snapshot checkpoint $S_{\text{snap}}$ can serve as $S_0$ for folding events $[e_{\text{snap}+1} \dots e_t]$.
- Event supercession: An event of type `SUPERSEDING_CORRECTION` modifies the projected outcome of the referenced event while preserving the full log.

## 19. Acceptance Criteria
### `AC-001-01` (Deterministic Fold)
```gherkin
Given a project initial state S_0 and an ordered list of 10 valid events [e_1 ... e_10]
When the core reducer evaluates Fold(S_0, [e_1 ... e_10]) twice in independent processes
Then both executions must produce identical state dictionaries with matching SHA-256 state hashes.
```

### `AC-001-02` (Illegal Transition Rejection)
```gherkin
Given a task in state PENDING
When an event of type TASK_CONVERGED is applied without preceding verification events
Then the reducer must raise CONTRACT_VIOLATION and the task status must remain PENDING.
```

## 20. Verification Strategy
Automated unit tests in `tests/specs/test_core_state.py` validating idempotency, snapshot resumption, and illegal transition rejection.

## 21. Traceability
- Research: EVD-015 (Reproducibility need)
- ADR: `P2-ADR-007`
- Contract: `EVENT-CONTRACT-001`, `CORE-CONTRACT-001`
- Requirements: `REQ-CORE-001`, `REQ-CORE-002`

## 22. Open Questions & Phase 5 Notes
- Snapshot compaction frequency (e.g. every 1000 events) is an open tuning parameter (`ARR-03`).
- Phase 5 note: The reducer must be implemented as a pure Python module with zero external network or OS imports.
