# Phase 4 — Specifications

Status: COMPLETED

Previous Phase:
Phase 3 — Contracts (COMPLETED)

Current Objective:
Transform contracts, architectural decisions, and requirements into precise, traceable, and executable specifications.

Next Phase:
Phase 5 — Implementation

Forbidden Scope:
Writing production code / building functional adapters / implementing memory or graph engines / experimental validation / autonomous evolution / starting Phase 5

---

## 1. Inputs from Phase 3

Phase 4 builds strictly upon the frozen, verified baselines established in earlier phases:
- **Phase 1 Research**: `docs/research/evidence-registry.md` (`EVD-001` through `EVD-020`) and `docs/research/sources.md`
- **Phase 2 Architecture**: `docs/architecture/` (principles, components, domains, data model, security, verification, progress, harness, context, graph, invariants) and binding ADRs (`docs/adr/P2-ADR-001` through `P2-ADR-008`)
- **Phase 3 Contracts & Schemas**: 15 formal contracts (`HARN-CONTRACT-001`, `CTX-CONTRACT-001`, `GRAPH-CONTRACT-001`, `VERIF-CONTRACT-001`, `EVENT-CONTRACT-001`, `CORE-CONTRACT-001` through `CORE-CONTRACT-010`) and Draft 2020-12 schemas under `schemas/contracts/`
- **Constitutional Governance**: `CONSTITUTION.md` and `AGENTS.md`
- **Contract Traceability & Handoff**: `docs/contracts/traceability.md` and `docs/contracts/phase-4-handoff.md`

---

## 2. Expected Outputs of Phase 4

1. **Specification Governance Framework** (`docs/specs/governance.md`):
   - Definitional boundaries (what a spec is/is not), lifecycle states, standard 22-section template, Given/When/Then scenario standards, ID naming conventions.
2. **Requirements Model**:
   - Comprehensive, explicit catalog of requirements (`REQ-001` through `REQ-035+`) across all system domains with priority, security impact, and verification methods.
3. **Core Behavioral Specifications** (`docs/specs/SPEC-*.md`):
   - `SPEC-001`: Core State Reducer ($S_t = \text{Fold}(S_0, [e_1 \dots e_t])$)
   - `SPEC-002`: Phased Orchestration Pipeline (Discovery → Converge)
   - `SPEC-003`: Task Lifecycle & Bounded Transitions
   - `SPEC-004`: Context Router & Minimal Sufficient Context (MSC)
   - `SPEC-005`: Storage-Agnostic Repository Graph Engine
   - `SPEC-006`: 7-Layer Verification Runner & Bounded Repair Loop
   - `SPEC-007`: Append-Only Event Log & Git HEAD Anchoring
   - `SPEC-008`: Security Boundaries, Capability Sandbox & Path Isolation
   - `SPEC-009`: Host Harness Adapters & Trace Streaming
   - `SPEC-010`: Contract-Bounded Subagents & CodeAct Execution
   - `SPEC-011`: Tripartite Memory Boundaries & Opt-in Admission Gates
   - `SPEC-012`: Skill Gateway, Static AST/YARA Auditing & Lock Pinning
   - `SPEC-013`: Feature Passport 12-Dimensional Convergence Bridge
   - `SPEC-014`: Gated Evolution & Self-Improvement Pipeline
   - `SPEC-015`: Event-Derived Progress & Observability
4. **Open Specification Decisions** (`docs/specs/open-specification-decisions.md`):
   - Rigorous catalog of open constants, uncalibrated thresholds, and experimental parameters (`ARR-01` through `ARR-05`).
5. **End-to-End Specification Traceability Matrix** (`docs/specs/traceability.md`):
   - `REQ` → `ADR` → `CONTRACT` → `SPEC` → `ACCEPTANCE CRITERIA` → `PHASE 5 TARGET` → `PHASE 6 TEST`.
6. **Machine-Readable Specification Schemas** (`schemas/specs/`):
   - Structural JSON Schemas defining the machine representation of requirements, specifications, and scenarios.
7. **Specification Consistency Suite** (`tests/specs/test_spec_consistency.py`):
   - Automated tests ensuring zero orphan requirements, zero broken contract links, unique IDs, complete acceptance criteria, and zero contradictions.
8. **Phase 5 Implementation Handoff & Quality Gate Review**:
   - `docs/specs/phase-5-handoff.md` and `docs/specs/phase-4-gate-review.md`.

---

## 3. Scope & Non-Goals

### In Scope:
- Defining observable component behaviors.
- Formulating unambiguous Given/When/Then acceptance criteria.
- Specifying operational invariants and preconditions/postconditions.
- Mapping failure semantics, edge cases, and escalation criteria.
- Defining exact inputs, outputs, and state transitions.

### Non-Goals (Strictly Forbidden in Phase 4):
- Writing production feature implementations or algorithms.
- Modifying core runtime code in `src/eidos/core/`.
- Creating functional harness adapters or graph database bindings.
- Resolving open empirical research questions or constants ($K$, thresholds) artificially.
- Declaring features `VALIDATED` without replicated Phase 7 benchmark runs.

---

## 4. Dependencies & Risks

- **Risk RSK-01 (Premature Implementation)**: Temptation to write Python implementation code in specifications. Mitigated by strict adherence to behavioral requirements (Given/When/Then) and Phase 4 Quality Gate review.
- **Risk RSK-07 (Specification Friction vs Grounding)**: Specifications becoming disconnected from Phase 3 contracts. Mitigated by automated consistency tests cross-referencing all 15 contract IDs and schemas.
- **Risk (Artificial Closure of Constants)**: Hardcoding uncalibrated thresholds ($K=5$, risk $<25$). Mitigated by marking them as open `DESIGN_CHOICE` parameters with fallback defaults.

---

## 5. Completion Criteria (Phase 4 Quality Gate)

Phase 4 transitions to `COMPLETED` when:
1. All 15 planned specifications are authored adhering to the 22-section standard template.
2. Every specification is backed by explicit source requirements (`REQ-XXX`), architectural decisions (`P2-ADR-XXX`), and contracts.
3. Every specification defines machine-checkable acceptance criteria (`AC-XXX`) in Given/When/Then format.
4. The specification consistency test suite runs cleanly and passes 100%.
5. The traceability matrix is complete from Research through Phase 6 test targets.
6. The Phase 4 Gate Review records a unanimous `PASS`.
