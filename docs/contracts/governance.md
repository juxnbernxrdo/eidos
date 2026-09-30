# Eidos Contract Governance Framework

**Status:** ACCEPTED  
**Version:** 1.0.0  
**Authority:** Canonical Phase 3 Contract Governance  
**Constitutional Basis:** CONSTITUTION.md (Articles II, III, IV, VI, VII, IX)

---

## 1. Foundational Contract Principles

All contracts in Eidos must strictly adhere to the following eleven governing principles:

1. **Explicitness**: Every input parameter, return type, error condition, state transition, and required capability must be explicitly declared. No implicit assumptions or hidden global side effects are permitted.
2. **Determinism Where Feasible**: For identical inputs, deterministic subsystems (Core, Graph Querier, Invariant Checker, Event Reducer) must return identical outputs. Where stochasticity exists (LLM inference), the contract must isolate the non-deterministic output with explicit confidence and provenance markers.
3. **Dual-Plane Symmetry (Machine + Human)**: Every contract exists simultaneously as a human-readable architecture specification (`docs/contracts/*.md`) and a machine-readable validation schema (`schemas/contracts/**/*.schema.json`). Neither plane is permitted to diverge silently.
4. **Strict Versionability**: All contracts are versioned using Semantic Versioning (SemVer 2.0.0). Every data payload must reference its governing contract ID and schema version.
5. **Fail-Closed Semantics**: If a schema validation fails, a permission check is ambiguous, or an unexpected exception occurs, execution must fail securely and deterministically (`fail-closed`). Default-allow is strictly prohibited.
6. **Security Boundaries & Least Privilege**: No contract grants implicit access to the filesystem, network, execution runtime, or cross-project memory. All capabilities must be explicitly declared and granted through the security boundary.
7. **Epistemic Provenance Preservation**: All claims, edges, findings, and results must preserve their epistemic status (`EXTRACTED`, `INFERRED`, `USER_CONFIRMED`, `AGENT_PROPOSED`). Provenance can never silently disappear during data transformations.
8. **Explicit Error Taxonomy**: Generic errors (e.g., `Error`, `Exception`, `fail`) are strictly prohibited in contract schemas. All errors must map to canonical error codes with typed details and remediation guidance.
9. **Explicit State Transitions**: Components with lifecycles (Harness Adapters, Tasks, Sessions, Verification Loops) must formally specify valid state machines. Unspecified or spontaneous transitions are contractual violations.
10. **Machine Validation First**: Contracts must be verifiable by automated machinery before runtime execution occurs. A task payload that fails schema validation is rejected before invoking any tool or agent.
11. **Traceability by Construction**: Every contract must maintain an auditable link backwards to its supporting architectural decision (P2-ADR) and empirical evidence (EVD), and forwards to its Phase 4 specification handoff.

---

## 2. Dual-Plane Contract Architecture

Eidos maintains two tightly synchronized representations for every system boundary:

```text
       Human-Readable Plane                   Machine-Readable Plane
┌─────────────────────────────────┐   1:1    ┌─────────────────────────────────┐
│   docs/contracts/<name>.md      │ ◄──────► │ schemas/contracts/<name>.json   │
│  - Conceptual Purpose & Context │          │  - JSON Schema Draft 2020-12    │
│  - Method & Property Analysis   │          │  - Strict Data Types & Enums    │
│  - State Machine & Invariants   │          │  - Required Properties          │
│  - Security & Provenance Rules  │          │  - Structural Constraints       │
│  - Open Constants & Thresholds  │          │  - AdditionalProperties: False  │
└─────────────────────────────────┘          └─────────────────────────────────┘
```

Automated contract tests (`tests/contracts/`) ensure that the two planes remain mutually consistent and that all schemas validate cleanly against JSON Schema Draft 2020-12.

---

## 3. Contract Lifecycle States

Every contract registered in Eidos progresses through five formal lifecycle states:

```text
  [ DRAFT ] ────────► [ REVIEW ] ────────► [ ACCEPTED ]
                                                 │
                                                 ├───► [ DEPRECATED ]
                                                 │
                                                 └───► [ SUPERSEDED ]
```

1. **`DRAFT`**: Initial design under construction; not yet approved for dependent subsystems.
2. **`REVIEW`**: Proposed contract under architectural inspection; schema frozen for test validation.
3. **`ACCEPTED`**: Approved binding contract for the current phase; actively enforced by validators.
4. **`DEPRECATED`**: Active contract scheduled for retirement; supported until next major milestone.
5. **`SUPERSEDED`**: Replaced by a newer major contract version; retained for historical replay.

*Rule:* States `VALIDATED` and `PRODUCTION_READY` are prohibited in Phase 3, as empirical benchmark validation occurs in Phase 7 (Constitution Honesty Axiom).

---

## 4. Contract Versioning Policy

Eidos contracts adopt **Semantic Versioning (SemVer 2.0.0)** formatted as `MAJOR.MINOR.PATCH`:

### MAJOR (X.0.0) — Breaking Changes
A MAJOR increment indicates an incompatible contractual modification. Examples:
- Removing or renaming an existing property or method.
- Adding a new `required` property to an input schema.
- Narrowing the allowed types or enum values of an existing property.
- Altering the semantic meaning or invariant constraints of an existing interface.
- Removing an existing lifecycle state or valid transition.

### MINOR (x.Y.0) — Backward-Compatible Additions
A MINOR increment indicates an additive, non-breaking capability enhancement. Examples:
- Adding a new `optional` property to an existing schema.
- Introducing a new permissible lifecycle state that does not invalidate existing paths.
- Adding a new optional method or capability flag.
- Expanding output payloads with supplemental metadata while preserving core fields.

