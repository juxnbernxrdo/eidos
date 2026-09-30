# SPEC-009 — Host Harness Adapters & Trace Streaming

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of Harness Adapters: insulating Eidos Core from the idiosyncrasies of host agent environments (Antigravity, Claude Code, OpenCode, Codex, Hermes, Headless CI) while streaming execution traces into Eidos.

## 3. Scope
Harness detection, capability discovery, instruction/rule mounting (`configure`), task dispatch (`invoke`), output collection, and raw trace ingestion.

## 4. Non-Goals
- Does not implement proprietary AI model runtimes.
- Does not perform verification certification (verification belongs to Verifier domain per Principle P5).
- Does not infer host internal prompts or hidden model weights (Honesty Axiom).

## 5. Source Requirements
- `REQ-HARN-001`: Host-Neutral Portability Boundary
- `REQ-HARN-002`: Full Raw Observation Trace Collection

## 6. Architectural Basis
- `docs/architecture/harness.md`: Adapter concept, method verdicts (REQUIRED, OPTIONAL, DROPPED), and observability limits.
- `docs/adr/P2-ADR-005`: Harness adapter abstraction.
- `docs/research/evidence-registry.md`: EVD-001 (harness moves outcomes 3.1×), EVD-002 (Agentless), SRC-105 (MCP standard).

## 7. Contract Dependencies
- `HARN-CONTRACT-001`: Harness Adapter Contract schema (`schemas/contracts/harness/harness-adapter.schema.json`).
- `CORE-CONTRACT-002`: Task Contract.

## 8. Behavioral Requirements
The adapter must implement the formal six required operations:
1. `detect()`: Scans environment/workspace markers to identify active host harness.
2. `capabilities()`: Returns capability matrix (subagents, CodeAct, MCP, worktrees, trace fidelity).
3. `configure()`: Mounts `AGENTS.md` and MCP server configurations into the host.
4. `invoke(dispatch_req)`: Dispatches bounded task and returns an execution ID.
5. `collect_output(exec_id)`: Gathers summary, patch diffs, created artifacts, and errors.
6. `collect_trace(exec_id)`: Gathers full raw turn-by-turn trace stream.
Verification is explicitly excluded from adapter duties (adapters must not self-certify).

## 9. Inputs
- Dispatch request conforming to `schemas/contracts/harness/harness-adapter.schema.json`:
  - `task`, `context_payload`, `permissions`, `environment`.

## 10. Outputs
- Execution response conforming to `HARN-CONTRACT-001`:
  - `execution_id`, `status`, `patch_diff`, `artifacts`, `observation_trace`, `errors`.

## 11. State Model
```text
[UNDETECTED] ──► [DETECTED] ──► [AVAILABLE] ──► [CONFIGURED] ──► [READY] ──► [RUNNING] ──┬──► [COMPLETED]
                                                                                        ├──► [FAILED]
                                                                                        └──► [UNAVAILABLE]
```

## 12. Invariants
- `INV-001`: Host adapter specific code stays strictly in adapter packages; Core has zero host imports.
- `INV-003`: Adapter status `COMPLETED` signifies task execution end, **not** verification convergence.

## 13. Preconditions
- The host harness CLI or IPC transport must be available in PATH or connected via socket.
- Workspace permissions must allow writing temporary rule configurations.

## 14. Postconditions
- On completion, unified patch diff and artifact hashes are emitted.
- All temporaryIPC sockets are cleaned up.

## 15. Failure Semantics
If the host process crashes or drops connection, the adapter catches the signal, sets status to `FAILED`, captures stderr, and transitions to `READY` or `UNAVAILABLE`.

## 16. Security Requirements
- Environment variables passed to `invoke()` must be scrubbed of unauthorized secrets.
- Adapter must confine host operations to the active repository root.

## 17. Observability Requirements
- Emits turn-by-turn metrics: turn index, timestamp, tool called, execution duration, and exit code.

## 18. Edge Cases
- Unobservable host internals: If a host does not expose intermediate reasoning, `trace_fidelity` is marked `tool_calls_only` or `summary_only`. Eidos never hallucinates hidden trace steps.
- Headless CI mode: A pure CLI runner operates as the reference headless harness for automated evaluation (`EXP-001`).

## 19. Acceptance Criteria
### `AC-009-01` (Zero Host Leakage into Core)
```gherkin
Given a task dispatched to Claude Code or Antigravity
When the adapter executes the task
Then Eidos Core domain modules remain untouched and import zero host-specific proprietary modules.
```

### `AC-009-02` (Complete Raw Trace Collection)
```gherkin
Given a multi-turn task execution of 3 turns
When collect_trace() is invoked upon completion
Then the returned observation_trace array must contain exactly 3 turn objects with timestamp, action, and exit codes.
```

## 20. Verification Strategy
Mock adapter tests in `tests/specs/test_harness_adapter.py` validating state transitions, capability negotiation, and trace streaming.

## 21. Traceability
- Research: EVD-001, EVD-002, SRC-105
- ADR: `P2-ADR-005`
- Contract: `HARN-CONTRACT-001`
- Requirements: `REQ-HARN-001`, `REQ-HARN-002`

## 22. Open Questions & Phase 5 Notes
- MCP stdio transport overhead vs direct process spawning to be measured in Phase 7 (`EXP-007`).
- Phase 5 note: Implement Antigravity and Headless adapters as first-class initial targets.
