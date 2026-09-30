# Eidos Specification Traceability Matrix

**Status:** ACCEPTED  
**Authority:** Canonical Phase 4 Traceability  
**Method:** Unbroken chain from Requirements (`REQ`) → Architectural Decisions (`P2-ADR`) → Contracts (`CONTRACT`) → Specifications (`SPEC`) → Acceptance Criteria (`AC`) → Phase 5 Target Modules → Phase 6 Verification Test Suites.

---

## 1. End-to-End Specification Traceability Table

| Requirement | Architectural Decision | Contract Dependency | Specification ID | Acceptance Criteria | Phase 5 Implementation Target | Phase 6 Verification Test Suite |
|---|---|---|---|---|---|---|
| `REQ-CORE-001` | `P2-ADR-007` | `EVENT-CONTRACT-001` | `SPEC-001-CORE-STATE` | `AC-001-01` | `src/eidos/core/state.py` | `tests/unit/test_core_state.py` |
| `REQ-CORE-002` | `P2-ADR-001` | `CORE-CONTRACT-002` | `SPEC-001-CORE-STATE` | `AC-001-02` | `src/eidos/core/state.py` | `tests/unit/test_core_state.py` |
| `REQ-PIPE-001` | `P2-ADR-001` | `CORE-CONTRACT-002` | `SPEC-002-PIPELINE` | `AC-002-01` | `src/eidos/orchestration/pipeline.py` | `tests/integration/test_pipeline.py` |
| `REQ-PIPE-002` | `P2-ADR-001` | `VERIF-CONTRACT-001` | `SPEC-002-PIPELINE` | `AC-002-02` | `src/eidos/orchestration/pipeline.py` | `tests/integration/test_pipeline.py` |
| `REQ-PIPE-003` | `P2-ADR-001` | `VERIF-CONTRACT-001` | `SPEC-002-PIPELINE` | `AC-002-03` | `src/eidos/orchestration/pipeline.py` | `tests/integration/test_pipeline.py` |
| `REQ-TASK-001` | `P2-ADR-003` | `CORE-CONTRACT-002` | `SPEC-003-TASK` | `AC-003-01` | `src/eidos/orchestration/task.py` | `tests/unit/test_task.py` |
| `REQ-TASK-002` | `P2-ADR-001` | `CORE-CONTRACT-002` | `SPEC-003-TASK` | `AC-003-02` | `src/eidos/orchestration/task.py` | `tests/unit/test_task.py` |
| `REQ-CTX-001` | `P2-ADR-002` | `CTX-CONTRACT-001` | `SPEC-004-CONTEXT-ROUTER` | `AC-004-01` | `src/eidos/context/router.py` | `tests/unit/test_context_router.py` |
| `REQ-CTX-002` | `P2-ADR-002` | `CTX-CONTRACT-001` | `SPEC-004-CONTEXT-ROUTER` | `AC-004-02` | `src/eidos/context/router.py` | `tests/unit/test_context_router.py` |
| `REQ-CTX-003` | `P2-ADR-002` | `CTX-CONTRACT-001` | `SPEC-004-CONTEXT-ROUTER` | `AC-004-03` | `src/eidos/context/router.py` | `tests/unit/test_context_router.py` |
| `REQ-GRAPH-001` | `P2-ADR-002` | `GRAPH-CONTRACT-001` | `SPEC-005-GRAPH-STORE` | `AC-005-01` | `src/eidos/graph/engine.py` | `tests/unit/test_graph_engine.py` |
| `REQ-GRAPH-002` | `P2-ADR-002` | `GRAPH-CONTRACT-001` | `SPEC-005-GRAPH-STORE` | `AC-005-02` | `src/eidos/graph/engine.py` | `tests/unit/test_graph_engine.py` |
| `REQ-GRAPH-003` | `P2-ADR-002` | `GRAPH-CONTRACT-001` | `SPEC-005-GRAPH-STORE` | `AC-005-03` | `src/eidos/graph/engine.py` | `tests/unit/test_graph_engine.py` |
| `REQ-VERIF-001` | `P2-ADR-001` | `VERIF-CONTRACT-001` | `SPEC-006-VERIFIER` | `AC-006-01` | `src/eidos/verification/runner.py` | `tests/integration/test_verifier.py` |
| `REQ-VERIF-002` | `P2-ADR-001` | `VERIF-CONTRACT-001` | `SPEC-006-VERIFIER` | `AC-006-02` | `src/eidos/verification/runner.py` | `tests/integration/test_verifier.py` |
| `REQ-VERIF-003` | `P2-ADR-001` | `VERIF-CONTRACT-001` | `SPEC-006-VERIFIER` | `AC-006-03` | `src/eidos/verification/runner.py` | `tests/integration/test_verifier.py` |
| `REQ-EVT-001` | `P2-ADR-007` | `EVENT-CONTRACT-001` | `SPEC-007-EVENT-LOG` | `AC-007-01` | `src/eidos/progress/logger.py` | `tests/unit/test_event_logger.py` |
| `REQ-EVT-002` | `P2-ADR-007` | `EVENT-CONTRACT-001` | `SPEC-007-EVENT-LOG` | `AC-007-02` | `src/eidos/progress/logger.py` | `tests/unit/test_event_logger.py` |
| `REQ-SEC-001` | `P2-ADR-006` | `CORE-CONTRACT-008` | `SPEC-008-SECURITY-SANDBOX` | `AC-008-01` | `src/eidos/security/supervisor.py` | `tests/security/test_sandbox.py` |
| `REQ-SEC-002` | `P2-ADR-006` | `CORE-CONTRACT-008` | `SPEC-008-SECURITY-SANDBOX` | `AC-008-02` | `src/eidos/security/supervisor.py` | `tests/security/test_sandbox.py` |
| `REQ-SEC-003` | `P2-ADR-006` | `CORE-CONTRACT-008` | `SPEC-008-SECURITY-SANDBOX` | `AC-008-03` | `src/eidos/security/supervisor.py` | `tests/security/test_sandbox.py` |
| `REQ-HARN-001` | `P2-ADR-005` | `HARN-CONTRACT-001` | `SPEC-009-HARNESS-ADAPTER` | `AC-009-01` | `src/eidos/harness/base.py` | `tests/harness/test_adapter.py` |
| `REQ-HARN-002` | `P2-ADR-005` | `HARN-CONTRACT-001` | `SPEC-009-HARNESS-ADAPTER` | `AC-009-02` | `src/eidos/harness/base.py` | `tests/harness/test_adapter.py` |
| `REQ-AGENT-001` | `P2-ADR-003` | `CORE-CONTRACT-003` | `SPEC-010-SUBAGENTS` | `AC-010-01` | `src/eidos/agents/subagent.py` | `tests/unit/test_subagents.py` |
| `REQ-AGENT-002` | `P2-ADR-003` | `CORE-CONTRACT-003` | `SPEC-010-SUBAGENTS` | `AC-010-02` | `src/eidos/agents/subagent.py` | `tests/unit/test_subagents.py` |
| `REQ-MEM-001` | `P2-ADR-004` | `CORE-CONTRACT-001` | `SPEC-011-MEMORY-GATING` | `AC-011-01` | `src/eidos/memory/manager.py` | `tests/unit/test_memory_gating.py` |
| `REQ-MEM-002` | `P2-ADR-004` | `CORE-CONTRACT-008` | `SPEC-011-MEMORY-GATING` | `AC-011-02` | `src/eidos/memory/manager.py` | `tests/unit/test_memory_gating.py` |
| `REQ-SKILL-001` | `P2-ADR-006` | `CORE-CONTRACT-008` | `SPEC-012-SKILL-GATEWAY` | `AC-012-01` | `src/eidos/skills/gateway.py` | `tests/security/test_skill_gateway.py` |
| `REQ-SKILL-002` | `P2-ADR-006` | `CORE-CONTRACT-008` | `SPEC-012-SKILL-GATEWAY` | `AC-012-02` | `src/eidos/skills/gateway.py` | `tests/security/test_skill_gateway.py` |
| `REQ-PASS-001` | `P2-ADR-007` | `CORE-CONTRACT-010` | `SPEC-013-FEATURE-PASSPORT` | `AC-013-01` | `src/eidos/progress/passport.py` | `tests/unit/test_passport.py` |
| `REQ-PASS-002` | `P2-ADR-007` | `CORE-CONTRACT-010` | `SPEC-013-FEATURE-PASSPORT` | `AC-013-02` | `src/eidos/progress/passport.py` | `tests/unit/test_passport.py` |
| `REQ-EVO-001` | `P2-ADR-007` | `CORE-CONTRACT-009` | `SPEC-014-EVOLUTION-PIPELINE` | `AC-014-01` | `src/eidos/evolution/pipeline.py` | `tests/integration/test_evolution.py` |
| `REQ-EVO-002` | `P2-ADR-007` | `CORE-CONTRACT-009` | `SPEC-014-EVOLUTION-PIPELINE` | `AC-014-02` | `src/eidos/evolution/pipeline.py` | `tests/integration/test_evolution.py` |
| `REQ-OBS-001` | `P2-ADR-007` | `EVENT-CONTRACT-001` | `SPEC-015-OBSERVABILITY-PROGRESS` | `AC-015-01` | `src/eidos/progress/projector.py` | `tests/unit/test_observability.py` |
| `REQ-OBS-002` | `P2-ADR-007` | `EVENT-CONTRACT-001` | `SPEC-015-OBSERVABILITY-PROGRESS` | `AC-015-02` | `src/eidos/progress/projector.py` | `tests/unit/test_observability.py` |

---

## 2. Integrity Audit
- 100% of requirements map to a recognized Phase 2 ADR.
- 100% of specifications reference a binding Phase 3 Contract.
- 100% of acceptance criteria have designated Phase 5 implementation targets and Phase 6 test suites.
