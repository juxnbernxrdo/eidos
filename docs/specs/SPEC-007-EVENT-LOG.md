# SPEC-007 — Append-Only Progress Logger & Git HEAD Anchoring

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of the Event Log persistence subsystem: maintaining an immutable, append-only JSONL log of all significant engineering actions, state transitions, tool invocations, and verification results anchored to Git HEAD commit SHAs.

## 3. Scope
Event appending, file locking, JSONL streaming, sequential replay, query filtering, and Git commit anchoring.

## 4. Non-Goals
- Does not replace Git (Git is the ground-truth substrate for physical files).
- Does not edit historical events (in-place modification is strictly forbidden).
- Does not execute arbitrary database transactions.

## 5. Source Requirements
- `REQ-EVT-001`: Append-Only Immutable Persistence
- `REQ-EVT-002`: Git HEAD Anchoring

## 6. Architectural Basis
- `docs/architecture/progress.md`: Event hierarchy and immutability rules.
- `docs/adr/P2-ADR-007`: Progress, passports, and append-only event sourcing.
- `CONSTITUTION.md` Article VIII: Event-sourced traceability and atomic progress logging.

## 7. Contract Dependencies
- `EVENT-CONTRACT-001`: Event Log Contract schema (`schemas/contracts/events/event-log.schema.json`).
- `CORE-CONTRACT-004`: Session Contract schema.

## 8. Behavioral Requirements
The logger writes events to `.eidos/progress/events.jsonl`.
- Each event is an atomic JSON record terminated by a newline.
- Every event contains a monotonically increasing or hash-chained `event_id`.
- Every event records `git_commit` representing `git rev-parse HEAD`.
- To correct a previous mistake or invalid event $e_k$, the logger appends a new event of type `SUPERSEDING_CORRECTION` specifying `supersedes_event_id: e_k`. Past lines are never edited.

## 9. Inputs
- Valid event payload conforming to `EVENT-CONTRACT-001`.
- Active Git repository context.

## 10. Outputs
- Appended event record with byte offset and persisted `event_id`.
- Replay stream for state reconstruction.

## 11. State Model
Append-only log; state transitions occur via events:
`Event Dispatched → Schema Validation → Git Anchor Fetch → File Lock Acquisition → Atomic Write → Release Lock`.

## 12. Invariants
- `INV-002`: Event payloads cannot contain paths or data from other projects.
- `INV-007`: The event log is immutable; truncation or in-place edit is a fatal violation.

## 13. Preconditions
- The `.eidos/progress/` directory must be writable.
- Payload must pass validation against `schemas/contracts/events/event-log.schema.json`.

## 14. Postconditions
- The event is flushed to disk and verifiable via read stream immediately after return.

## 15. Failure Semantics
If disk is full or write fails, the logger raises `RESOURCE_UNAVAILABLE` and aborts the active operation fail-closed.

## 16. Security Requirements
- Events must never record plaintext secrets, access tokens, or sensitive API keys.
- Multi-process writes must use OS file locks (`fcntl.flock`) to prevent log corruption.

## 17. Observability Requirements
- Emits metrics on total log size (bytes), event count, and write latency (milliseconds).

## 18. Edge Cases
- Detached HEAD or uncommitted repo: Logger records `"HEAD"` or the nearest valid commit hash.
- Corrupted log line: Replay stops with an explicit `PROVENANCE_INVALID` error and prompts operator repair.

## 19. Acceptance Criteria
### `AC-007-01` (Append-Only Immutability)
```gherkin
Given an existing events.jsonl file with 100 events
When a new valid event is logged
Then the file length must increase by exactly 1 line and all prior 100 lines must remain byte-identical.
```

### `AC-007-02` (Git HEAD Anchoring)
```gherkin
Given a repository at Git commit abc1234
When any task or verification event is logged
Then the event's git_commit property must equal "abc1234".
```

## 20. Verification Strategy
Automated tests in `tests/specs/test_event_log.py` verifying multi-process append safety, Git commit anchoring, and supercession event generation.

## 21. Traceability
- Research: EVD-015
- ADR: `P2-ADR-007`
- Contract: `EVENT-CONTRACT-001`
- Requirements: `REQ-EVT-001`, `REQ-EVT-002`

## 22. Open Questions & Phase 5 Notes
- Event log rotation or archival policy for very long-lived projects is an open operational detail (`ARR-03`).
- Phase 5 note: Use buffered atomic appends with `flock` to ensure thread-safe and process-safe concurrency.
