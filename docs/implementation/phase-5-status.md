# Phase 5 — Implementation

Status: COMPLETED

Previous Phase:
Phase 4 — Specifications (COMPLETED)

Current Objective:
Implement Eidos incrementally and traceably, utilizing Architecture + Contracts + Specifications as the source of truth, without reinterpreting decisions and without declaring the system VERIFIED or VALIDATED before Phase 6.

Next Phase:
Phase 6 — Verification (INITIALIZING)

Forbidden Scope:
- Reinterpreting architectural decisions silently
- Converting open hypotheses into factual assumptions
- Declaring the system `VALIDATED` or `VERIFIED`
- Running benchmark suites as proof of global efficacy
- Implementing un-audited autonomous self-evolution (`ARR-04`)
- Bypassing contracts or ignoring invariants
- Erasing previous engineering decision records
- Jumping to or initiating Phase 6 automatically

---

## 1. Engineering Chain & Authority Hierarchy

The binding chain of engineering authority in Eidos is:
```text
CONSTITUTION
    ↓
ARCHITECTURE
    ↓
ADR
    ↓
CONTRACT
    ↓
SPECIFICATION
    ↓
IMPLEMENTATION
```

Conflict Resolution Rules:
- **Specification vs Implementation**: Specification wins.
- **Contract vs Implementation**: Contract wins.
- **Architecture vs Implementation**: Architecture wins.
- **ADR vs Implementation**: ADR wins.
- **Specification vs Contract**: Cannot be resolved silently; must register `IMPLEMENTATION_BLOCKED_BY_CONTRACT_SPEC_CONFLICT` and escalate.

---

## 2. Implementation Boundaries & Operating Principles

1. **State Reducer Discipline**: State is strictly an event fold $S_t = \text{Fold}(S_0, [e_1 \dots e_t])$.
2. **Default-Deny Security**: All capabilities, tool executions, and file accesses fail closed.
3. **Pure Core Isolation**: Core logic has zero direct dependencies on CLI, outer harnesses, or network I/O (`ARCH-001`).
4. **Contract Schemas**: All data exchanges must conform to machine-checkable Draft 2020-12 schemas.
5. **Configurable Defaults**:
   - Repair iteration limit: $K = 5$ (`OPEN-DEC-001`)
   - Skill risk score cutoff: $\text{risk} < 25$ (`OPEN-DEC-002`)
   - Graph hop limit: $k \le 2$ (`OPEN-DEC-003`)
   - Persistent memory: disabled by default (`OPEN-DEC-005`)
   - Invariant enforcement: advisory-first pre-calibration (`OPEN-DEC-006`)

---

## 3. Implementation Slices

- **Slice 1**: Core Primitives, Typed Exceptions & Pure State Reducer (`SPEC-001`)
- **Slice 2**: Event Logging, Progress Projector & Feature Passport (`SPEC-007`, `SPEC-013`, `SPEC-015`)
- **Slice 3**: Security Sandbox, Permissions Supervisor & Path Confinement (`SPEC-008`)
- **Slice 4**: Repository Intelligence Graph Engine (`SPEC-005`)
- **Slice 5**: Context Router & Minimal Sufficient Context (MSC) (`SPEC-004`)
- **Slice 6**: 7-Layer Verification Runner & Traceback Capture (`SPEC-006`)
- **Slice 7**: Task & Pipeline Orchestration & Bounded Subagents (`SPEC-002`, `SPEC-003`, `SPEC-010`)
- **Slice 8**: Harness Adapters, Memory Gating, Skill Gateway & Evolution Pipeline (`SPEC-009`, `SPEC-011`, `SPEC-012`, `SPEC-014`)
- **Slice 9**: Master CLI Command Wiring & Diagnostic Battery
- **Slice 10**: Phase 5 Quality Gate Review & Phase 6 Handoff

---

## 4. Phase 5 Completion Criteria

1. All 15 specifications implemented in `src/eidos/`.
2. Unit and integration test suites covering all acceptance criteria (`AC-001-01` through `AC-015-02`).
3. 100% test pass rate with zero invariant violations (`eidos invariant check`).
4. Zero un-audited dependencies, zero architectural drift.
5. Implementation matrix, blockers report, deviations record, and gate review finalized.
