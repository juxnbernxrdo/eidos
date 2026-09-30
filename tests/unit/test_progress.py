"""Unit tests for SPEC-013 (Feature Passport) and SPEC-015 (Progress Observability)."""

from pathlib import Path
import pytest

from eidos.core.exceptions import VerificationError, ContractViolationError
from eidos.progress.passport import FeaturePassportManager
from eidos.progress.projector import ProgressProjector


def make_valid_dimensions(converged: bool = True, sec_verdict: str = "PASS") -> dict:
    return {
        "requirement": {
            "req_id": "REQ-TEST-001",
            "statement": "Implement test feature",
            "provenance": "USER_CONFIRMED",
        },
        "spec": {
            "spec_id": "SPEC-001",
            "status": "ACCEPTED",
        },
        "architecture": {
            "touched_nodes": ["node:state_py"],
        },
        "dependencies": {
            "records": ["DDR-001"],
        },
        "contracts": {
            "contract_ids": ["CORE-CONTRACT-001"],
        },
        "implementation": {
            "commit_sha": "abc1234",
            "diff_hash": "sha256:fedcba",
        },
        "tests": {
            "test_node_ids": ["test:test_core_state"],
            "passed_count": 5,
        },
        "security": {
            "sandbox_policy_id": "SANDBOX-DEFAULT",
            "gateway_verdict": sec_verdict,
        },
        "documentation": {
            "doc_node_ids": ["doc:spec-001"],
            "doc_drift_status": "PASS",
        },
        "evidence": {
            "evidence_ids": ["EVD-001"],
        },
        "git": {
            "base_commit": "c000",
            "head_commit": "c001",
            "branch": "main",
        },
        "verification": {
            "verification_id": "VERIF-001",
            "converged": converged,
        },
    }


def test_passport_12_dimensional_conformance_ac_013_01(tmp_path: Path):
    """AC-013-01: Generates valid 12-dimensional Feature Passport satisfying CORE-CONTRACT-010."""
    manager = FeaturePassportManager(tmp_path)
    dims = make_valid_dimensions(converged=True, sec_verdict="PASS")
    
    passport = manager.compile_passport("FEAT-STATE-01", dims, auto_stamp=True)
    
    assert passport["contract_id"] == "CORE-CONTRACT-010"
    assert passport["feature_id"] == "FEAT-STATE-01"
    assert passport["status"] == "CONVERGED"
    assert len(passport["dimensions"]) == 12
    assert (tmp_path / ".eidos" / "passports" / "FEAT-STATE-01.json").exists()


def test_passport_convergence_gating_ac_013_02(tmp_path: Path):
    """AC-013-02: Unconverged verification blocks passport stamping to CONVERGED."""
    manager = FeaturePassportManager(tmp_path)
    dims = make_valid_dimensions(converged=False, sec_verdict="PASS")
    
    with pytest.raises(VerificationError) as exc_info:
        manager.compile_passport("FEAT-FAIL-01", dims, auto_stamp=True)
        
    assert "Refusing to stamp Feature Passport" in str(exc_info.value)
    assert "verification not converged" in str(exc_info.value)


def test_progress_evidence_gated_metric_ac_015_01():
    """AC-015-01: Agent verbal claims without machine verification are reported as UNCONVERGED."""
    projector = ProgressProjector()
    events = [
        {
            "event_id": "EVT-001",
            "event_type": "TASK_CREATED",
            "payload": {"task_id": "TASK-100", "title": "Build parser"},
        },
        {
            "event_id": "EVT-002",
            "event_type": "AGENT_MESSAGE",
            "task_id": "TASK-100",
            "payload": {"message": "I am done, the task is complete and verified."},
        },
    ]
    
    summary = projector.project_events(events)
    assert summary["total_tasks"] == 1
    assert summary["converged_tasks"] == 0
    assert summary["unconverged_tasks"] == 1
    assert summary["verified_success_rate"] == 0.0
    assert summary["tasks"]["TASK-100"]["verbal_claim_only"] is True


def test_progress_deterministic_token_cost_ac_015_02():
    """AC-015-02: Aggregates tokens and costs deterministically from event stream."""
    projector = ProgressProjector()
    events = [
        {"event_id": "EVT-01", "event_type": "TOOL_INVOKED", "payload": {"tokens": 100, "cost_usd": 0.001}},
        {"event_id": "EVT-02", "event_type": "TOOL_INVOKED", "payload": {"tokens": 200, "cost_usd": 0.002}},
        {"event_id": "EVT-03", "event_type": "TOOL_INVOKED", "payload": {"tokens": 300, "cost_usd": 0.003}},
    ]
    
    summary = projector.project_events(events)
    assert summary["total_tokens_consumed"] == 600
    assert summary["total_cost_usd"] == 0.006
    assert summary["total_tool_invocations"] == 3
