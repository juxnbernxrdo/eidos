# Phase 6 Machine Evidence Registry

**Authority:** Eidos Verification Protocol  
**Scope:** Complete Catalog of Reproducible Machine Evidence Artifacts  
**Status:** VALIDATED  
**Last Updated:** 2026-09-30  

---

## 1. Registry Architecture & Protocol

In accordance with Eidos epistemic standards, no claim of conformance is valid without a permanent entry in this registry. Each evidence item records:
- **Evidence ID**: Unique canonical identifier.
- **Verification Level**: L1 through L14.
- **Target Contract / Spec / Invariant**: Traceability anchor.
- **Execution Command / Test**: Exact command reproducing the assertion.
- **Artifact Trace**: Test function, output assertion, or log location.
- **Result / Exit Code**: Machine return status (`0` / `PASS`).

---

## 2. Level-by-Level Verification Evidence Catalog

| Evidence ID | Level | Verification Dimension | Reproducible Test / Command | Output / Assertion | Exit Status |
|:---:|:---:|:---|:---|:---|:---:|
| `EVID-L01` | L1 | Syntax & AST Parsing | `.venv/bin/pytest tests/verification/test_level1_syntax_build.py` | All 18 modules compile & import cleanly; entrypoint discoverable. | `PASS` (0) |
| `EVID-L02` | L2 | Static Analysis & Types | `.venv/bin/pytest tests/verification/test_level2_static_analysis.py` | Import graph is strict DAG; 100% public functions documented. | `PASS` (0) |
| `EVID-L03` | L3 | Unit Verification | `.venv/bin/pytest tests/unit/ tests/integration/test_verifier.py` | Zero false confidence, oracle diagnostics verified. | `PASS` (0) |
| `EVID-L04` | L4 | Contract Schemas | `.venv/bin/pytest tests/contracts/test_contract_schemas.py` | 15 contracts validate 100% against Draft 2020-12 schemas. | `PASS` (0) |
| `EVID-L05` | L5 | Specifications | `.venv/bin/pytest tests/specs/test_spec_consistency.py` | All 35 Given/When/Then acceptance criteria verified. | `PASS` (0) |
| `EVID-L06` | L6 | State Machine | `.venv/bin/pytest tests/verification/test_level6_state_machine.py` | Pure fold deterministic under 100-event stress; snapshot resumption identical. | `PASS` (0) |
| `EVID-L07` | L7 | System Invariants | `.venv/bin/pytest tests/verification/test_level7_invariants_comprehensive.py` | `ARCH-001`, `ARCH-002`, `INV-001`..`INV-009` machine-checked. | `PASS` (0) |
| `EVID-L08` | L8 | Security & Sandbox | `.venv/bin/pytest tests/verification/test_level8_security_boundaries.py` | Symlink traversal blocked; 6 multi-provider secrets scrubbed. | `PASS` (0) |
| `EVID-L09` | L9 | Heterogeneous Graph | `.venv/bin/pytest tests/verification/test_level9_graph_semantics.py` | 21 nodes, 11 edges, `EXTRACTED` > `INFERRED` precedence confirmed. | `PASS` (0) |
| `EVID-L10` | L10 | Context Router | `.venv/bin/pytest tests/unit/test_context_router.py` | Topological pruning within budget; pinned invariants preserved. | `PASS` (0) |
| `EVID-L11` | L11 | Subagent Isolation | `.venv/bin/pytest tests/integration/test_pipeline.py` | Fresh context (0 turns) and CodeAct sandbox verified. | `PASS` (0) |
| `EVID-L12` | L12 | Harness Adapters | `.venv/bin/pytest tests/unit/test_harness_adapter.py` | Zero host leak; 6 lifecycle operations emit complete trace. | `PASS` (0) |
| `EVID-L13` | L13 | Event Log & Progress | `.venv/bin/pytest tests/unit/test_event_log.py tests/unit/test_progress.py` | Monotonic JSONL, POSIX lock, Git HEAD anchoring, honest metrics. | `PASS` (0) |
| `EVID-L14` | L14 | Feature Passports | `.venv/bin/pytest tests/verification/test_level14_feature_passports.py` | 15/15 features compile complete 12-dimensional passports. | `PASS` (0) |

