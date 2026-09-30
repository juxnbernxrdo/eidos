"""Level 14 Verification Suite: Feature Passport 12-Dimensional Traceability Bridges."""

from pathlib import Path
import pytest
from eidos.core.exceptions import ContractViolationError, VerificationError
from eidos.progress.passport import FeaturePassportManager, REQUIRED_DIMENSIONS


def make_test_dimensions(feature_key: str, converged: bool = True):
    return {
        "requirement": {
            "req_id": f"REQ-{feature_key.upper()}-001",
            "statement": f"Requirement statement for {feature_key}",
            "provenance": "USER_CONFIRMED",
        },
        "spec": {
            "spec_id": f"SPEC-{feature_key.upper()}",
            "status": "ACCEPTED",
        },
        "architecture": {
            "touched_nodes": [f"node:{feature_key}"],
        },
        "dependencies": {
            "records": ["DDR-001"],
        },
        "contracts": {
            "contract_ids": [f"CONTRACT-{feature_key.upper()}"],
        },
        "implementation": {
            "commit_sha": "c1234567",
            "diff_hash": "sha256:fedcba0987654321",
        },
        "tests": {
            "test_node_ids": [f"test_{feature_key}"],
            "passed_count": 10,
        },
        "security": {
            "sandbox_policy_id": "SANDBOX-CONF",
            "gateway_verdict": "PASS",
        },
        "documentation": {
            "doc_node_ids": [f"doc:{feature_key}"],
            "doc_drift_status": "PASS",
        },
        "evidence": {
            "evidence_ids": [f"EVD-{feature_key.upper()}-01"],
        },
        "git": {
            "base_commit": "c000",
            "head_commit": "c001",
            "branch": "main",
        },
        "verification": {
            "verification_id": f"VERIF-{feature_key.upper()}-01",
            "converged": converged,
        },
    }


def test_12_dimensions_exact_catalog():
    """Level 14: Verifies the exact list of 12 dimensions required by CORE-CONTRACT-010."""
    expected = (
        "requirement", "spec", "architecture", "dependencies",
        "contracts", "implementation", "tests", "security",
        "documentation", "evidence", "git", "verification"
    )
    assert REQUIRED_DIMENSIONS == expected


def test_passport_compilation_all_15_features(tmp_path: Path):
    """Level 14: Successfully compiles and stamps valid 12-dimensional passports for all 15 features."""
    manager = FeaturePassportManager(tmp_path)
    features = [
        "core_state", "pipeline", "task", "context_router",
        "graph_store", "verifier", "event_log", "security_sandbox",
        "harness_adapter", "subagents", "memory_gating", "skill_gateway",
        "feature_passport", "evolution_pipeline", "observability_progress"
    ]

    for feat in features:
        dims = make_test_dimensions(feat, converged=True)
        passport = manager.compile_passport(feat, dims, auto_stamp=True)
        assert passport["status"] == "CONVERGED"
        assert len(passport["dimensions"]) == 12
        assert (tmp_path / ".eidos" / "passports" / f"{feat}.json").exists()


def test_missing_dimension_rejected(tmp_path: Path):
    """Level 14: Omitting any required dimension raises ContractViolationError."""
    manager = FeaturePassportManager(tmp_path)
    dims = make_test_dimensions("incomplete", converged=True)
    del dims["documentation"]  # Omit 1 of 12 dimensions

    with pytest.raises(ContractViolationError) as exc_info:
        manager.compile_passport("incomplete_feature", dims)

    assert "missing required dimensions: documentation" in str(exc_info.value)
