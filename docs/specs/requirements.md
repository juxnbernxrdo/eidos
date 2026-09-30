# Eidos System Requirements Catalog

**Status:** ACCEPTED  
**Version:** 1.0.0  
**Authority:** Canonical Phase 4 Requirements Inventory  
**Constitutional Basis:** CONSTITUTION.md (Articles I, II, III, IV, VI, VII, VIII, IX)

---

## 1. Core State & Reducer Domain

### `REQ-CORE-001` — Deterministic State Fold
- **Title:** Event-Sourced Deterministic State Reconstruction
- **Description:** The system must compute current runtime state strictly as a pure left-fold of valid historical events over an initial state: $S_t = \text{Fold}(S_0, [e_1 \dots e_t])$.
- **Source:** [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md), [`EVENT-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/event-log.md), Constitution Art. VIII
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-001-01`
- **Security Impact:** `CRITICAL` (Guarantees unalterable audit trails)
- **Verification Method:** `UNIT_TEST`

### `REQ-CORE-002` — Invalid Transition Rejection
- **Title:** Fail-Closed Rejection of Invalid State Transitions
- **Description:** Any event attempting an uncontracted state transition (e.g. `PENDING → CONVERGED` without verification) must be rejected with an explicit `CONTRACT_VIOLATION` error, leaving system state unchanged.
- **Source:** [P2-ADR-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-001-phased-verification-first-pipeline.md), [`CORE-CONTRACT-002`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/core-contracts.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-001-02`
- **Security Impact:** `HIGH`
- **Verification Method:** `UNIT_TEST`

---

## 2. Pipeline Orchestration Domain

### `REQ-PIPE-001` — Non-Bypassable Phase Gating
- **Title:** Enforced Progression of Phased Engineering Pipeline
- **Description:** The pipeline must enforce sequential stage progression: `DISCOVERY → SPECIFY → PLAN → EXECUTE → VERIFY → CONVERGE`. Skipping any phase is strictly prohibited.
- **Source:** [EVD-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-001-phased-verification-first-pipeline.md), Principle P6
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-002-01`
- **Security Impact:** `HIGH`
- **Verification Method:** `INTEGRATION_TEST`

### `REQ-PIPE-002` — Bounded Reflexion Loop ($K$-Bound)
- **Title:** Strict Upper Bound on Automated Repair Retries
- **Description:** When verification fails, automated repair loops must be strictly capped at $K \le 5$ iterations (configurable policy default). Upon exceeding $K$, the pipeline must transition to `ESCALATED`.
- **Source:** [EVD-009](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-001-phased-verification-first-pipeline.md), Constitution Art. IV
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-002-02`
- **Security Impact:** `MEDIUM` (Token burn prevention)
- **Verification Method:** `UNIT_TEST`

### `REQ-PIPE-003` — Human Escalation with Diagnostic Diffs
- **Title:** Comprehensive Diagnostic Diffs on Escalation
- **Description:** When an automated task escalates, the pipeline must emit an `escalation_payload` containing a cumulative unified diff, failure logs, and suggested human remediation actions.
- **Source:** [P2-ADR-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-001-phased-verification-first-pipeline.md), [`VERIF-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/verifier.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-002-03`
- **Security Impact:** `LOW`
- **Verification Method:** `INTEGRATION_TEST`

---

## 3. Task Lifecycle Domain

### `REQ-TASK-001` — Contract-Bounded Task Dispatch
- **Title:** Explicit Scope and Capabilities for Dispatched Tasks
- **Description:** Every dispatched task must declare target files, allowed tools, acceptance criteria, and maximum turns ($\le 50$, default 30). Tasks lacking these fields must be rejected at dispatch.
- **Source:** [EVD-004](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-003](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-003-contract-subagents-codeact.md), [`CORE-CONTRACT-002`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/core-contracts.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-003-01`
- **Security Impact:** `HIGH`
- **Verification Method:** `SCHEMA_VALIDATION`

### `REQ-TASK-002` — Deterministic Task State Transitions
- **Title:** Formal Ten-State Task Lifecycle
- **Description:** Tasks must transition strictly through valid states: `CREATED → PLANNED → READY → RUNNING → VERIFYING → REPAIRING → CONVERGED | FAILED | ESCALATED | CANCELLED`.
- **Source:** [`CORE-CONTRACT-002`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/core-contracts.md), [P2-ADR-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-001-phased-verification-first-pipeline.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-003-02`
- **Security Impact:** `MEDIUM`
- **Verification Method:** `UNIT_TEST`

---

## 4. Context Routing Domain

### `REQ-CTX-001` — Minimal Sufficient Context Assembly
- **Title:** Deliberate Context Assembly with Boundary Pinning
- **Description:** Context payloads must prune target files in full and neighbor files ($k \le 2$) to signatures/types. Critical interfaces must be pinned at prompt boundaries (start/end) to combat attention degradation.
- **Source:** [EVD-003](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [EVD-016](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-002-graph-msc-router.md), Principle P8
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-004-01`
- **Security Impact:** `MEDIUM`
- **Verification Method:** `UNIT_TEST`

### `REQ-CTX-002` — Auditable Selection Rationale
- **Title:** Mandatory Justification for Every Context Item
- **Description:** Every assembled context item must include a `selection_audit` containing `selection_reason`, `proximity_hops`, and matched query symbol.
- **Source:** [P2-ADR-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-002-graph-msc-router.md), [`CTX-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/context-router.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-004-02`
- **Security Impact:** `LOW`
- **Verification Method:** `SCHEMA_VALIDATION`

### `REQ-CTX-003` — Strict Token Budgeting and Quarantine
- **Title:** Hard Token Budget Enforcement and Adversarial Quarantine
- **Description:** The Context Router must never exceed `max_tokens - reserve_for_generation`. Contaminating, unverified, or out-of-budget items must be emitted into `quarantined_exclusions`.
- **Source:** [EVD-003](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-002-graph-msc-router.md), [`CTX-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/context-router.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-004-03`
- **Security Impact:** `HIGH`
- **Verification Method:** `UNIT_TEST`

---

## 5. Repository Graph Domain

### `REQ-GRAPH-001` — Storage-Agnostic Heterogeneous Graph
- **Title:** Graph Representation of Code Structure and Governance
- **Description:** The graph engine must support all 21 canonical node types (`File`, `Function`, `Spec`, `Rule`, `Evidence`, etc.) and the 11 closed relation types without hardcoding a concrete database backend.
- **Source:** [EVD-005](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-002-graph-msc-router.md), [`GRAPH-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/graph-store.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-005-01`
- **Security Impact:** `LOW`
- **Verification Method:** `UNIT_TEST`

### `REQ-GRAPH-002` — Epistemic Provenance on Graph Edges
- **Title:** Preservation of Edge Epistemic Origin and Confidence
- **Description:** Every edge must declare its epistemic provenance (`EXTRACTED`, `INFERRED`, `USER_CONFIRMED`, `AGENT_PROPOSED`) and confidence $\in [0.0, 1.0]$. `EXTRACTED` edges must carry confidence 1.0.
- **Source:** [P2-ADR-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-002-graph-msc-router.md), [`GRAPH-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/graph-store.md), Constitution Art. IX
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-005-02`
- **Security Impact:** `MEDIUM`
- **Verification Method:** `UNIT_TEST`

### `REQ-GRAPH-003` — Bounded Neighborhood Queries ($k \le 2$)
- **Title:** Graph Traversal Abstractions with Strict Hop Limits
- **Description:** Neighborhood queries must default to $k \le 2$ hops. High-level abstractions (`traverse`, `callers`, `callees`, `path`) must be exposed; raw AST or CPG queries must remain hidden from task agents.
- **Source:** [EVD-005](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-002](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-002-graph-msc-router.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-005-03`
- **Security Impact:** `LOW`
- **Verification Method:** `UNIT_TEST`

---

## 6. Verification Domain

### `REQ-VERIF-001` — Machine Decidability of Done
- **Title:** Verification Gated by Machine Oracles Only
- **Description:** Transition to `CONVERGED` occurs if and only if all active verification layers pass with 0 test failures, 0 type errors, 0 linter violations, and 0 blocking invariant violations. Agent verbal claims are ignored.
- **Source:** [EVD-009](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [EVD-015](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-001-phased-verification-first-pipeline.md), `INV-003`
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-006-01`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `INTEGRATION_TEST`

### `REQ-VERIF-002` — External Oracle Necessity for Repair
- **Title:** Mandatory Machine Oracle Trace for Repair Eligibility
- **Description:** A failed verification run is eligible for automated repair if and only if an external machine oracle output (traceback, compiler diagnostic, exit code) is present. Verbal-only repair loops are forbidden.
- **Source:** [EVD-009](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-001-phased-verification-first-pipeline.md), [`VERIF-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/verifier.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-006-02`
- **Security Impact:** `MEDIUM`
- **Verification Method:** `UNIT_TEST`

### `REQ-VERIF-003` — Seven-Layer Verification Execution
- **Title:** Multi-Layered Verification Architecture
- **Description:** The verifier must execute up to 7 distinct layers: Tests, Static Types, Lint, Contracts, Invariants, Security, and Drift.
- **Source:** [P2-ADR-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-001-phased-verification-first-pipeline.md), [verification.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/verification.md), [`VERIF-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/verifier.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-006-03`
- **Security Impact:** `HIGH`
- **Verification Method:** `INTEGRATION_TEST`

---

## 7. Event Log Domain

### `REQ-EVT-001` — Append-Only Immutable Persistence
- **Title:** Unalterable Event Log with Monotonic Ordering
- **Description:** Events in `.eidos/progress/events.jsonl` must be append-only. Modification, truncation, or deletion of past events is strictly prohibited. Corrections must append a `SUPERSEDING_CORRECTION` event.
- **Source:** [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md), [`EVENT-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/event-log.md), `INV-007`
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-007-01`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `UNIT_TEST`

### `REQ-EVT-002` — Git HEAD Anchoring
- **Title:** Binding Every Event to Git HEAD Commit SHA
- **Description:** Every event appended to the log must record the physical Git HEAD commit SHA-1/256 at the moment of emission.
- **Source:** [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md), Constitution Art. VIII
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-007-02`
- **Security Impact:** `HIGH`
- **Verification Method:** `UNIT_TEST`

---

## 8. Security & Capability Sandbox Domain

### `REQ-SEC-001` — Policy-as-Physics Capability Enforcement
- **Title:** OS-Level and Sandbox Enforced Capability Confinement
- **Description:** Security must not rely on prompt text. Execution must be confined by explicit capability grants (`CORE-CONTRACT-008`). Actions lacking grants must fail with `PERMISSION_DENIED`.
- **Source:** [EVD-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-006](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-006-skill-gateway-sandbox.md), Constitution Art. III, `INV-008`
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-008-01`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `INTEGRATION_TEST`

### `REQ-SEC-002` — Zero Cross-Project Data Leakage
- **Title:** Strict Workspace Boundary Confinement
- **Description:** Subagents, tools, memory queries, and adapters must not read, write, or query outside the designated repository workspace without explicit authorization.
- **Source:** [EVD-008](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-006](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-006-skill-gateway-sandbox.md), `INV-002`
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-008-02`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `UNIT_TEST`

### `REQ-SEC-003` — Secret Blindness
- **Title:** Exclusion and Redaction of Authentication Secrets
- **Description:** Secret access is strictly forbidden (`secret_access: false`). Any trace output matching secret entropy patterns must be redacted before entering logs or context payloads.
- **Source:** [P2-ADR-006](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-006-skill-gateway-sandbox.md), [`CORE-CONTRACT-008`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/core-contracts.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-008-03`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `UNIT_TEST`

---

## 9. Harness Adapter Domain

### `REQ-HARN-001` — Host-Neutral Portability Boundary
- **Title:** Isolation of External Harness Specifics from Core
- **Description:** Adapters must isolate host-specific details (Claude Code hooks, Antigravity brain artifacts, OpenCode TUI) while exposing a uniform contract interface (`HARN-CONTRACT-001`). Core must not import host SDKs.
- **Source:** [EVD-001](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [SRC-105](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/sources.md), [P2-ADR-005](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-005-harness-adapters.md), `INV-001`
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-009-01`
- **Security Impact:** `HIGH`
- **Verification Method:** `UNIT_TEST`

### `REQ-HARN-002` — Full Raw Observation Trace Collection
- **Title:** Complete Streaming of Tool Invocations and Terminal Logs
- **Description:** The adapter must capture the full raw observation stream (turn index, timestamp, action, tool input, output, exit code) for the immutable event log and evaluation runs.
- **Source:** [EVD-015](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-005](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-005-harness-adapters.md), [`HARN-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/harness-adapter.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-009-02`
- **Security Impact:** `MEDIUM`
- **Verification Method:** `UNIT_TEST`

---

## 10. Subagent & Execution Domain

### `REQ-AGENT-001` — Fresh Context per Subtask
- **Title:** Zero Conversational History Inheritance
- **Description:** Subagents must be spawned with fresh, isolated context containing only the assigned task contract and Minimal Sufficient Context payload. Inheriting messy parent conversation history is forbidden.
- **Source:** [EVD-004](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-003](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-003-contract-subagents-codeact.md), Constitution Art. IX
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-010-01`
- **Security Impact:** `HIGH`
- **Verification Method:** `UNIT_TEST`

### `REQ-AGENT-002` — CodeAct Programmatic Execution Space
- **Title:** Sandboxed Executable Code Actions over JSON Tool Calls
- **Description:** For programmatic engineering tasks, subagents must execute Python actions inside a sandbox rather than generating raw conversational tool calls, capturing tracebacks for self-debug.
- **Source:** [EVD-006](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-003](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-003-contract-subagents-codeact.md)
- **Priority:** `SHOULD`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-010-02`
- **Security Impact:** `HIGH`
- **Verification Method:** `INTEGRATION_TEST`

---

## 11. Memory Domain

### `REQ-MEM-001` — Tripartite Memory Scoping
- **Title:** Explicit Isolation Across Working, Project, and Institutional Memory
- **Description:** Working memory must be ephemeral (destroyed upon subtask completion). Project memory must be scoped to the active repo (`.eidos/memory/`). Institutional memory must be human-sanitized and approved.
- **Source:** [EVD-017](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-004](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-004-memory-opt-in.md), `ARR-01`
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-011-01`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `UNIT_TEST`

### `REQ-MEM-002` — Opt-In Gating for Persistent Memory
- **Title:** Memory Writes Gated by Explicit Configuration
- **Description:** Memory operations must be disabled by default (`opt-in only`, ARR-01). Writes to project memory must pass write-time consistency gating.
- **Source:** [EVD-017](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-004](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-004-memory-opt-in.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-011-02`
- **Security Impact:** `HIGH`
- **Verification Method:** `UNIT_TEST`

---

## 12. Skill Gateway Domain

### `REQ-SKILL-001` — Pre-Installation Static & YARA Scanning
- **Title:** Zero Unaudited Skills Security Verification
- **Description:** Every external skill must undergo static AST analysis, YARA scanning, and risk assessment before installation. Unaudited skills must be rejected.
- **Source:** [EVD-008](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-006](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-006-skill-gateway-sandbox.md), Constitution Art. III
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-012-01`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `INTEGRATION_TEST`

### `REQ-SKILL-002` — Cryptographic Hash Pinning in Manifest
- **Title:** Lockfile Pinning of Skill Packages
- **Description:** Installed skills must be recorded in `skills-lock.json` with commit hash and SHA-256 integrity digest.
- **Source:** [P2-ADR-006](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-006-skill-gateway-sandbox.md), [skills.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/skills.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-012-02`
- **Security Impact:** `HIGH`
- **Verification Method:** `UNIT_TEST`

---

## 13. Feature Passport Domain

### `REQ-PASS-001` — 12-Dimensional Traceability Certificate
- **Title:** Convergence Certification via 12 Dimensional Records
- **Description:** A Feature Passport must capture all 12 dimensions: Requirement, Spec, Architecture, Dependencies, Contracts, Implementation, Tests, Security, Documentation, Evidence, Git, and Verification.
- **Source:** [data-model.md §4](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/data-model.md), [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md), [`CORE-CONTRACT-010`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/feature-passport.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-013-01`
- **Security Impact:** `MEDIUM`
- **Verification Method:** `SCHEMA_VALIDATION`

### `REQ-PASS-002` — Stamping Gated Strictly by Convergence
- **Title:** Prohibition of Stamping Unverified Passports
- **Description:** Transition to `CONVERGED` status on a passport is prohibited unless verification converged (`dimensions.verification.converged == true`) and security passed (`gateway_verdict == "PASS"`).
- **Source:** [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md), `INV-003`
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-013-02`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `UNIT_TEST`

---

## 14. Evolution & Self-Improvement Domain

### `REQ-EVO-001` — Gated Evolution Pipeline
- **Title:** Multi-Stage Human-Approved Self-Improvement
- **Description:** All modifications to pipeline rules, prompts, or thresholds must follow the formal path: `Observation → Proposal → Evidence → Experiment → Evaluation → Human Approval → Versioned Change`.
- **Source:** [EVD-018](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md), `ARR-04`, `INV-004`
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-014-01`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `INTEGRATION_TEST`

### `REQ-EVO-002` — Prohibition of Autonomous Self-Evolution
- **Title:** Strict Ban on Unsandboxed Autonomous Mechanism Modification
- **Description:** Autonomous modification of the execution runtime or search space without human review is strictly prohibited. Unapproved mutation attempts must be blocked and logged as security violations.
- **Source:** [EVD-018](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [evolution.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/evolution.md), `ARR-04`
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-014-02`
- **Security Impact:** `CRITICAL`
- **Verification Method:** `UNIT_TEST`

---

## 15. Observability & Progress Domain

### `REQ-OBS-001` — Event-Derived Progress Reporting
- **Title:** Calculation of Progress Strictly from Evidence Logs
- **Description:** Project health and task progress must be derived strictly from verified event logs and Git hashes. Displaying optimistic agent-asserted scorecards without underlying machine evidence is forbidden.
- **Source:** [EVD-015](file:///home/juxnbernxrdo/Documentos/eidos/docs/research/evidence-registry.md), [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md), Constitution Art. IV
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-015-01`
- **Security Impact:** `MEDIUM`
- **Verification Method:** `UNIT_TEST`

### `REQ-OBS-002` — Comprehensive Operational Telemetry
- **Title:** Auditable Logging of System Decisions
- **Description:** Context routing selections, verification results, sandbox security checks, and task state transitions must emit structured telemetry to the event log.
- **Source:** [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md), [`EVENT-CONTRACT-001`](file:///home/juxnbernxrdo/Documentos/eidos/docs/contracts/event-log.md)
- **Priority:** `MUST`
- **Status:** `ACCEPTED`
- **Acceptance Criteria:** `AC-015-02`
- **Security Impact:** `HIGH`
- **Verification Method:** `UNIT_TEST`
