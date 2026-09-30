"""Contract tests verifying schema validity, serialization, and fail-closed rejection.

In accordance with Phase 3 instructions (§24 & §25), these tests validate
contracts and schemas, NOT system runtime behavior.
"""

import json
from pathlib import Path
import pytest

from eidos.contracts.validator import ContractSchemaValidator


SCHEMAS_DIR = Path(__file__).parent.parent.parent / "schemas" / "contracts"


def get_all_schema_paths() -> list[Path]:
    """Retrieve all JSON schema files under schemas/contracts."""
    return sorted(list(SCHEMAS_DIR.glob("**/*.schema.json")))


def test_schema_inventory_count():
    """Verify that all 15 planned schemas exist."""
    schemas = get_all_schema_paths()
    assert len(schemas) == 15, f"Expected 15 schemas, found {len(schemas)}: {[s.name for s in schemas]}"


def test_all_schemas_syntax_and_structure():
    """Verify that every schema parses as valid JSON and conforms to Draft 2020-12 structure."""
    schemas = get_all_schema_paths()
    for schema_path in schemas:
        with open(schema_path, "r", encoding="utf-8") as f:
            try:
                schema_json = json.load(f)
            except Exception as e:
                pytest.fail(f"Schema {schema_path.name} failed JSON parsing: {e}")

        errors = ContractSchemaValidator.validate_schema_structure(schema_json)
        assert not errors, f"Schema {schema_path.name} has structural errors:\n" + "\n".join(errors)


def test_schema_identifiers_are_unique():
    """Ensure no duplicate $id or contract_id definitions exist across schemas."""
    schemas = get_all_schema_paths()
    seen_ids = set()
    seen_contract_ids = set()

    for schema_path in schemas:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        schema_id = schema.get("$id")
        assert schema_id not in seen_ids, f"Duplicate schema $id: {schema_id}"
        seen_ids.add(schema_id)

        # Check contract_id if top-level const
        contract_id_prop = schema.get("properties", {}).get("contract_id", {})
        if "const" in contract_id_prop:
            cid = contract_id_prop["const"]
            assert cid not in seen_contract_ids, f"Duplicate contract_id const: {cid}"
            seen_contract_ids.add(cid)


def test_harness_adapter_contract_valid_payload():
    """Verify valid HarnessAdapter dispatch and response payloads."""
    schema_path = SCHEMAS_DIR / "harness" / "harness-adapter.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    valid_payload = {
        "contract_id": "HARN-CONTRACT-001",
        "contract_version": "1.0.0",
        "harness_id": "antigravity",
        "lifecycle_state": "READY",
        "capabilities": {
            "supports_subagents": True,
            "supports_codeact": True,
            "supports_mcp": True,
            "supports_worktrees": True,
            "supports_sandbox": True,
            "trace_fidelity": "full_raw"
        },
        "dispatch_request": {
            "execution_id": "exec-101",
            "task": {
                "task_id": "TASK-001",
                "objective": "Verify contracts",
                "target_files": ["tests/contracts/test_contract_schemas.py"],
                "allowed_tools": ["pytest"]
            },
            "context_payload": {
                "msc_id": "msc-001",
                "content": "# Test context",
                "token_count": 42
            },
            "permissions": {
                "filesystem_scope": "repo_read_only",
                "network_scope": "disabled",
                "max_turns": 10,
                "timeout_seconds": 300
            },
            "environment": {"CI": "true"}
        },
        "execution_response": {
            "execution_id": "exec-101",
            "status": "COMPLETED",
            "result_summary": "Execution finished cleanly",
            "patch_diff": "",
            "artifacts": [],
            "observation_trace": [
                {
                    "turn_index": 1,
                    "timestamp": "2026-09-30T15:30:00Z",
                    "action": "pytest",
                    "output": "17 passed",
                    "exit_code": 0
                }
            ],
            "evidence_refs": ["EVD-101"],
            "errors": []
        }
    }

    errors = ContractSchemaValidator.validate_payload(schema, valid_payload)
    assert not errors, f"Valid payload had validation errors: {errors}"


