# Phase 3 — Contracts

Status: COMPLETED

Previous Phase:
Phase 2 — Architecture (COMPLETED)

Current Objective:
Formalize architectural boundaries into machine-readable and human-readable contracts.

Next Phase:
Phase 4 — Specifications

Forbidden Scope:
Implementation / full specifications / experimental validation / autonomous evolution

---

## 1. Context & Phase 2 Baseline Inputs

Phase 3 operates strictly upon the authoritative baseline established in Phase 2:
- **Foundational Architecture**: `docs/architecture/` (overview, principles, domains, components, boundaries, data-model, security, verification, evolution, progress, harness, context, graph, invariants)
- **Binding Decisions**: `docs/adr/P2-ADR-001` through `docs/adr/P2-ADR-008`
- **Readiness Map**: `docs/architecture/interface-contract-readiness.md`
- **Constitutional Governance**: `CONSTITUTION.md` and `AGENTS.md`
- **Research Traceability**: `docs/architecture/research-traceability.md` and `docs/research/evidence-registry.md`

Phase 2 established what boundaries exist and why. Phase 3 establishes what data and invariants cross those boundaries, how contracts are versioned, validated, and audited, and how they serve as binding constraints for Phase 4 specifications.

---

## 2. Expected Outputs of Phase 3

1. **Contract Governance Framework** (`docs/contracts/governance.md`):
   - Foundational contract principles, SemVer versioning policy, compatibility semantics, error taxonomy, epistemic provenance, security boundaries.
2. **Primary Boundary Contracts (Dual Plane: Markdown + JSON Schema Draft 2020-12)**:
   - `HarnessAdapter` (`docs/contracts/harness-adapter.md`, `schemas/contracts/harness/harness-adapter.schema.json`)
   - `ContextRouter` (`docs/contracts/context-router.md`, `schemas/contracts/context/context-router.schema.json`)
   - `GraphStore` (`docs/contracts/graph-store.md`, `schemas/contracts/graph/graph-store.schema.json`)
   - `Verifier` (`docs/contracts/verifier.md`, `schemas/contracts/verification/verifier.schema.json`)
   - `EventLog` (`docs/contracts/event-log.md`, `schemas/contracts/events/event-log.schema.json`)
3. **Core Architectural Contracts**:
   - `Project`, `Task`, `Agent`, `Session`, `Evidence`, `Finding`, `Artifact`, `Capability & Permission`, `Invariant`, `Feature Passport`.
4. **Architectural Invariants Formalization** (`docs/contracts/invariants.md`):
   - Machine-checkable invariant rules INV-001 through INV-006 with clear enforcement points.
5. **Contract Traceability & Registry**:
   - Traceability Matrix: `docs/contracts/traceability.md` (Research → Architecture → ADR → Contract → Spec Input).
   - Registry: `docs/contracts/registry.md` with active lifecycle states.
6. **Decision Log & Quality Gate**:
   - Contractual decisions in `docs/contracts/phase-3-decisions.md`.
   - Quality Gate review and checklist in `docs/contracts/phase-3-gate-review.md`.
   - Phase 4 handoff definition in `docs/contracts/phase-4-handoff.md`.
7. **Contract Test Suite**:
   - Automated schema syntax, constraint, serialization, and negative rejection tests under `tests/contracts/`.

---

## 3. Planned Contracts Inventory

