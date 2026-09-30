# ADR-008: Event-Sourced Progress Log and Cryptographic Evidence Anchoring

**Status:** Accepted  
**Date:** 2024-09-30 (Updated 2026)  
**Deciders:** Juan Bernardo Ordóñez (Author), AI Agent Systems Architecture Team  

---

## Context
Standard AI coding agents report progress through ephemeral chat messages or unstructured markdown files (`PROGRESS.md`). When an agent fails, overwrites a working component, or makes an ungrounded architectural assertion, it is nearly impossible to determine *why* the decision was made, what evidence was evaluated, or which Git commit introduced the regression.

## Decision
Eidos implements an **Event-Sourced Progress and Cryptographic Evidence Architecture**:

### 1. Append-Only Event Stream
All orchestrator decisions, subagent invocations, tool outputs, verification runs, and human feedbacks are recorded as immutable event objects in:
`.eidos/progress/events.jsonl`

Each event complies with the `ProgressEvent` JSON schema and records:
- `event_id`: UUIDv4
- `timestamp`: UTC ISO 8601
- `session_id`: Active session identifier
- `task_id`: Linked task contract
- `agent_id`: Identifier of the executing subagent
- `event_type`: (`TASK_STARTED`, `TOOL_INVOKED`, `VERIFICATION_FAILED`, `PATCH_COMMITTED`, etc.)
- `payload`: Detailed structured payload
- `git_commit`: Current Git HEAD SHA

### 2. Evidence Anchoring
Every assertion, claim, or architectural finding must be anchored to verifiable evidence via the `Evidence` schema:
```json
{
  "evidence_id": "EVID-9021",
  "claim": "Module auth/jwt.py violates ARCH-001 by importing infrastructure/db.py",
  "evidence_type": "observed",
  "source_file": "src/auth/jwt.py",
  "line_range": [14, 15],
  "graph_node_id": "src/auth/jwt.py:import_db",
  "verification_command": "eidos invariant check ARCH-001",
  "exit_code": 1,
  "confidence": 1.0,
  "git_commit": "7f8b91a"
}
```

### 3. State Reconstruction & Time-Travel
The active project state (`.eidos/progress/state.json`) is a pure materialized projection derived by replaying `events.jsonl`. This allows Eidos to "time-travel" to any historical point in the development process to reconstruct the agent's exact knowledge state.

## Consequences

### Positive
- Absolute auditability: Every change, fix, and decision can be traced back to its root requirement and evidence anchor.
- Fault reconstruction: Post-mortem debugging can replay the exact sequence of events leading to a failure.
- Git synchronicity: Every progress event is tied directly to a specific Git commit SHA.

### Negative
- Log files grow monotonically over long-lived projects (mitigated by periodic state snapshotting in `.eidos/progress/snapshots/`).
