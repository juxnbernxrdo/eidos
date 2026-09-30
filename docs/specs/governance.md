# Eidos Specification Governance Framework

**Status:** ACCEPTED  
**Version:** 1.0.0  
**Authority:** Canonical Phase 4 Specification Governance  
**Constitutional Basis:** CONSTITUTION.md (Articles I, II, III, IV, VI, VII, IX)

---

## 1. Definitional Boundaries: What a Specification Is and Is Not

To prevent semantic conflation across project phases, Eidos enforces strict distinctions across the engineering lifecycle:

```text
Requirement (Phase 1/4)   ──► Defines WHAT need exists and WHY.
Architecture (Phase 2)    ──► Defines WHAT system boundaries exist and WHY.
Contract (Phase 3)        ──► Defines WHAT data and invariants cross those boundaries.
Specification (Phase 4)   ──► Defines HOW each capability behaves under all scenarios.
Implementation (Phase 5)  ──► Realizes the specification in physical source code.
Verification (Phase 6)    ──► Machine-checks that code satisfies the specification.
Validation (Phase 7)      ──► Replicates empirical efficacy on controlled benchmarks.
```

### What a Specification IS:
- A precise, deterministic, observable description of component behavior.
- An unambiguous translation of architecture and contracts into testable scenarios.
- A complete catalog of preconditions, state transitions, postconditions, and failure modes.
- A machine-checkable contract for Phase 5 developers: satisfying the spec guarantees satisfying the architecture.

### What a Specification IS NOT:
- A specification is **not** Python code or executable script logic.
- A specification is **not** an architecture proposal (it cannot invent new boundaries).
- A specification is **not** a benchmark validation claim.
- A specification is **not** an open ReAct prompt loop.

---

## 2. Specification Lifecycle States

Specifications progress through seven distinct, audited states:

```text
  [ DRAFT ] ────────► [ REVIEW ] ────────► [ ACCEPTED ]
                                                 │
                                                 ├───► [ IMPLEMENTED ] (Phase 5)
                                                 │           │
                                                 │           ▼
                                                 │     [ VERIFIED ] (Phase 6)
                                                 │
                                                 ├───► [ SUPERSEDED ]
                                                 │
                                                 └───► [ DEPRECATED ]
```

1. **`DRAFT`**: Initial authoring; requirements and scenarios being drafted.
2. **`REVIEW`**: Complete specification undergoing consistency and quality review.
3. **`ACCEPTED`**: Approved binding specification ready for Phase 5 implementation.
4. **`IMPLEMENTED`**: Fully implemented in code during Phase 5.
5. **`VERIFIED`**: Validated by automated tests during Phase 6.
6. **`SUPERSEDED`**: Replaced by a newer specification version.
7. **`DEPRECATED`**: Scheduled for phase-out; no longer actively maintained.

*Rule:* The state `VALIDATED` is prohibited in Phase 4. Empirical validation belongs strictly to Phase 7 benchmarks (Constitution Honesty Axiom).

---

## 3. Identification & Naming Conventions

All identifiers across specifications must adhere to the standard prefix taxonomy:

| Entity Prefix | Pattern | Purpose | Example |
|---|---|---|---|
| **Requirement** | `REQ-[DOMAIN]-[0-9]{3}` | Atomic, verifiable system requirement | `REQ-CORE-001` |
| **Specification** | `SPEC-[0-9]{3}-[NAME]` | Complete capability specification | `SPEC-001-CORE-STATE` |
| **Acceptance Criteria** | `AC-[SPEC_NUM]-[0-9]{2}` | Machine-decidable Given/When/Then test | `AC-001-01` |
| **Scenario** | `SCENARIO-[SPEC_NUM]-[0-9]{2}` | Concrete execution scenario or edge flow | `SCENARIO-001-01` |
| **Invariant** | `INV-[0-9]{3}` | Binding architectural rule | `INV-001` |

---

## 4. Standard Specification Structure (22 Mandatory Sections)

Every specification file in Eidos must strictly implement the following 22 sections:

```markdown
# SPEC-XXX — [Name]

## 1. Status
## 2. Purpose
## 3. Scope
## 4. Non-Goals
## 5. Source Requirements
## 6. Architectural Basis
## 7. Contract Dependencies
## 8. Behavioral Requirements
## 9. Inputs
## 10. Outputs
## 11. State Model
## 12. Invariants
## 13. Preconditions
## 14. Postconditions
## 15. Failure Semantics
## 16. Security Requirements
## 17. Observability Requirements
## 18. Edge Cases
## 19. Acceptance Criteria
## 20. Verification Strategy
## 21. Traceability
## 22. Open Questions & Phase 5 Notes
```

---

## 5. Requirement Model

All source requirements must be formally registered with the following attributes:

```text
REQ-ID: [Unique Identifier]
Title: [Concise noun phrase]
Description: [Precise observable description of what the system must perform]
Source: [EVD-XXX / P2-ADR-XXX / CONTRACT-XXX / Constitution Article]
Priority: [MUST | SHOULD | MAY]
Status: [DRAFT | REVIEW | ACCEPTED]
Acceptance Criteria: [Reference to AC-XXX]
Security Impact: [CRITICAL | HIGH | MEDIUM | LOW | NONE]
Verification Method: [UNIT_TEST | INTEGRATION_TEST | INVARIANT_CHECK | SCHEMA_VALIDATION]
```

### Priority Definitions (RFC 2119):
- **`MUST`**: Absolute requirement; non-negotiable for system correctness or security.
- **`SHOULD`**: Strongly recommended; valid architectural exceptions must be documented.
- **`MAY`**: Truly optional capability or configurable extension.

---

## 6. Behavioral Specification Format (Given / When / Then)

All behavioral specifications and acceptance criteria must be expressed in structured **Given / When / Then** format:

```gherkin
Given [Initial state, preconditions, and active capability grants]
When  [Concrete action, trigger, or event occurs]
Then  [Deterministic, observable result, state transition, and evidence emitted]
```

### Prohibited Language:
Vague, unobservable, or non-deterministic assertions are strictly prohibited in acceptance criteria:
- *Prohibited:* "Must be fast", "Should work reliably", "Must use AI effectively".
- *Mandatory:* "Response time must be $\le 500\text{ms}$", "Must emit exit code 0", "Must raise typed `PERMISSION_DENIED` error".

---

## 7. Change Management & Consistency Governance

1. **No Silent Changes**: A specification cannot contradict an approved Phase 2 ADR or Phase 3 Contract.
2. **Conflict Resolution (`SPECIFICATION_CONFLICT`)**: If a specification uncovers an architectural oversight or contract gap, a `SPECIFICATION_CONFLICT` must be recorded. Resolution requires an explicit ADR amendment or Contract version bump.
3. **Traceability Guarantee**: Every requirement must be linked to at least one acceptance criterion and targeted for verification in Phase 6.
