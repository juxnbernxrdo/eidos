"""Level 7 Verification Suite: Comprehensive Machine Invariant Verification (ARCH, SEC, STATE, PROV)."""

from pathlib import Path
import pytest
from eidos.core.exceptions import (
    ContractViolationError,
    PermissionDeniedError,
    VerificationError,
)
from eidos.core.state import create_initial_state, reduce_event
from eidos.intelligence.invariants import check_invariants, load_default_invariants
from eidos.security.permissions import canonicalize_and_confine_path
from eidos.security.supervisor import SandboxSupervisor
from eidos.progress.passport import FeaturePassportManager


def test_arch_001_and_arch_002_live_ast():
    """Level 7: Machine AST evaluation of ARCH-001 (core layer isolation) and ARCH-002 (contracts independence)."""
    repo_root = Path(__file__).parent.parent.parent
    violations = check_invariants(repo_root)
    assert len(violations) == 0, f"Architectural invariant violations found: {violations}"


def test_inv_001_zero_model_provider_dependencies():
    """Level 7 [INV-001]: Core domain has zero dependencies on proprietary model providers (openai, anthropic, google)."""
    repo_root = Path(__file__).parent.parent.parent
    core_dir = repo_root / "src" / "eidos" / "core"
    forbidden_providers = ("openai", "anthropic", "google", "mistral", "cohere", "langchain")

    for f in core_dir.rglob("*.py"):
        text = f.read_text(encoding="utf-8").lower()
        for prov in forbidden_providers:
            assert f"import {prov}" not in text, f"Forbidden provider import '{prov}' in {f.name}"
            assert f"from {prov}" not in text, f"Forbidden provider import '{prov}' in {f.name}"


def test_inv_002_path_confinement_physics(tmp_path: Path):
    """Level 7 [INV-002]: Zero file access or traversal outside the designated workspace root."""
    inside = tmp_path / "inside.txt"
    inside.write_text("ok", encoding="utf-8")
    assert canonicalize_and_confine_path(inside, tmp_path) == inside.resolve()

    outside = tmp_path / ".." / "outside.txt"
    with pytest.raises(PermissionDeniedError) as exc_info:
        canonicalize_and_confine_path(outside, tmp_path)
    assert exc_info.value.details.get("invariant") == "INV-002"


def test_inv_003_verification_before_done():
    """Level 7 [INV-003]: Cannot grant CONVERGED status without passing machine verification."""
    s0 = create_initial_state()
    s1 = reduce_event(s0, {
        "event_id": "EVT-01",
        "event_type": "TASK_CREATED",
        "timestamp": "2026-09-30T10:00:00Z",
        "payload": {"task_id": "TASK-INV-3", "status": "PENDING"},
    })

    with pytest.raises(ContractViolationError) as exc:
        reduce_event(s1, {
            "event_id": "EVT-02",
            "event_type": "TASK_CONVERGED",
            "timestamp": "2026-09-30T10:01:00Z",
            "payload": {"task_id": "TASK-INV-3"},
        })
    assert "Cannot mark task 'TASK-INV-3' as CONVERGED without passing verification" in str(exc.value)


def test_inv_007_monotonic_event_reduction():
    """Level 7 [INV-007]: Re-application of an existing event ID raises CONTRACT_VIOLATION."""
    s0 = create_initial_state()
    evt = {"event_id": "EVT-01", "event_type": "SESSION_STARTED", "timestamp": "2026-09-30T10:00:00Z", "payload": {}}
    s1 = reduce_event(s0, evt)
    with pytest.raises(ContractViolationError):
        reduce_event(s1, evt)


def test_inv_008_default_deny_policy_as_physics(tmp_path: Path):
    """Level 7 [INV-008]: Default-deny security sandbox blocks write when scope is READ_ONLY."""
    supervisor = SandboxSupervisor(tmp_path)
    # Default supervisor grant is WORKTREE_ONLY; set up a READ_ONLY grant
    supervisor.grant["filesystem"]["scope"] = "READ_ONLY"

    with pytest.raises(PermissionDeniedError):
        supervisor.validate_write(tmp_path / "src" / "test.py")


def test_inv_009_epistemic_ground_truth_precedence(tmp_path: Path):
    """Level 7 [INV-009]: EXTRACTED ground truth facts strictly override INFERRED claims."""
    from eidos.graph.engine import RepositoryGraphEngine
    from eidos.contracts.models import EdgeRelation, EpistemicType

    engine = RepositoryGraphEngine(tmp_path)
    engine.graph.add_edge("file:a.py", "fn:foo", relation=EdgeRelation.DEFINED_BY.value, epistemic_provenance=EpistemicType.EXTRACTED.value, confidence=1.0)

    # Propose conflicting inferred definition from b.py
    outcome = engine.propose_edge("file:b.py", "fn:foo", relation=EdgeRelation.DEFINED_BY.value, epistemic_provenance=EpistemicType.INFERRED.value)

    assert outcome["status"] == "QUARANTINED"
    assert outcome["relation"] == EdgeRelation.CONFLICTS_WITH.value
    # Ground truth remains untouched
    assert engine.graph.edges["file:a.py", "fn:foo"]["epistemic_provenance"] == EpistemicType.EXTRACTED.value
