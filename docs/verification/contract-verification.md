# Contract Verification Report (Level 4)

**Status:** PASS  
**Authority:** Phase 3 Formal Contracts & JSON Schema Draft 2020-12  
**Scope:** 15 Formal Contracts  

---

## 1. Contract Conformance Summary

Every formal contract defined in Phase 3 was verified against its corresponding Draft 2020-12 schema using automated validation in [`tests/contracts/test_contract_schemas.py`](file:///home/juxnbernxrdo/Documentos/eidos/tests/contracts/test_contract_schemas.py) and [`src/eidos/contracts/validator.py`](file:///home/juxnbernxrdo/Documentos/eidos/src/eidos/contracts/validator.py):

| Contract ID | Contract Title | Bound Schema Path | Implementing Module | Inputs & Preconditions | Outputs & Postconditions | Error Semantics | Verdict |
|:---|:---|:---|:---|:---|:---|:---:|:---:|
| `HARN-CONTRACT-001` | Harness Adapter Contract | `schemas/contracts/harness/harness-adapter.schema.json` | `src/eidos/harness/` | Valid task, context, and permissions | Execution ID, unified patch, observation trace | `UNSUPPORTED_CAPABILITY` | **PASS** |
| `CTX-CONTRACT-001` | Context Router Contract | `schemas/contracts/context/context-router.schema.json` | `src/eidos/context/router.py` | Task, target files, budget, project ID | MSC payload, selection audit, pinned contracts | `INVALID_INPUT`, budget exhaustion | **PASS** |
| `GRAPH-CONTRACT-001` | Graph Store Contract | `schemas/contracts/graph/graph-store.schema.json` | `src/eidos/graph/engine.py` | Source files, AST parse, Git commit | 21 nodes, 11 edges, JSON snapshot | Quarantined `CONFLICTS_WITH` | **PASS** |
| `VERIF-CONTRACT-001` | Verifier Contract | `schemas/contracts/verification/verifier.schema.json` | `src/eidos/verification/runner.py` | Workspace, active layers, attempt count | Verdict, layer results, oracle trace | `VERIFICATION_FAILED` | **PASS** |
| `EVENT-CONTRACT-001` | Event Log Contract | `schemas/contracts/events/event-log.schema.json` | `src/eidos/progress/logger.py` | Event type, actor, payload, Git commit | Append-only record, monotonic event ID | `RESOURCE_UNAVAILABLE` | **PASS** |
| `CORE-CONTRACT-001` | Project Contract | `schemas/contracts/core/project.schema.json` | `src/eidos/contracts/models.py` | Project ID, harness, doc language | `.eidos/project.json` | `CONFIGURATION_ERROR` | **PASS** |
| `CORE-CONTRACT-002` | Task Contract | `schemas/contracts/core/task.schema.json` | `src/eidos/orchestration/task.py` | Objective, target files, allowed tools | 10-state lifecycle, transition evidence | `CONTRACT_VIOLATION` | **PASS** |
| `CORE-CONTRACT-003` | Agent Contract | `schemas/contracts/core/agent.schema.json` | `src/eidos/agents/subagent.py` | Role, model, capabilities, max turns | Execution output, CodeAct traceback | `EXECUTION_TIMEOUT` | **PASS** |
| `CORE-CONTRACT-004` | Skill Contract | `schemas/contracts/core/skill.schema.json` | `src/eidos/skills/gateway.py` | Skill package, scripts, YAML meta | Audited package, `skills-lock.json` | `PERMISSION_DENIED` | **PASS** |
| `CORE-CONTRACT-005` | Evidence Contract | `schemas/contracts/core/evidence.schema.json` | `src/eidos/contracts/models.py` | Claim, source file, command, stdout | Verified evidence record | `PROVENANCE_ERROR` | **PASS** |
| `CORE-CONTRACT-006` | Finding Contract | `schemas/contracts/core/finding.schema.json` | `src/eidos/contracts/models.py` | Rule ID, severity, message, file, line | Structured finding record | `INVARIANT_VIOLATION` | **PASS** |
| `CORE-CONTRACT-007` | Session Contract | `schemas/contracts/core/session.schema.json` | `src/eidos/core/state.py` | Session ID, operator, token budget | Aggregated session progress | `INVALID_INPUT` | **PASS** |
| `CORE-CONTRACT-008` | Capability Permission Contract | `schemas/contracts/core/capability-permission.schema.json` | `src/eidos/security/permissions.py` | Subject, filesystem scope, network, exec | Capability grant record | `PERMISSION_DENIED` | **PASS** |
| `CORE-CONTRACT-009` | Invariant Contract | `schemas/contracts/core/invariant.schema.json` | `src/eidos/intelligence/invariants.py` | Invariant ID, severity, forbidden imports | AST audit report | `INVARIANT_VIOLATION` | **PASS** |
| `CORE-CONTRACT-010` | Feature Passport Contract | `schemas/contracts/core/feature-passport.schema.json` | `src/eidos/progress/passport.py` | 12 formal dimensions, verification result | Stamped passport JSON | `VERIFICATION_FAILED` | **PASS** |

---

## 2. Evidence Artifacts
- **Schema Validation Suite**: [`tests/contracts/test_contract_schemas.py`](file:///home/juxnbernxrdo/Documentos/eidos/tests/contracts/test_contract_schemas.py) (12 tests passed).
- **Core Contract Models**: [`tests/test_contracts.py`](file:///home/juxnbernxrdo/Documentos/eidos/tests/test_contracts.py) (4 tests passed).
- **Overall Contract Compliance**: **100% (15/15 Contracts Verified)**.
