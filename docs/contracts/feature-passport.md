# Feature Passport Contract (`CORE-CONTRACT-010`)

**Contract ID:** `CORE-CONTRACT-010`  
**Version:** 1.0.0  
**Status:** ACCEPTED  
**Owner Domain:** Progress / Governance  
**Machine Schema:** [`feature-passport.schema.json`](file:///home/juxnbernxrdo/Documentos/eidos/schemas/contracts/core/feature-passport.schema.json)  
**Architecture Basis:** [data-model.md §4](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/data-model.md), [progress.md](file:///home/juxnbernxrdo/Documentos/eidos/docs/architecture/progress.md), [P2-ADR-007](file:///home/juxnbernxrdo/Documentos/eidos/docs/adr/P2-ADR-007-progress-passports-evolution.md)

---

## 1. Purpose & Inter-Phase Traceability Role

The `FeaturePassport` contract establishes the formal convergence certificate for a feature.

### Phase 3 Scope Clarification:
> In Phase 3, the Feature Passport is **NOT an implemented runtime engine**. This contract formalizes the **minimal data boundary** required to connect requirements, architecture, contracts, implementation, and verification across lifecycle phases.

```text
Requirement (REQ) ──► Spec (SPEC) ──► Architecture (Graph) ──► Contracts
         ▲                                                         │
         │                   Feature Passport                      ▼
         │           ┌─────────────────────────────┐        Implementation
         └───────────┤   12-Dimensional Bridge     │◄──────────────┘
                     │    Stamped on CONVERGE      │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                         Verification & Evidence
```

---

## 2. Minimal 12-Dimensional Schema Structure

To guarantee end-to-end auditability without premature bloat, the contract requires exactly 12 minimal dimensional records:

1. **`requirement`**: `req_id`, `statement`, and `provenance: USER_CONFIRMED`.
2. **`spec`**: `spec_id` and approval `status`.
3. **`architecture`**: `touched_nodes` (array of graph entity IDs modified or introduced).
4. **`dependencies`**: `records` (array of Dependency Decision Record IDs).
5. **`contracts`**: `contract_ids` (array of contracts adhered to by the feature).
6. **`implementation`**: `commit_sha` and `diff_hash` representing the physical code change.
7. **`tests`**: `test_node_ids` and `passed_count`.
8. **`security`**: `sandbox_policy_id` and `gateway_verdict: PASS | FAIL`.
9. **`documentation`**: `doc_node_ids` and `doc_drift_status: PASS | FAIL`.
10. **`evidence`**: `evidence_ids` (array of immutable execution evidence logs).
11. **`git`**: `base_commit`, `head_commit`, and `branch`.
12. **`verification`**: `verification_id` and `converged: true | false`.

---

## 3. Passport Stamping Rules & Invariants

1. **Convergence Prerequisite (INV-003)**: A passport can transition to `status = "CONVERGED"` **if and only if** `dimensions.verification.converged == true` and `dimensions.security.gateway_verdict == "PASS"`.
2. **Immutability Once Stamped**: Once stamped with `stamped_at` and `stamped_by`, the passport becomes immutable. If subsequent commits break the feature, a new passport version must be issued.
3. **Training & Evolution Gating (INV-004)**: Only features carrying a stamped `CONVERGED` passport may be fed into the Evolution or learning pipeline as positive exemplars.

---

## 4. Phase 4 Handoff

Phase 4 will specify:
- Specification-to-passport projection format.
- Interactive CLI inspection commands (`eidos passport inspect <feat-id>`).
- Export templates for human-facing documentation releases.
