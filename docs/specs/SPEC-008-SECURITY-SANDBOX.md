# SPEC-008 — Security Boundaries, Capability Sandbox & Path Isolation

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the security supervisor subsystem: enforcing Policy-as-Physics, capability confinement, filesystem path isolation, network egress restriction, and secret redaction.

## 3. Scope
Process isolation, capability grant enforcement (`CORE-CONTRACT-008`), path confinement, network blocking, and secret redaction.

## 4. Non-Goals
- Does not replace host OS kernel security (builds upon standard Linux primitives).
- Does not implement prompt-based security instructions (prompt restrictions fail under injection).
- Does not provide secret management (Eidos is secret-blind).

## 5. Source Requirements
- `REQ-SEC-001`: Policy-as-Physics Capability Enforcement
- `REQ-SEC-002`: Zero Cross-Project Data Leakage
- `REQ-SEC-003`: Secret Blindness

## 6. Architectural Basis
- `docs/architecture/security.md`: Trust boundary stack and boundary mechanisms.
- `docs/adr/P2-ADR-006`: Skill Gateway and Sandbox Supervisor.
- `CONSTITUTION.md` Article III: Policy-as-Physics and zero unaudited execution.

## 7. Contract Dependencies
- `CORE-CONTRACT-008`: Capability & Permission Contract (`schemas/contracts/core/capability-permission.schema.json`).
- `HARN-CONTRACT-001`: Harness Adapter Contract.

## 8. Behavioral Requirements
The sandbox supervisor intercepts all subagent or tool execution requests.
- Maps requested action against the active `CapabilityPermissionContract`.
- If the action requires filesystem write, verifies target path is inside `allowed_write_patterns`.
- If the action requires network egress, verifies destination is in `allowed_hosts`.
- If permission check fails, halts execution immediately and raises `PERMISSION_DENIED`.

## 9. Inputs
- Command or script execution payload with argument list.
- Active capability grant conforming to `CORE-CONTRACT-008`.

## 10. Outputs
- Execution outcome (stdout, stderr, exit code) or immediate `PERMISSION_DENIED` error.

## 11. State Model
Enforces the trust boundary stack:
`Agent → Skill → Tool → Filesystem → Repository → Network → External Service`.
Every boundary crossing validates active grants fail-closed.

## 12. Invariants
- `INV-002`: Zero access to files, processes, or sockets outside the designated workspace root.
- `INV-008`: Policy-as-Physics: missing capability grant means `PERMISSION_DENIED`.

## 13. Preconditions
- The workspace root directory must be verified and resolved to its canonical absolute path.
- Capability grant must be cryptographically or structurally validated.

## 14. Postconditions
- All subprocesses spawned must terminate cleanly; orphaned background processes are killed upon turn exit.

## 15. Failure Semantics
Any attempt to access unauthorized paths (e.g. `/etc/passwd`, `~/.ssh`, sibling repos) triggers an immediate `PERMISSION_DENIED` security finding with severity `CRITICAL`.

## 16. Security Requirements
- Default-Deny: Zero filesystem write or network permissions unless explicitly declared.
- Secrets Redaction: Entropy scanner scrubs strings matching API key patterns (`ghp_`, `sk-`, etc.) from all output buffers.

## 17. Observability Requirements
- Emits security audit events on every rejected syscall, path violation, or unauthorized network attempt.

## 18. Edge Cases
- Symlink traversal: Paths resolving outside workspace root via symlinks are detected via `os.path.realpath` and rejected.
- Fork bombs / runaway processes: Subprocess pool is constrained with strict process limits (`RLIMIT_NPROC`) and execution timeouts.

## 19. Acceptance Criteria
### `AC-008-01` (Default-Deny File Write Enforcement)
```gherkin
Given a subagent granted scope READ_ONLY
When the subagent attempts to write to src/main.py
Then the supervisor intercepts the action, aborts the write, and emits PERMISSION_DENIED.
```

### `AC-008-02` (Cross-Project Path Confinement)
```gherkin
Given an execution confined to /home/user/project-a
When a command attempts to read /home/user/project-b/secret.txt
Then the supervisor blocks the read and records an INV-002 security finding.
```

### `AC-008-03` (Secret Redaction in Output)
```gherkin
Given a subprocess outputting text containing a pattern matching sk-proj-123456789abcdef
When the supervisor buffers the trace output
Then the token is replaced with "[REDACTED_SECRET]" before entering logs or context.
```

## 20. Verification Strategy
Integration tests in `tests/specs/test_security_sandbox.py` verifying path traversal blocking, secret masking, and capability enforcement.

## 21. Traceability
- Research: EVD-007, EVD-008
- ADR: `P2-ADR-006`
- Contract: `CORE-CONTRACT-008`
- Requirements: `REQ-SEC-001`, `REQ-SEC-002`, `REQ-SEC-003`

## 22. Open Questions & Phase 5 Notes
- Linux kernel sandboxing implementation (Landlock vs bubblewrap vs containers) is an open implementation choice (`EXP-005`).
- Phase 5 note: The supervisor must resolve all canonical paths before checking pattern globs to prevent symlink bypasses.