def test_context_router_contract_valid_payload():
    """Verify ContextRouter minimal sufficient context payload with auditable selection."""
    schema_path = SCHEMAS_DIR / "context" / "context-router.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    valid_payload = {
        "contract_id": "CTX-CONTRACT-001",
        "contract_version": "1.0.0",
        "routing_request": {
            "request_id": "req-001",
            "task": {
                "task_id": "TASK-001",
                "objective": "Test routing",
                "target_files": ["src/eidos/core/state.py"],
                "seed_symbols": ["Fold"]
            },
            "context_sources": {
                "include_graph": True,
                "include_rules": True,
                "include_specs": True,
                "include_skills": False,
                "include_memory": False,
                "include_evidence": True
            },
            "budget_constraints": {
                "max_tokens": 8000,
                "reserve_for_generation": 2000,
                "k_hop_limit": 2
            },
            "security_constraints": {
                "quarantine_adversarial": True,
                "allow_inferred_edges": False,
                "isolated_project_id": "PROJ-EIDOS"
            }
        },
        "routing_response": {
            "msc_id": "msc-001",
            "request_id": "req-001",
            "total_tokens": 3500,
            "budget_exhausted": False,
            "escalation_required": False,
            "pinned_boundary_contracts": ["HARN-CONTRACT-001"],
            "assembled_items": [
                {
                    "item_id": "ctx-item-1",
                    "order_index": 0,
                    "source_domain": "GRAPH_NODE",
                    "content_format": "FULL_CODE",
                    "content": "def Fold(s, events): pass",
                    "token_count": 150,
                    "epistemic_provenance": "EXTRACTED",
                    "confidence": 1.0,
                    "selection_audit": {
                        "selection_reason": "TARGET_SCOPE",
                        "proximity_hops": 0,
                        "matched_query": "Fold"
                    }
                }
            ],
            "quarantined_exclusions": []
        }
    }

    errors = ContractSchemaValidator.validate_payload(schema, valid_payload)
    assert not errors, f"Context router payload errors: {errors}"


def test_graph_store_contract_valid_payload():
    """Verify GraphStore snapshot with epistemic tags and query interface."""
    schema_path = SCHEMAS_DIR / "graph" / "graph-store.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    valid_payload = {
        "contract_id": "GRAPH-CONTRACT-001",
        "contract_version": "1.0.0",
        "snapshot": {
            "snapshot_id": "snap-001",
            "project_id": "PROJ-EIDOS",
            "git_commit": "bbe1167",
            "created_at": "2026-09-30T15:30:00Z",
            "graph_freshness": "FRESH",
            "node_count": 2,
            "edge_count": 1,
            "nodes": [
                {
                    "id": "file:src/core/state.py",
                    "type": "File",
                    "label": "state.py",
                    "file_path": "src/core/state.py"
                },
                {
                    "id": "fn:core.state#Fold",
                    "type": "Function",
                    "label": "Fold",
                    "file_path": "src/core/state.py",
                    "line_range": [10, 30]
                }
            ],
            "edges": [
                {
                    "source": "file:src/core/state.py",
                    "target": "fn:core.state#Fold",
                    "relation": "DEFINED_BY",
                    "epistemic_provenance": "EXTRACTED",
                    "confidence": 1.0
                }
            ]
        },
        "query_interface": {
            "query_type": "traverse",
            "parameters": {
                "seed_ids": ["fn:core.state#Fold"],
                "k_hops": 2,
                "edge_whitelist": ["DEFINED_BY", "DEPENDS_ON"]
            }
        }
    }

    errors = ContractSchemaValidator.validate_payload(schema, valid_payload)
    assert not errors, f"Graph store payload errors: {errors}"


