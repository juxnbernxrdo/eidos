# Phase 5 Implementation Handoff

**Status:** ACCEPTED  
**Origin Phase:** Phase 4 — Specifications (COMPLETED)  
**Destination Phase:** Phase 5 — Implementation (READY)  
**Authority:** Inter-Phase Engineering Handoff Protocol

---

## 1. The Implementation Boundary

Phase 4 has formally converted all architectural boundaries and contracts into **executable, unambiguous behavioral specifications**. 

When Phase 5 commences, developers will build the physical source modules strictly against these specifications:

```text
PHASE 4 (Specifications)                  PHASE 5 (Implementation)
Provides:                                 Executes:
- 15 Detailed Specifications              - Production Source Code in src/eidos/
- 35 Core Requirements                    - Component Implementations
- 35 Given/When/Then Acceptance Criteria  - Unit & Integration Test Implementations
- Canonical Invariant & Error Bindings    - Sandbox & Adapter Integration
- 3 Spec Schemas                          - Zero Architectural Reinterpretation
```

---

## 2. Ready for Implementation (15 Specifications)

All 15 specifications have passed the Phase 4 Quality Gate with status `ACCEPTED`:

1. [`SPEC-001-CORE-STATE`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-001-CORE-STATE.md) → Target: `src/eidos/core/state.py`
2. [`SPEC-002-PIPELINE`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-002-PIPELINE.md) → Target: `src/eidos/orchestration/pipeline.py`
3. [`SPEC-003-TASK`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-003-TASK.md) → Target: `src/eidos/orchestration/task.py`
4. [`SPEC-004-CONTEXT-ROUTER`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-004-CONTEXT-ROUTER.md) → Target: `src/eidos/context/router.py`
5. [`SPEC-005-GRAPH-STORE`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-005-GRAPH-STORE.md) → Target: `src/eidos/graph/engine.py`
6. [`SPEC-006-VERIFIER`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-006-VERIFIER.md) → Target: `src/eidos/verification/runner.py`
7. [`SPEC-007-EVENT-LOG`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-007-EVENT-LOG.md) → Target: `src/eidos/progress/logger.py`
8. [`SPEC-008-SECURITY-SANDBOX`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-008-SECURITY-SANDBOX.md) → Target: `src/eidos/security/supervisor.py`
9. [`SPEC-009-HARNESS-ADAPTER`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-009-HARNESS-ADAPTER.md) → Target: `src/eidos/harness/base.py`
10. [`SPEC-010-SUBAGENTS`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-010-SUBAGENTS.md) → Target: `src/eidos/agents/subagent.py`
11. [`SPEC-011-MEMORY-GATING`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-011-MEMORY-GATING.md) → Target: `src/eidos/memory/manager.py`
12. [`SPEC-012-SKILL-GATEWAY`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-012-SKILL-GATEWAY.md) → Target: `src/eidos/skills/gateway.py`
13. [`SPEC-013-FEATURE-PASSPORT`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-013-FEATURE-PASSPORT.md) → Target: `src/eidos/progress/passport.py`
14. [`SPEC-014-EVOLUTION-PIPELINE`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-014-EVOLUTION-PIPELINE.md) → Target: `src/eidos/evolution/pipeline.py`
15. [`SPEC-015-OBSERVABILITY-PROGRESS`](file:///home/juxnbernxrdo/Documentos/eidos/docs/specs/SPEC-015-OBSERVABILITY-PROGRESS.md) → Target: `src/eidos/progress/projector.py`

---

## 3. Blocked Specifications

- **Currently Blocked Specifications:** **NONE (0)**.
- All 15 core specifications are unblocked and ready for Phase 5 implementation.

---

## 4. Open Decisions to Preserve in Implementation

Phase 5 developers must implement the following parameters as **configurable settings with documented defaults**, without hardcoding assumptions:
- **`OPEN-DEC-001` (Repair Bound $K$)**: Configurable policy default $K = 5$ iterations.
- **`OPEN-DEC-002` (Skill Risk Cutoff)**: Configurable threshold $\text{risk} < 25$.
- **`OPEN-DEC-003` (Context Ranking)**: Default to topological hop proximity ($k=0, 1, 2$) in source order.
- **`OPEN-DEC-004` (Graph Storage Backend)**: Storage-agnostic engine; in-memory NetworkX with JSON snapshot default.
- **`OPEN-DEC-005` (Memory Opt-in)**: Persistent memory disabled by default (`opt_in_memory=false`).
- **`OPEN-DEC-006` (Invariant Enforcement Mode)**: Advisory-first checking pre-calibration (`ARR-02`).
- **`OPEN-DEC-007` (Autonomous Evolution)**: Strictly prohibited; changes require human proposal approval.

---

## 5. Implementation Dependencies & Technology Stack

- **Runtime**: Python 3.11+ (CPython 3.14 compatible, strict typing required per Constitution Art. VI).
- **Core Dependencies**:
  - `pydantic` v2 (for model validation).
  - `networkx` (for graph topology algorithms).
  - Python standard library (`json`, `ast`, `pathlib`, `re`, `fcntl` for atomic file locking).
- **Constitutional Limits**:
  - Zero external heavy dependencies if clean native code $< 150$ LOC is possible (Constitution Art. V).
  - Only OSI-approved permissive licenses (`MIT`, `Apache-2.0`, `BSD`).

---

## 6. Verification Requirements for Phase 6

Phase 6 will verify that Phase 5 implementations satisfy all 35 Acceptance Criteria:
- `AC-001-01` through `AC-015-02` defined in `docs/specs/traceability.md`.
- 100% pass rate on unit and integration suites.
- 0 type errors under `mypy/pyright` strict mode.
- 0 linter violations under `ruff`.
- 0 invariant violations under `eidos invariant check`.

---

## 7. Mandatory Security Requirements

1. **Default-Deny Policy-as-Physics**: All capability checks must fail closed (`PERMISSION_DENIED`).
2. **Path Confinement**: All file reads and writes must be resolved via `os.path.realpath` and verified inside the workspace root.
3. **Secret Blindness**: Secrets must never be stored in logs, tasks, passports, or context payloads.
4. **Sandboxed Subprocess Execution**: External tool commands and skill scripts must execute in isolated subprocesses with timeout and memory limits.

---

## 8. Stop Condition

Phase 4 is complete. In accordance with the stop condition, **Phase 5 must NOT be initialized automatically**.
