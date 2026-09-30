# SPEC-013 — Feature Passport & 12-Dimensional Traceability Bridge

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of the Feature Passport subsystem: serving as the definitive 12-dimensional convergence bridge linking requirements, specifications, architecture, code, tests, evidence, and verification across all project phases.

## 3. Scope
Passport schema generation, dimensional validation, verification result linkage, cryptographic commit anchoring, and stamping on convergence.

## 4. Non-Goals
- Does not implement an external cloud credential service.
- Does not permit passports to be stamped without passing machine verification.
- Does not replace Git commit messages (complements them with structured metadata).

## 5. Source Requirements
- `REQ-PASS-001`: 12-Dimensional Traceability Certificate
- `REQ-PASS-002`: Stamping Gated Strictly by Convergence

## 6. Architectural Basis
- `docs/architecture/data-model.md §4`: Feature Passport architectural model.
- `docs/adr/P2-ADR-007`: Progress passports and evidence anchoring.
- `docs/contracts/feature-passport.md`: Contractual schema definition.

## 7. Contract Dependencies
- `CORE-CONTRACT-010`: Feature Passport Contract schema (`schemas/contracts/core/feature-passport.schema.json`).
- `VERIF-CONTRACT-001`: Verifier Contract.
- `CORE-CONTRACT-005`: Evidence Contract.

## 8. Behavioral Requirements
When a task or feature finishes execution, the orchestrator compiles the 12-dimensional passport record:
1. `requirement`: `req_id`, `statement`, `provenance: USER_CONFIRMED`.
2. `spec`: `spec_id`, `status`.
3. `architecture`: `touched_nodes` (graph entity IDs).
4. `dependencies`: `records` (DDR IDs).
5. `contracts`: `contract_ids`.
6. `implementation`: `commit_sha`, `diff_hash`.
7. `tests`: `test_node_ids`, `passed_count`.
8. `security`: `sandbox_policy_id`, `gateway_verdict`.
9. `documentation`: `doc_node_ids`, `doc_drift_status`.
10. `evidence`: `evidence_ids`.
11. `git`: `base_commit`, `head_commit`, `branch`.
12. `verification`: `verification_id`, `converged`.
If and only if `verification.converged == true` and `security.gateway_verdict == "PASS"`, the passport transitions to `CONVERGED` and is stamped.

## 9. Inputs
- Completed task context and patch diff.
- `VerificationResult` from Verifier subsystem.

## 10. Outputs
- Validated, immutable `FeaturePassport` record written to `.eidos/passports/<feature_id>.json`.

## 11. State Model
Lifecycle: `DRAFT → VERIFIED → CONVERGED`.

## 12. Invariants
- `INV-003`: `CONVERGED` status cannot be granted if `verification.converged` is false.
- `INV-005`: All evidence IDs in the passport must resolve to existing evidence log entries.

## 13. Preconditions
- The candidate patch must be staged in Git.
- Verification runner must have completed evaluation of all active layers.

## 14. Postconditions
- The stamped passport is committed to git in synchronization with the feature patch.

## 15. Failure Semantics
If verification fails, the passport remains in `DRAFT` or `VERIFIED` (unconverged) state; the pipeline refuses to stamp the feature.

## 16. Security Requirements
- The passport captures the `sandbox_policy_id` under which the feature was evaluated.
- Any security gateway failure blocks convergence unconditionally.

## 17. Observability Requirements
- Emits structured telemetry on passport creation, dimensional validation errors, and convergence stamping.

## 18. Edge Cases
- Partial feature revert: If a Git commit reverts changes of a feature, a new passport must be issued with updated diff hashes and test evidence.
- Multi-feature commit: Each feature maintains its own distinct passport file.

## 19. Acceptance Criteria
### `AC-013-01` (12-Dimensional Schema Conformance)
```gherkin
Given a converged task ready for feature passport stamping
When the orchestrator generates the Feature Passport
Then the resulting JSON object must satisfy all 12 required dimensions of CORE-CONTRACT-010.
```

### `AC-013-02` (Convergence Gating on Stamping)
```gherkin
Given a verification result where test_failed=1 and converged=false
When passport stamping is requested
Then passport status must not transition to CONVERGED and an error must be emitted.
```

## 20. Verification Strategy
Automated tests in `tests/specs/test_feature_passport.py` verifying full 12-dimensional schema validation and refusal to stamp unconverged runs.

## 21. Traceability
- Research: EVD-015, EVD-018
- ADR: `P2-ADR-007`
- Contract: `CORE-CONTRACT-010`, `VERIF-CONTRACT-001`
- Requirements: `REQ-PASS-001`, `REQ-PASS-002`

## 22. Open Questions & Phase 5 Notes
- CLI passport inspection commands (`eidos passport inspect <id>`) to be built in Phase 5.
- Phase 5 note: Serialize passports using deterministic JSON formatting (sorted keys, 2 spaces indentation).