def test_verifier_contract_valid_payload():
    """Verify Verifier 7-layer result, repair eligibility, and CONVERGED verdict."""
    schema_path = SCHEMAS_DIR / "verification" / "verifier.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    valid_payload = {
        "contract_id": "VERIF-CONTRACT-001",
        "contract_version": "1.0.0",
        "verification_target": {
            "task_id": "TASK-001",
            "spec_id": "SPEC-001",
            "target_files": ["src/eidos/core/state.py"],
            "git_head_sha": "bbe1167",
            "attempt_index": 1
        },
        "verification_policy": {
            "max_repair_attempts_k": 5,
            "active_layers": ["tests", "static_types", "lint", "contracts", "invariants"]
        },
        "layer_results": {
            "tests": {
                "status": "PASS",
                "passed": 17,
                "failed": 0,
                "errors": 0,
                "oracle_trace": "17 passed in 0.91s"
            },
            "static_types": {
                "status": "PASS",
                "error_count": 0,
                "diagnostic_messages": []
            },
            "lint": {
                "status": "PASS",
                "violation_count": 0,
                "details": []
            },
            "contracts": {
                "status": "PASS",
                "schema_errors": []
            },
            "invariants": {
                "status": "PASS",
                "violations": []
            }
        },
        "verdict_payload": {
            "verdict": "CONVERGED",
            "converged": True,
            "repair_eligibility": {
                "is_eligible": False,
                "reason": "All layers passed successfully."
            },
            "evidence_id": "EVD-VERIF-001",
            "timestamp": "2026-09-30T15:30:00Z"
        }
    }

    errors = ContractSchemaValidator.validate_payload(schema, valid_payload)
    assert not errors, f"Verifier payload errors: {errors}"


def test_event_log_contract_valid_payload():
    """Verify EventLog payload with Git HEAD anchor and fold operations."""
    schema_path = SCHEMAS_DIR / "events" / "event-log.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    valid_payload = {
        "contract_id": "EVENT-CONTRACT-001",
        "contract_version": "1.0.0",
        "event": {
            "event_id": "evt-000001",
            "timestamp": "2026-09-30T15:30:00Z",
            "event_type": "TASK_CONVERGED",
            "actor": {
                "type": "SYSTEM",
                "id": "eidos-core"
            },
            "session_id": "sess-001",
            "project_id": "PROJ-EIDOS",
            "git_commit": "bbe1167",
            "payload": {
                "task_id": "TASK-001",
                "verification_id": "VERIF-001"
            },
            "provenance": "OBSERVED",
            "schema_version": "1.0.0"
        },
        "operations": {
            "append": {
                "accepted": True,
                "persisted_event_id": "evt-000001",
                "log_offset": 0
            },
            "read": {
                "limit": 50,
                "returned_count": 1
            },
            "replay": {
                "from_event_id": "evt-000001",
                "to_event_id": "evt-000001",
                "events_folded": 1,
                "projected_state_hash": "a1b2c3d4e5"
            },
            "snapshot": {
                "snapshot_id": "snap-001",
                "anchored_event_id": "evt-000001",
                "projected_state": {"status": "ready"},
                "timestamp": "2026-09-30T15:30:01Z"
            }
        }
    }

    errors = ContractSchemaValidator.validate_payload(schema, valid_payload)
    assert not errors, f"EventLog payload errors: {errors}"


