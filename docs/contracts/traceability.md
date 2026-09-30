# Eidos Contract Traceability Matrix

**Status:** ACCEPTED  
**Authority:** Canonical Phase 3 Contract Traceability  
**Method:** End-to-end chain from Research Evidence (Phase 1) through Architectural Decisions (Phase 2), Boundary Interfaces, Contracts (Phase 3), and Specification Hand-offs (Phase 4).

---

## 1. Traceability Chain Overview

```text
Research Evidence (EVD)
       ↓
Architectural Decision (P2-ADR)
       ↓
Architectural Boundary
       ↓
Contract (Phase 3)
       ↓
Specification Target (Phase 4)
```

---

## 2. End-to-End Contract Traceability Table

| Research Evidence | Architectural Decision | Boundary Component | Contract ID | Contract Name | Phase 4 Specification Input | Epistemic Status |
|---|---|---|---|---|---|---|
| `EVD-001`, `EVD-002`, `SRC-105` | `P2-ADR-005` | HarnessAdapter | `HARN-CONTRACT-001` | HarnessAdapterContract | `SPEC-HARNESS-BRIDGES` | `PARTIALLY_SUPPORTED` |
| `EVD-003`, `EVD-016` | `P2-ADR-002` | ContextRouter | `CTX-CONTRACT-001` | ContextRouterContract | `SPEC-CONTEXT-ROUTER` | `SUPPORTED` |
| `EVD-005`, `EVD-013` | `P2-ADR-002` | GraphStore | `GRAPH-CONTRACT-001` | GraphStoreContract | `SPEC-GRAPH-STORE` | `SUPPORTED` |
| `EVD-009`, `EVD-012`, `EVD-015` | `P2-ADR-001` | Verifier | `VERIF-CONTRACT-001` | VerifierContract | `SPEC-VERIFICATION-RUNNER` | `PARTIALLY_SUPPORTED` |
| `EVD-015`, `SRC-005` | `P2-ADR-007` | EventLog | `EVENT-CONTRACT-001` | EventLogContract | `SPEC-EVENT-LOGGER` | `DESIGN_CHOICE` |
| `EVD-002`, `EVD-001` | `P2-ADR-008` | Project Core | `CORE-CONTRACT-001` | ProjectContract | `SPEC-CORE-CONFIG` | `DESIGN_CHOICE` |
| `EVD-004`, `EVD-006` | `P2-ADR-003` | Task Orchestration | `CORE-CONTRACT-002` | TaskContract | `SPEC-SUBAGENT-RUNNER` | `PARTIALLY_SUPPORTED` |
| `EVD-004`, `EVD-006` | `P2-ADR-003` | Subagent Runtime | `CORE-CONTRACT-003` | AgentContract | `SPEC-SUBAGENT-RUNNER` | `PARTIALLY_SUPPORTED` |
| `EVD-001`, `EVD-004` | `P2-ADR-001` | Session Accounting | `CORE-CONTRACT-004` | SessionContract | `SPEC-SESSION-MANAGER` | `DESIGN_CHOICE` |
| `EVD-009`, `EVD-015` | `P2-ADR-001` | Evidence Anchor | `CORE-CONTRACT-005` | EvidenceContract | `SPEC-VERIFICATION-RUNNER` | `PARTIALLY_SUPPORTED` |
| `EVD-009`, `EVD-012` | `P2-ADR-001` | Diagnostic Findings | `CORE-CONTRACT-006` | FindingContract | `SPEC-INVARIANT-ENGINE` | `SUPPORTED` |
| `EVD-002`, `EVD-009` | `P2-ADR-001` | Artifact Tracker | `CORE-CONTRACT-007` | ArtifactContract | `SPEC-EXECUTION-SANDBOX` | `DESIGN_CHOICE` |
| `EVD-007`, `EVD-008` | `P2-ADR-006` | Security Gateway | `CORE-CONTRACT-008` | CapabilityPermissionContract | `SPEC-SANDBOX-POLICY` | `PARTIALLY_SUPPORTED` |
| `EVD-012`, `P1-P12` | `P2-ADR-001` | Invariant Checker | `CORE-CONTRACT-009` | InvariantContract | `SPEC-INVARIANT-ENGINE` | `RESEARCH_HYPOTHESIS` |
| `EVD-015`, `EVD-018` | `P2-ADR-007` | Feature Passport | `CORE-CONTRACT-010` | FeaturePassportContract | `SPEC-FEATURE-PASSPORT` | `DESIGN_CHOICE` |

---

## 3. Epistemic Integrity Audit

- Zero synthetic or hallucinated IDs: all cited `EVD-XXX` exist in `docs/research/evidence-registry.md`.
- Zero unratified ADR references: all cited `P2-ADR-XXX` exist in `docs/adr/`.
- All contracts specify their exact Phase 4 specification consumption destination.
