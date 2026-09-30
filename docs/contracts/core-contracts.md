# Core Architectural Contracts (`CORE-CONTRACT-001` .. `009`)

**Status:** ACCEPTED  
**Authority:** Canonical Phase 3 Core Contracts Specification  
**Constitutional Basis:** CONSTITUTION.md (Articles I, II, III, IV, VI, VIII, IX)

---

## 1. Architectural Justification Analysis

In accordance with Phase 3 instructions, each core entity is audited to determine its strict contractual necessity before formalization:

| Entity | Contract ID | Required? | Why? | Producer | Consumer | Invariant Bound |
|---|---|---|---|---|---|---|
| **Project** | `CORE-CONTRACT-001` | **YES** | Authoritative identity, language, harness, and governance boundary for a repository. | CLI `init`, operator | All domains | `INV-001`, `INV-002` |
| **Task** | `CORE-CONTRACT-002` | **YES** | Enforces contract-bounded subagent dispatch with explicit scope and tools. | Orchestration, Spec Planner | Subagents, Verifier, ContextRouter | `INV-003`, `INV-002` |
| **Agent** | `CORE-CONTRACT-003` | **YES** | Declares model, context budget, tools, and isolation level (worktree/sandbox). | Orchestration | HarnessAdapter, SandboxSupervisor | `INV-001`, `INV-002` |
| **Session** | `CORE-CONTRACT-004` | **YES** | Bounds interactive sessions, tracking token burn and execution cost across turns. | CLI, Harness | Progress, Reporting, EventLog | `INV-004`, `INV-001` |
| **Evidence** | `CORE-CONTRACT-005` | **YES** | Verifiable execution proof (exit codes, logs, hashes) required for convergence. | Tool Runner, Sandbox, Verifier | Verifier, Feature Passport, EventLog | `INV-003`, `INV-005` |
| **Finding** | `CORE-CONTRACT-006` | **YES** | Structured diagnostic findings consumed by repair agents without natural language ambiguity. | InvariantChecker, Linter, Gateway | Verifier, Orchestrator, ContextRouter | `INV-003` |
| **Artifact** | `CORE-CONTRACT-007` | **YES** | Tracks generated files and diffs with SHA-256 hashes to prevent filesystem clobbering. | Subagent, Tool execution | Verifier, Git Committer, Orchestrator | `INV-002`, `INV-003` |
| **Capability & Permission** | `CORE-CONTRACT-008` | **YES** | Enforces Policy-as-Physics: least-privilege capability grants for subagents/skills. | Project Config, Orchestration | SandboxSupervisor, SkillGateway | `INV-002`, Art. III |
| **Invariant** | `CORE-CONTRACT-009` | **YES** | Machine-checkable definition of architectural boundaries and forbidden dependencies. | Governance | InvariantChecker, Verifier | `INV-001`..`006` |

---

## 2. Core Contract Specifications

### 2.1 Project Contract (`CORE-CONTRACT-001`)
- **Schema:** [`project.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/project.schema.json)
- **Scope:** Root repository configuration file (`.eidos/project.json`).
- **Guarantees:**
  - Strict documentation language declaration (`es`, `en`, `pt`, `fr`, `de`, `zh`).
  - Primary harness binding (`antigravity`, `claude_code`, `opencode`, `codex`, `hermes`, `headless`).
  - Strict SemVer project version.

### 2.2 Task Contract (`CORE-CONTRACT-002`)
- **Schema:** [`task.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/task.schema.json)
- **Scope:** Dispatched unit of work.
- **Guarantees:**
  - Must specify `target_files` (at least 1), `allowed_tools` (at least 1), and `acceptance_criteria` (at least 1).
  - Maximum turn count bounded ($\le 50$, default 30).
  - Status progression: `PENDING → IN_PROGRESS → VERIFIED → CONVERGED | FAILED | ESCALATED`.

### 2.3 Agent Contract (`CORE-CONTRACT-003`)
- **Schema:** [`agent.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/agent.schema.json)
- **Scope:** Subagent definition.
- **Guarantees:**
  - Strict isolation level (`in_process`, `worktree`, `container`, `sandbox`).
  - Hard upper bound on `context_budget`.
  - Zero parent chat history inherited (fresh context guarantee per Constitution Art. IX).

### 2.4 Session Contract (`CORE-CONTRACT-004`)
- **Schema:** [`session.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/session.schema.json)
- **Scope:** Interactive or batch execution session.
- **Guarantees:**
  - Cumulative accounting of `total_tokens_consumed` and `total_cost_usd`.
  - Correlation to active specification (`active_spec_id`).

### 2.5 Evidence Contract (`CORE-CONTRACT-005`)
- **Schema:** [`evidence.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/evidence.schema.json)
- **Scope:** Machine-checkable proof.
- **Guarantees:**
  - Anchored to Git HEAD commit SHA.
  - Epistemic classification (`observed`, `reproduced`, `inferred`, `human_confirmed`).
  - Exact command, exit code, stdout/stderr captures.

### 2.6 Finding Contract (`CORE-CONTRACT-006`)
- **Schema:** [`finding.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/finding.schema.json)
- **Scope:** Static, invariant, or runtime diagnostic finding.
- **Guarantees:**
  - Severity enum: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.
  - Category enum: `SECURITY`, `ARCHITECTURE`, `PERFORMANCE`, `DEAD_CODE`, `DRIFT`, `BUG`, `INVARIANT`.
  - Exact file path and line range $[start, end]$.

### 2.7 Artifact Contract (`CORE-CONTRACT-007`)
- **Schema:** [`artifact.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/artifact.schema.json)
- **Scope:** Files modified or generated by an execution.
- **Guarantees:**
  - Cryptographic SHA-256 fingerprint (64 hex characters).
  - Explicit action: `created`, `modified`, `deleted`.
  - Epistemic provenance marker.

### 2.8 Capability & Permission Contract (`CORE-CONTRACT-008`)
- **Schema:** [`capability-permission.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/capability-permission.schema.json)
- **Scope:** Security boundary grant.
- **Guarantees:**
  - Filesystem scope: `READ_ONLY`, `WORKTREE_ONLY`, `REPO_BOUNDED`.
  - Network egress: `DISABLED`, `LOOPBACK_ONLY`, `HOST_WHITELIST`.
  - `secret_access: false` (strictly immutable constant).

### 2.9 Invariant Contract (`CORE-CONTRACT-009`)
- **Schema:** [`invariant.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/invariant.schema.json)
- **Scope:** Architectural rules.
- **Guarantees:**
  - Enforcement level: `ADVISORY` (default pre-calibration) | `BLOCKING`.
  - Forbidden import paths and required interface declarations.
  - Status: `ARCHITECTED`, `CONTRACT_BOUND`, `CALIBRATED`.
