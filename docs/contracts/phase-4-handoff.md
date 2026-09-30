# Phase 4 Handoff Specification

**Status:** ACCEPTED  
**Origin Phase:** Phase 3 — Contracts  
**Destination Phase:** Phase 4 — Specifications  
**Authority:** Architectural Handoff Protocol

---

## 1. The Inter-Phase Boundary

Phase 3 established the contractual layer of Eidos: what data is exchanged, what schemas are enforced, what errors can be raised, what invariants must be preserved, and what capability boundaries are locked.

Phase 4 has a distinct, non-overlapping mandate:

```text
PHASE 3 (Contracts)                     PHASE 4 (Specifications)
Formalizes:                             Specifies:
- Boundaries & Schemas                  - Concrete Component Behaviors
- Data Structures & Types               - Execution Workflows & Sequences
- Permissible States & Errors           - Concrete Scenarios & Gherkin Flows
- Invariant Rule Declarations           - Acceptance Criteria & Edge Cases
- Fail-Closed Security Constraints      - Testable Behavioral Specs
```

---

## 2. Inventory of Handoff Artifacts Provided to Phase 4

Phase 4 receives the following frozen baselines as binding inputs:

1. **Foundational Architecture**:
   - `docs/architecture/` (overview, principles P1–P12, domains, components, data model, security, verification, progress, harness, context, graph, invariants)
   - Canonical ADRs: `docs/adr/P2-ADR-001` through `P2-ADR-008`
2. **Empirical Evidence & Literature**:
   - `docs/research/evidence-registry.md` (`EVD-001` through `EVD-020`)
   - `docs/research/sources.md` (`SRC-001` through `SRC-304`)
3. **Formal Contracts & Draft 2020-12 Schemas (15 Contracts)**:
   - Primary Boundaries: `HarnessAdapter`, `ContextRouter`, `GraphStore`, `Verifier`, `EventLog`
   - Core Entities: `Project`, `Task`, `Agent`, `Session`, `Evidence`, `Finding`, `Artifact`, `CapabilityPermission`, `Invariant`, `FeaturePassport`
   - Schema root: `schemas/contracts/`
4. **Contract Governance & Error Taxonomy**:
   - `docs/contracts/governance.md`
   - Canonical error codes: `INVALID_INPUT`, `UNSUPPORTED_CAPABILITY`, `PERMISSION_DENIED`, `CONTRACT_VIOLATION`, `RESOURCE_UNAVAILABLE`, `VERIFICATION_FAILED`, `PROVENANCE_INVALID`, `VERSION_MISMATCH`, `INVARIANT_VIOLATION`, `EXECUTION_TIMEOUT`
5. **Architectural & Contractual Invariants**:
   - `docs/contracts/invariants.md` (`INV-001` through `INV-010`)
6. **End-to-End Traceability**:
   - `docs/contracts/traceability.md` (Research → Architecture → ADR → Contract → Spec Input)
   - `docs/contracts/registry.md`
7. **Contract Test Suite**:
   - `tests/contracts/test_contract_schemas.py` and `src/eidos/contracts/validator.py`

---

## 3. Explicit Phase 4 Deliverables (To Be Produced in Phase 4)

When Phase 4 commences, it must specify (without implementing code):
- **Component Behavioral Specifications**: Step-by-step state machine execution, input parsing, error handling, and output emission.
- **Concrete Scenario Matrices**: Given-When-Then scenarios covering happy paths, edge cases, corrupted inputs, and failure cascades.
- **Harness Bridge Protocols**: Specific transport bindings (MCP stdio schemas, Claude Code hook payloads, Antigravity brain artifact structures).
- **Context Routing Algorithm Specification**: Exact token allocation rules and scoring heuristics satisfying the MSC contract.
- **Verification Runner Specification**: Concrete invocations of test suites, typecheckers, linters, and invariant checks.
- **Feature Passport SDD Artefacts**: Specification-driven development artifacts mapping directly to the 12 passport dimensions.

---

## 4. Strict Stop Condition

No Phase 4 work has been executed during Phase 3. The boundaries, schemas, and contracts are established and frozen as inputs for Phase 4.