### PATCH (x.y.Z) — Non-Semantic Fixes
A PATCH increment indicates bug fixes, documentation clarifications, or typographical corrections that do not alter the structural validation or runtime behavior of the contract.

---

## 5. Contract Compatibility Semantics

| Compatibility Mode | Definition | Requirement |
|---|---|---|
| **Backward Compatibility** | Newer components can consume payloads generated by older contract versions. | Default requirement for all MINOR and PATCH updates. Old data remains parseable. |
| **Forward Compatibility** | Older components can gracefully handle or ignore unrecognized fields from newer versions. | Schemas should allow controlled extension points or version-negotiation handshakes. |
| **Breaking Change** | Incompatible change requiring coordinated system-wide migration. | Requires MAJOR version bump, migration guide, and deprecation period. |
| **Unknown Compatibility** | Payload version cannot be mapped to the known contract registry. | Must fail-closed with `VERSION_MISMATCH` error. Unregistered schemas cannot be evaluated. |

---

## 6. Canonical Error Semantics

To eliminate vague runtime failures, all contract-bound interfaces must emit structured error payloads conforming to the canonical error taxonomy:

```json
{
  "code": "PERMISSION_DENIED",
  "category": "SECURITY",
  "message": "Subagent 'agent-42' attempted write to '/etc/hosts' without grant.",
  "details": {
    "target_path": "/etc/hosts",
    "required_capability": "fs:write:system",
    "granted_capabilities": ["fs:read:repo", "fs:write:worktree"]
  },
  "remediation": "Request explicit system write grant in task contract security scope.",
  "timestamp": "2026-09-30T15:30:00Z"
}
```

### Standard Error Codes:
- `INVALID_INPUT`: Payload fails schema structural or type validation.
- `UNSUPPORTED_CAPABILITY`: Requested operation is not supported by the active harness or adapter.
- `PERMISSION_DENIED`: Operation violates security sandbox or capability boundaries.
- `CONTRACT_VIOLATION`: Component violated an explicit precondition or postcondition.
- `RESOURCE_UNAVAILABLE`: Required external entity, file, or service cannot be resolved.
- `VERIFICATION_FAILED`: Verification layer failed to satisfy acceptance criteria.
- `PROVENANCE_INVALID`: Entity lacks required epistemic source or contains invalid confidence rating.
- `VERSION_MISMATCH`: Payload version incompatible with receiver's contract version.
- `INVARIANT_VIOLATION`: Operation violates an immutable architectural invariant.
- `EXECUTION_TIMEOUT`: Operation exceeded allocated turn count or time budget.

---

## 7. Security Boundaries & Capability Scoping

Contracts must enforce the foundational trust boundary stack:

```text
Agent ──▶ Skill ──▶ Tool ──▶ Filesystem ──▶ Repository ──▶ Network ──▶ External Service
```

### Security Rules for Contracts:
1. **Explicit Capability Grants**: An agent or tool possesses zero permissions by default. Every action requiring I/O must reference an explicit capability grant (e.g., `fs:read:repo`, `fs:write:worktree`, `net:outbound:disabled`).
2. **Path Confinement**: Filesystem permissions must be strictly scoped to the repository root or dedicated worktree. Access outside the workspace root is rejected with `PERMISSION_DENIED`.
3. **Network Isolation**: By default, network egress is disabled (`net:egress:none`) unless an explicit external endpoint is declared and approved.
4. **Secret Blindness**: Secrets and authentication tokens must never be written to task contracts, MSC payloads, event logs, or repository graphs.

---

## 8. Epistemic Provenance Framework

To satisfy the Constitution Honesty Axiom (Article IX), all entities carrying factual claims, code analysis, or verification results must declare their epistemic provenance:

| Provenance Tag | Source Description | Permissible Confidence | Gating Authority |
|---|---|---|---|
| **`EXTRACTED`** | Deterministic output from parsers, compilers, AST analyzers, or Git hashes. | 1.0 (Exact) | Authoritative ground truth. |
| **`INFERRED`** | Output generated by LLM reasoning, heuristic retrieval, or semantic scoring. | $[0.0, 0.99]$ | May NOT override EXTRACTED facts. May NOT gate verification alone. |
| **`USER_CONFIRMED`** | Explicit human affirmation of an inference, requirement, or decision. | 1.0 (Affirmed) | Authoritative human intent. |
| **`AGENT_PROPOSED`** | Ephemeral hypothesis or proposal generated by an agent awaiting verification. | $[0.0, 1.0)$ | Advisory only. Quarantined upon conflict. |

---

## 9. Contract Quality Checklist

Before any contract transitions to `ACCEPTED`, it must fulfill the following sixteen quality gates:
- [x] Clear architectural basis (grounded in Phase 2 docs and P2-ADR).
- [x] Explicit purpose and non-goals.
- [x] Defined input payload schema.
- [x] Defined output payload schema.
- [x] Formal lifecycle state machine (if stateful).
- [x] Explicit error code bindings.
- [x] Explicit architectural invariants.
- [x] Enforced security and permission boundaries.
- [x] Epistemic provenance metadata attached.
- [x] Formal SemVer version identifier.
- [x] Documented compatibility semantics.
- [x] Validated JSON Schema Draft 2020-12 file.
- [x] Synchronized human-readable specification.
- [x] Automated test coverage in `tests/contracts/`.
- [x] Traceability link from Research through Phase 4 Input.
- [x] Clear Phase 4 specification handoff boundary.
