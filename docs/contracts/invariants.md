# Architectural & Contractual Invariants

**Status:** CONTRACT_BOUND (Advisory-First Pre-Calibration per ARR-02)  
**Authority:** Canonical Phase 3 Invariant Catalog  
**Constitutional Basis:** CONSTITUTION.md (Articles I, II, III, IV, IX)

---

## 1. Governance Policy for Invariants

Per **ARR-02** and constitutional mandates, invariants defined in Phase 3 are **CONTRACT_BOUND**. 
- They define formal compliance boundaries across all contracts and schemas.
- In Phase 3, invariant checks are **advisory-first** during experimental baselining to prevent false-block deadlocks before empirical calibration (Phase 6/7).
- No invariant may be silently violated without triggering an explicit `INVARIANT_VIOLATION` finding.

---

## 2. Invariants Catalog

### `INV-001` — Model-Provider & Harness Agnosticism
- **Description:** Core and contract schemas must never depend on any single model provider (Anthropic, OpenAI, Google) or execution harness. All interfaces must remain provider-neutral.
- **Scope:** Core runtime, contract schemas, pipeline state machine.
- **Enforcement Point:** Invariant AST scanner, dependency analyzer, contract validation.
- **Evidence Requirement:** Zero imports or references to provider-specific proprietary SDKs in `src/eidos/core/`.
- **Status:** `CONTRACT_BOUND`

### `INV-002` — Zero Cross-Project Leakage Without Explicit Authorization
- **Description:** No subagent, memory store, graph query, or harness adapter may access, leak, or merge data from outside the designated workspace root.
- **Scope:** Filesystem, GraphStore, ContextRouter, Memory, HarnessAdapter.
- **Enforcement Point:** SandboxSupervisor, ContextRouter security filter, Harness boundary check.
- **Evidence Requirement:** Path confinement audit log; zero cross-project node IDs in MSC payload.
- **Status:** `CONTRACT_BOUND`

### `INV-003` — Machine Decidability of Done (`IMPLEMENTED ≠ VERIFIED ≠ VALIDATED`)
- **Description:** Agent verbal claims (e.g. "task completed successfully") possess zero evidential weight. A task or feature transitions to `CONVERGED` if and only if all active verification layers pass with machine-verifiable evidence.
- **Scope:** Verifier, Orchestrator, Task Contract, Feature Passport.
- **Enforcement Point:** Verifier `verdict_payload`, Feature Passport stamping gate.
- **Evidence Requirement:** Passing `VerificationResult` containing zero test errors, zero type errors, zero linter violations, and zero blocking invariant violations.
- **Status:** `CONTRACT_BOUND`

### `INV-004` — Auditable Self-Improvement & Parameter Changes
- **Description:** Autonomous or semi-autonomous mutation of system rules, skills, prompts, or thresholds is strictly forbidden outside an auditable, sandboxed evolution protocol requiring human approval.
- **Scope:** Evolution pipeline, Skill Gateway, Governance rules.
- **Enforcement Point:** Evolution gate, EventLog append validator.
- **Evidence Requirement:** An approved `LearningProposal` with pre-registered experiment evidence refs.
- **Status:** `CONTRACT_BOUND`

### `INV-005` — Provenance Preservation Across Transformations
- **Description:** Epistemic status (`EXTRACTED`, `INFERRED`, `USER_CONFIRMED`, `AGENT_PROPOSED`) and confidence scores must accompany all knowledge claims, graph edges, and findings. Provenance cannot silently disappear during context assembly or pipeline transitions.
- **Scope:** ContextRouter, GraphStore, Evidence, Finding, EventLog.
- **Enforcement Point:** Schema validators for MSC payloads, graph snapshots, and events.
- **Evidence Requirement:** Every edge and assembled context item carries a valid `epistemic_provenance` tag.
- **Status:** `CONTRACT_BOUND`

### `INV-006` — Decision-to-Evidence Traceability
- **Description:** Every architectural commitment or contract specification must trace to empirical research evidence (EVD) or be explicitly classified as a `DESIGN_CHOICE`.
- **Scope:** Architecture documentation, ADRs, Contract specifications.
- **Enforcement Point:** Contract Quality Gate, ADR documentation review.
- **Evidence Requirement:** Valid citations to `docs/research/evidence-registry.md` or explicit `DESIGN_CHOICE` label.
- **Status:** `CONTRACT_BOUND`

### `INV-007` — Immutability of Event Log
- **Description:** Past records in `.eidos/progress/events.jsonl` are append-only and immutable. In-place modification, truncation, or deletion of historical events is strictly forbidden. Corrections require appending a `SUPERSEDING_CORRECTION` event.
- **Scope:** Progress domain, EventLog.
- **Enforcement Point:** EventLog file append handler, Git commit pre-commit hook.
- **Evidence Requirement:** Hash-chain continuity and monotonic sequence ordering of `event_id`s.
- **Status:** `CONTRACT_BOUND`

### `INV-008` — Policy-as-Physics Capability Confinement
- **Description:** Security cannot rely on natural language system prompt instructions. Tools, subagents, and skills must be constrained by OS-level or sandbox capability grants. Missing capability means `PERMISSION_DENIED`.
- **Scope:** Execution runtime, SandboxSupervisor, SkillGateway.
- **Enforcement Point:** CapabilityPermissionContract enforcement in execution sandbox.
- **Evidence Requirement:** Execution trace verifying denial of ungranted syscalls or unauthorized paths.
- **Status:** `CONTRACT_BOUND`

### `INV-009` — Epistemic Precedence (`EXTRACTED > INFERRED`)
- **Description:** An `INFERRED` edge or claim generated by an LLM can never overwrite, invalidate, or suppress a compiler/AST `EXTRACTED` ground-truth fact. Conflicting inferences are quarantined.
- **Scope:** GraphStore, ContextRouter MSC assembly.
- **Enforcement Point:** GraphStore edge conflict resolver, ContextRouter exclusion filter.
- **Evidence Requirement:** Graph snapshot records conflict as `CONFLICTS_WITH` with quarantined status.
- **Status:** `CONTRACT_BOUND`

### `INV-010` — Honesty in Validation Claims
- **Description:** No contract, component, or algorithm may be labeled `VALIDATED` or `PRODUCTION_READY` in the absence of replicated, statistically significant benchmark evidence (Constitution Honesty Axiom).
- **Scope:** Lifecycle metadata across all documents, contracts, and code.
- **Enforcement Point:** Contract Registry and Phase Gate review.
- **Evidence Requirement:** Link to completed Phase 7 `evaluation_run.json` with preregistered protocol.
- **Status:** `CONTRACT_BOUND`
