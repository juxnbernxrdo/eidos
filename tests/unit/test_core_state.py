"""Unit tests for SPEC-001: Core State Reducer & Event Fold Engine."""

import pytest
from eidos.core.state import (
    create_initial_state,
    reduce_event,
    fold_events,
    compute_state_hash,
    TaskState,
)
from eidos.core.exceptions import ContractViolationError, InvalidInputError


def test_empty_event_stream():
    """Fold(S_0, []) must return S_0 identically."""
    s0 = create_initial_state("PROJ-TEST", "TestProject")
    folded = fold_events(s0, [])
    assert folded["project"]["project_id"] == "PROJ-TEST"
    assert folded["event_count"] == 0
    assert folded["last_event_id"] is None


def test_deterministic_fold_ac_001_01():
    """AC-001-01: Evaluating Fold(S_0, [e_1...e_10]) twice produces identical state & hash."""
    s0 = create_initial_state("PROJ-TEST", "TestProject")
    events = [
        {
            "event_id": f"EVT-{i:03d}",
            "event_type": "SESSION_UPDATED" if i > 1 else "PROJECT_INITIALIZED",
            "timestamp": f"2026-09-30T12:{i:02d}:00Z",
            "git_commit": f"commit_{i}",
            "payload": {"tokens": 100, "cost_usd": 0.002} if i > 1 else {"name": "InitializedProject"},
        }
        for i in range(1, 11)
    ]

    run_1 = fold_events(s0, events)
    run_2 = fold_events(s0, events)

    assert run_1["state_hash"] == run_2["state_hash"]
    assert run_1["event_count"] == 10
    assert run_1["last_event_id"] == "EVT-010"
    assert run_1["git_head"] == "commit_10"
    assert run_1["active_session"]["tokens_consumed"] == 900


def test_illegal_transition_rejection_ac_001_02():
    """AC-001-02: Applying TASK_CONVERGED to unverified task raises CONTRACT_VIOLATION."""
    s0 = create_initial_state()
    event_task_create = {
        "event_id": "EVT-001",
        "event_type": "TASK_CREATED",
        "timestamp": "2026-09-30T12:00:00Z",
        "git_commit": "abc1234",
        "payload": {
            "task_id": "TASK-001",
            "title": "Unverified Task",
            "status": "PENDING",
        },
    }
    state = reduce_event(s0, event_task_create)
    assert state["tasks"]["TASK-001"]["status"] == "PENDING"

    # Attempt illegal transition directly to CONVERGED without verification
    event_illegal_converged = {
        "event_id": "EVT-002",
        "event_type": "TASK_CONVERGED",
        "timestamp": "2026-09-30T12:01:00Z",
        "git_commit": "abc1234",
        "payload": {"task_id": "TASK-001"},
    }

    with pytest.raises(ContractViolationError) as exc_info:
        reduce_event(state, event_illegal_converged)

    assert "Cannot mark task 'TASK-001' as CONVERGED without passing verification" in str(exc_info.value)
    # State remains unchanged
    assert state["tasks"]["TASK-001"]["status"] == "PENDING"


def test_monotonicity_rejection():
    """Re-applying an already applied event raises ContractViolationError."""
    s0 = create_initial_state()
    evt = {
        "event_id": "EVT-001",
        "event_type": "SESSION_STARTED",
        "timestamp": "2026-09-30T12:00:00Z",
        "git_commit": "abc1234",
        "payload": {"session_id": "SESSION-1"},
    }
    s1 = reduce_event(s0, evt)
    with pytest.raises(ContractViolationError) as exc_info:
        reduce_event(s1, evt)
    assert "Monotonicity violation" in str(exc_info.value)


def test_task_verification_and_convergence_lifecycle():
    """Valid verification leads to CONVERGED state and allows feature passport stamping."""
    s0 = create_initial_state()
    events = [
        {
            "event_id": "EVT-001",
            "event_type": "TASK_CREATED",
            "timestamp": "2026-09-30T12:00:00Z",
            "git_commit": "commit_1",
            "payload": {"task_id": "TASK-001", "title": "Test Task"},
        },
        {
            "event_id": "EVT-002",
            "event_type": "VERIFICATION_COMPLETED",
            "timestamp": "2026-09-30T12:01:00Z",
            "git_commit": "commit_2",
            "payload": {
                "verification_id": "VERIF-001",
                "task_id": "TASK-001",
                "converged": True,
                "test_passed": 5,
                "test_failed": 0,
            },
        },
        {
            "event_id": "EVT-003",
            "event_type": "FEATURE_PASSPORT_STAMPED",
            "timestamp": "2026-09-30T12:02:00Z",
            "git_commit": "commit_2",
            "payload": {
                "passport_id": "PASS-001",
                "task_id": "TASK-001",
                "passport_hash": "sha256:abcdef",
            },
        },
    ]

    final_state = fold_events(s0, events)
    assert final_state["tasks"]["TASK-001"]["status"] == TaskState.CONVERGED.value
    assert final_state["tasks"]["TASK-001"]["converged"] is True
    assert "PASS-001" in final_state["passports"]
    assert final_state["event_count"] == 3