| Contract ID | Domain | Name | Human Specification | Machine Schema |
|---|---|---|---|---|
| `HARN-CONTRACT-001` | Harness | HarnessAdapterContract | `docs/contracts/harness-adapter.md` | `schemas/contracts/harness/harness-adapter.schema.json` |
| `CTX-CONTRACT-001` | Context | ContextRouterContract | `docs/contracts/context-router.md` | `schemas/contracts/context/context-router.schema.json` |
| `GRAPH-CONTRACT-001` | Graph | GraphStoreContract | `docs/contracts/graph-store.md` | `schemas/contracts/graph/graph-store.schema.json` |
| `VERIF-CONTRACT-001` | Verification | VerifierContract | `docs/contracts/verifier.md` | `schemas/contracts/verification/verifier.schema.json` |
| `EVENT-CONTRACT-001` | Progress | EventLogContract | `docs/contracts/event-log.md` | `schemas/contracts/events/event-log.schema.json` |
| `CORE-CONTRACT-001` | Core | ProjectContract | `docs/contracts/core-contracts.md` | `schemas/contracts/core/project.schema.json` |
| `CORE-CONTRACT-002` | Core / Agents | TaskContract | `docs/contracts/core-contracts.md` | `schemas/contracts/core/task.schema.json` |
| `CORE-CONTRACT-003` | Agents | AgentContract | `docs/contracts/core-contracts.md` | `schemas/contracts/core/agent.schema.json` |
| `CORE-CONTRACT-004` | Orchestration | SessionContract | `docs/contracts/core-contracts.md` | `schemas/contracts/core/session.schema.json` |
| `CORE-CONTRACT-005` | Verification | EvidenceContract | `docs/contracts/core-contracts.md` | `schemas/contracts/core/evidence.schema.json` |
| `CORE-CONTRACT-006` | Verification | FindingContract | `docs/contracts/core-contracts.md` | `schemas/contracts/core/finding.schema.json` |
| `CORE-CONTRACT-007` | Execution | ArtifactContract | `docs/contracts/core-contracts.md` | `schemas/contracts/core/artifact.schema.json` |
| `CORE-CONTRACT-008` | Security | CapabilityPermissionContract | `docs/contracts/core-contracts.md` | `schemas/contracts/core/capability-permission.schema.json` |
| `CORE-CONTRACT-009` | Verification | InvariantContract | `docs/contracts/core-contracts.md` | `schemas/contracts/core/invariant.schema.json` |
| `CORE-CONTRACT-010` | Progress | FeaturePassportContract | `docs/contracts/feature-passport.md` | `schemas/contracts/core/feature-passport.schema.json` |

---

## 4. Open Decisions & Watchlist (Carried from Phase 2)

All items below remain open constants/thresholds (`DESIGN_CHOICE`), pending experimental validation in Phase 7:
- **ARR-01**: Memory is opt-in only; no autonomous cross-project writes.
- **ARR-02**: Invariants are advisory-first pre-calibration; blocking requires calibrated rules.
- **ARR-03**: Numerical constants (Repair limit $K=5$, risk score $<25$, delta-quality thresholds, graph hop $k \le 2$) remain DESIGN_CHOICE.
- **ARR-04**: Autonomous self-evolution is prohibited-by-default; changes require human approval.
- **ARR-05**: Literature evidence standards remain strict.

Contracts must represent these parameters as configurable or policy inputs, never hardcoding uncalibrated thresholds as immutable physical laws.

---

## 5. Dependencies and Risks

- **Dependency**: Strict schema validation without adding heavy dependencies beyond Python standard library and existing Pydantic v2.
- **Risk RSK-01 (Scope Creep)**: Accidentally drafting executable specs or implementation code in Phase 3. Mitigated by strict Quality Gate enforcing contract-only deliverables.
- **Risk RSK-04 (Harness Drift)**: Host adapters varying widely in trace fidelity. Mitigated by capability-dependent flags in `HarnessAdapterContract`.

---

## 6. Completion Criteria (Phase 3 Quality Gate)

Phase 3 transitions to `COMPLETED` when:
1. All 15 planned contracts have matching human-readable and machine-readable schema representations.
2. Dual-plane consistency is verified (no divergence between docs and schemas).
3. JSON Schemas are valid Draft 2020-12 documents and tested via automated pytest suite.
4. Error semantics, security boundaries, epistemic provenance, and versioning rules are fully formalized.
5. Traceability chain (EVD → P2-ADR → Boundary → Contract → Spec Input) is unbroken.
6. The Phase 3 Gate Review yields a `PASS`.
