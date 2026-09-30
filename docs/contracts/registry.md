# Eidos Contract Registry

**Status:** LIVING (Phase 3 Baseline)  
**Authority:** Canonical Contract Inventory  
**Permissible States:** `DRAFT` / `REVIEW` / `ACCEPTED` / `DEPRECATED` / `SUPERSEDED`

---

## 1. Registered Contracts

| Contract ID | Name | Version | Status | Owner Domain | Schema | Architecture Basis | Phase 4 Input |
|---|---|---|---|---|---|---|---|
| `HARN-CONTRACT-001` | HarnessAdapterContract | `1.0.0` | `ACCEPTED` | Harness | `schemas/contracts/harness/harness-adapter.schema.json` | `P2-ADR-005`, `harness.md` | `SPEC-HARNESS-BRIDGES` |
| `CTX-CONTRACT-001` | ContextRouterContract | `1.0.0` | `ACCEPTED` | Context | `schemas/contracts/context/context-router.schema.json` | `P2-ADR-002`, `context.md` | `SPEC-CONTEXT-ROUTER` |
| `GRAPH-CONTRACT-001` | GraphStoreContract | `1.0.0` | `ACCEPTED` | Graph | `schemas/contracts/graph/graph-store.schema.json` | `P2-ADR-002`, `graph.md` | `SPEC-GRAPH-STORE` |
| `VERIF-CONTRACT-001` | VerifierContract | `1.0.0` | `ACCEPTED` | Verification | `schemas/contracts/verification/verifier.schema.json` | `P2-ADR-001`, `verification.md` | `SPEC-VERIFICATION-RUNNER` |
| `EVENT-CONTRACT-001` | EventLogContract | `1.0.0` | `ACCEPTED` | Progress | `schemas/contracts/events/event-log.schema.json` | `P2-ADR-007`, `progress.md` | `SPEC-EVENT-LOGGER` |
| `CORE-CONTRACT-001` | ProjectContract | `1.0.0` | `ACCEPTED` | Core | `schemas/contracts/core/project.schema.json` | `P2-ADR-008`, `domains.md` | `SPEC-CORE-CONFIG` |
| `CORE-CONTRACT-002` | TaskContract | `1.0.0` | `ACCEPTED` | Core / Agents | `schemas/contracts/core/task.schema.json` | `P2-ADR-003`, `agents.md` | `SPEC-SUBAGENT-RUNNER` |
| `CORE-CONTRACT-003` | AgentContract | `1.0.0` | `ACCEPTED` | Agents | `schemas/contracts/core/agent.schema.json` | `P2-ADR-003`, `agents.md` | `SPEC-SUBAGENT-RUNNER` |
| `CORE-CONTRACT-004` | SessionContract | `1.0.0` | `ACCEPTED` | Orchestration | `schemas/contracts/core/session.schema.json` | `P2-ADR-001`, `progress.md` | `SPEC-SESSION-MANAGER` |
| `CORE-CONTRACT-005` | EvidenceContract | `1.0.0` | `ACCEPTED` | Verification | `schemas/contracts/core/evidence.schema.json` | `P2-ADR-001`, `data-model.md` | `SPEC-VERIFICATION-RUNNER` |
| `CORE-CONTRACT-006` | FindingContract | `1.0.0` | `ACCEPTED` | Verification | `schemas/contracts/core/finding.schema.json` | `P2-ADR-001`, `data-model.md` | `SPEC-INVARIANT-ENGINE` |
| `CORE-CONTRACT-007` | ArtifactContract | `1.0.0` | `ACCEPTED` | Execution | `schemas/contracts/core/artifact.schema.json` | `P2-ADR-001`, `data-model.md` | `SPEC-EXECUTION-SANDBOX` |
| `CORE-CONTRACT-008` | CapabilityPermissionContract | `1.0.0` | `ACCEPTED` | Security | `schemas/contracts/core/capability-permission.schema.json` | `P2-ADR-006`, `security.md` | `SPEC-SANDBOX-POLICY` |
| `CORE-CONTRACT-009` | InvariantContract | `1.0.0` | `ACCEPTED` | Verification | `schemas/contracts/core/invariant.schema.json` | `P2-ADR-001`, `invariants.md` | `SPEC-INVARIANT-ENGINE` |
| `CORE-CONTRACT-010` | FeaturePassportContract | `1.0.0` | `ACCEPTED` | Progress | `schemas/contracts/core/feature-passport.schema.json` | `P2-ADR-007`, `data-model.md` | `SPEC-FEATURE-PASSPORT` |

---

## 2. Integrity Rules

1. Every contract listed above has a matching JSON Schema under `schemas/contracts/` and a corresponding human specification under `docs/contracts/`.
2. No contract is marked `VALIDATED` or `PRODUCTION_READY` (Constitution Honesty Axiom).
3. Any future contract additions must follow the Phase 3 Quality Gate before being registered.