def test_feature_passport_contract_valid_payload():
    """Verify FeaturePassport minimal 12-dimensional schema."""
    schema_path = SCHEMAS_DIR / "core" / "feature-passport.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    valid_payload = {
        "contract_id": "CORE-CONTRACT-010",
        "contract_version": "1.0.0",
        "passport_id": "PASS-FEAT-001",
        "feature_id": "phase-3-contracts",
        "status": "CONVERGED",
        "dimensions": {
            "requirement": {
                "req_id": "REQ-P3-001",
                "statement": "Establish machine-readable contracts",
                "provenance": "USER_CONFIRMED"
            },
            "spec": {
                "spec_id": "SPEC-CONTRACTS",
                "status": "ACCEPTED"
            },
            "architecture": {
                "touched_nodes": ["Contract:HarnessAdapter", "Contract:ContextRouter"]
            },
            "dependencies": {
                "records": ["DDR-001-PYTHON"]
            },
            "contracts": {
                "contract_ids": ["HARN-CONTRACT-001", "CTX-CONTRACT-001"]
            },
            "implementation": {
                "commit_sha": "bbe1167",
                "diff_hash": "d41d8cd98f00b204e9800998ecf8427e"
            },
            "tests": {
                "test_node_ids": ["test_contract_schemas.py"],
                "passed_count": 10
            },
            "security": {
                "sandbox_policy_id": "POLICY-DEFAULT",
                "gateway_verdict": "PASS"
            },
            "documentation": {
                "doc_node_ids": ["docs/contracts/governance.md"],
                "doc_drift_status": "PASS"
            },
            "evidence": {
                "evidence_ids": ["EVD-001", "EVD-002"]
            },
            "git": {
                "base_commit": "d820503",
                "head_commit": "bbe1167",
                "branch": "main"
            },
            "verification": {
                "verification_id": "VERIF-P3-001",
                "converged": True
            }
        },
        "stamped_at": "2026-09-30T15:30:00Z",
        "stamped_by": "eidos-phase-3-gate"
    }

    errors = ContractSchemaValidator.validate_payload(schema, valid_payload)
    assert not errors, f"FeaturePassport payload errors: {errors}"


def test_fail_closed_on_uncontracted_additional_properties():
    """Verify that unexpected extra properties cause fail-closed rejection."""
    schema_path = SCHEMAS_DIR / "core" / "task.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    invalid_payload = {
        "contract_id": "CORE-CONTRACT-002",
        "contract_version": "1.0.0",
        "task_id": "TASK-001",
        "spec_id": "SPEC-001",
        "title": "Title",
        "objective": "Objective",
        "status": "PENDING",
        "target_files": ["a.py"],
        "allowed_tools": ["pytest"],
        "acceptance_criteria": ["pass"],
        "uncontracted_rogue_field": "EXPLODING_INJECTION"
    }

    errors = ContractSchemaValidator.validate_payload(schema, invalid_payload)
    assert any("unexpected property 'uncontracted_rogue_field'" in err for err in errors), (
        f"Expected unexpected property error, got: {errors}"
    )


def test_fail_closed_on_secret_access_violation():
    """Verify that attempting to enable secret_access in CapabilityPermission is rejected."""
    schema_path = SCHEMAS_DIR / "core" / "capability-permission.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    breach_payload = {
        "contract_id": "CORE-CONTRACT-008",
        "contract_version": "1.0.0",
        "grant_id": "GRANT-001",
        "subject": {"type": "AGENT", "id": "agent-rogue"},
        "filesystem": {
            "scope": "READ_ONLY",
            "allowed_read_patterns": ["src/*"],
            "allowed_write_patterns": [],
            "denied_patterns": ["/etc/*"]
        },
        "network": {
            "egress": "DISABLED",
            "allowed_hosts": []
        },
        "execution": {
            "allow_subprocess": False,
            "allowed_binaries": [],
            "timeout_seconds": 60
        },
        "secret_access": True,  # CONTRACT BREACH: must be false!
        "issued_at": "2026-09-30T15:30:00Z"
    }

    errors = ContractSchemaValidator.validate_payload(schema, breach_payload)
    assert any("does not match const 'False'" in err or "does not match const" in err for err in errors), (
        f"Expected secret_access const violation, got: {errors}"
    )


def test_fail_closed_on_invalid_enum_status():
    """Verify that unauthorized status values fail validation."""
    schema_path = SCHEMAS_DIR / "core" / "task.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    invalid_status_payload = {
        "contract_id": "CORE-CONTRACT-002",
        "contract_version": "1.0.0",
        "task_id": "TASK-001",
        "spec_id": "SPEC-001",
        "title": "Title",
        "objective": "Objective",
        "status": "VALIDATED_AND_DEPLOYED",  # Invalid enum!
        "target_files": ["a.py"],
        "allowed_tools": ["pytest"],
        "acceptance_criteria": ["pass"]
    }

    errors = ContractSchemaValidator.validate_payload(schema, invalid_status_payload)
    assert any("not in allowed enum" in err for err in errors), f"Expected enum rejection, got: {errors}"