---

## 3. Requirement Verification Evidence Index (`EVID-VER-001` to `035`)

| Evidence ID | Requirement ID | Specification | Verifying Test Identifier | Assertion Verified |
|:---:|:---|:---|:---|:---|
| `EVID-VER-001` | `REQ-CORE-001` | `SPEC-001` | `tests/unit/test_core_state.py::test_deterministic_fold_ac_001_01` | Pure fold deterministic replay |
| `EVID-VER-002` | `REQ-CORE-002` | `SPEC-001` | `tests/unit/test_core_state.py::test_illegal_transition_rejection_ac_001_02` | Invalid state transition rejected |
| `EVID-VER-003` | `REQ-PIPE-001` | `SPEC-002` | `tests/integration/test_pipeline.py::test_non_bypassable_gating_ac_002_01` | Verification gate cannot be bypassed |
| `EVID-VER-004` | `REQ-PIPE-002` | `SPEC-002` | `tests/integration/test_pipeline.py::test_repair_loop_bounding_at_k_ac_002_02` | Repair loop terminates at $k \le 5$ |
| `EVID-VER-005` | `REQ-PIPE-003` | `SPEC-002` | `tests/integration/test_pipeline.py::test_diagnostic_diff_on_escalation_ac_002_03` | Diagnostic diff emitted on escalation |
| `EVID-VER-006` | `REQ-TASK-001` | `SPEC-003` | `tests/unit/test_task.py::test_task_lifecycle_transitions` | Valid task lifecycle sequence |
| `EVID-VER-007` | `REQ-TASK-002` | `SPEC-003` | `tests/unit/test_task.py::test_illegal_unconverged_transition_rejection` | Unconverged completion rejected |
| `EVID-VER-008` | `REQ-CTX-001` | `SPEC-004` | `tests/unit/test_context_router.py::test_topological_pruning_and_boundary_pinning_ac_004_01` | Topological pruning with pinned boundary |
| `EVID-VER-009` | `REQ-CTX-002` | `SPEC-004` | `tests/unit/test_context_router.py::test_auditable_selection_reason_ac_004_02` | Auditable rationale for context items |
| `EVID-VER-010` | `REQ-CTX-003` | `SPEC-004` | `tests/unit/test_context_router.py::test_token_budget_enforcement_ac_004_03` | Total token count $\le \text{budget}$ |
| `EVID-VER-011` | `REQ-GRAPH-001` | `SPEC-005` | `tests/unit/test_graph_engine.py::test_heterogeneous_nodes_and_extracted_provenance_ac_005_01` | Heterogeneous nodes & extraction provenance |
| `EVID-VER-012` | `REQ-GRAPH-002` | `SPEC-005` | `tests/unit/test_graph_engine.py::test_epistemic_precedence_over_inference_ac_005_02` | `EXTRACTED` overrides `INFERRED` |
| `EVID-VER-013` | `REQ-GRAPH-003` | `SPEC-005` | `tests/unit/test_graph_engine.py::test_hop_bounded_neighborhood_traversal_ac_005_03` | $k \le 2$ hop neighborhood extraction |
| `EVID-VER-014` | `REQ-VERIF-001` | `SPEC-006` | `tests/integration/test_verifier.py::test_convergence_on_pass_ac_006_01` | `PASS` result marks convergence |
| `EVID-VER-015` | `REQ-VERIF-002` | `SPEC-006` | `tests/integration/test_verifier.py::test_repair_eligibility_with_oracle_trace_ac_006_02` | `FAIL` emits oracle trace for repair |
| `EVID-VER-016` | `REQ-VERIF-003` | `SPEC-006` | `tests/integration/test_verifier.py::test_exhaustion_escalation_ac_006_03` | $k > K_{max}$ transitions to `EXHAUSTED` |
| `EVID-VER-017` | `REQ-EVT-001` | `SPEC-007` | `tests/unit/test_event_log.py::test_append_only_immutability_ac_007_01` | Append-only immutability under lock |
| `EVID-VER-018` | `REQ-EVT-002` | `SPEC-007` | `tests/unit/test_event_log.py::test_git_head_anchoring_ac_007_02` | Events anchored to valid Git HEAD |
| `EVID-VER-019` | `REQ-SEC-001` | `SPEC-008` | `tests/security/test_sandbox.py::test_default_deny_file_write_ac_008_01` | Unauthorized file writes denied |
| `EVID-VER-020` | `REQ-SEC-002` | `SPEC-008` | `tests/security/test_sandbox.py::test_cross_project_path_confinement_ac_008_02` | Path escapes outside root blocked |
| `EVID-VER-021` | `REQ-SEC-003` | `SPEC-008` | `tests/verification/test_level8_security_boundaries.py::test_comprehensive_secret_scrubbing` | Secrets scrubbed across providers |
| `EVID-VER-022` | `REQ-HARN-001` | `SPEC-009` | `tests/unit/test_harness_adapter.py::test_zero_host_leakage_ac_009_01` | Zero host environment variable leak |
| `EVID-VER-023` | `REQ-HARN-002` | `SPEC-009` | `tests/unit/test_harness_adapter.py::test_complete_raw_trace_collection_ac_009_02` | Unparsed trace stream capture |
| `EVID-VER-024` | `REQ-AGENT-001` | `SPEC-010` | `tests/integration/test_pipeline.py::test_subagent_fresh_context_isolation_ac_010_01` | Zero prior conversational turns |
| `EVID-VER-025` | `REQ-AGENT-002` | `SPEC-010` | `tests/integration/test_pipeline.py::test_codeact_sandboxed_execution_ac_010_02` | CodeAct sandbox execution confined |
| `EVID-VER-026` | `REQ-MEM-001` | `SPEC-011` | `tests/unit/test_memory_gating.py::test_default_opt_in_gating_ac_011_01` | Memory disabled by default |
| `EVID-VER-027` | `REQ-MEM-002` | `SPEC-011` | `tests/unit/test_memory_gating.py::test_cross_project_isolation_ac_011_02` | Zero memory leakage across projects |
| `EVID-VER-028` | `REQ-SKILL-001` | `SPEC-012` | `tests/unit/test_skill_gateway.py::test_malicious_pattern_rejection_ac_012_01` | Dangerous script patterns blocked |
| `EVID-VER-029` | `REQ-SKILL-002` | `SPEC-012` | `tests/unit/test_skill_gateway.py::test_lockfile_hash_pinning_ac_012_02` | Unpinned or tampered skills rejected |
| `EVID-VER-030` | `REQ-PASS-001` | `SPEC-013` | `tests/verification/test_level14_feature_passports.py::test_passport_compilation_all_15_features` | 15 features satisfy all 12 dimensions |
| `EVID-VER-031` | `REQ-PASS-002` | `SPEC-013` | `tests/unit/test_progress.py::test_passport_convergence_gating_ac_013_02` | Gated transition blocks missing passport |
| `EVID-VER-032` | `REQ-EVO-001` | `SPEC-014` | `tests/unit/test_evolution_pipeline.py::test_human_approval_gate_enforcement_ac_014_01` | Human signature required for evolution |
| `EVID-VER-033` | `REQ-EVO-002` | `SPEC-014` | `tests/unit/test_evolution_pipeline.py::test_blocking_unapproved_self_modification_ac_014_02` | Self-modification blocked without gate |
| `EVID-VER-034` | `REQ-OBS-001` | `SPEC-015` | `tests/unit/test_progress.py::test_progress_evidence_gated_metric_ac_015_01` | Progress calculated from verified passes |
| `EVID-VER-035` | `REQ-OBS-002` | `SPEC-015` | `tests/unit/test_progress.py::test_progress_deterministic_token_cost_ac_015_02` | Deterministic cost accounting |

---

## 4. Overall Evidence Statistics

- Total Machine Evidence Records: 49 (`EVID-L01`..`L14` + `EVID-VER-001`..`035`)
- Passing Evidence Records: 49 (100.0%)
- Failing Evidence Records: 0 (0.0%)
- Re-run Reproducibility Rate: 100.0%
