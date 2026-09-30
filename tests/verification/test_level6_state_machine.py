"""Level 6 Verification Suite: State Machine Determinism, Checkpoint Resumption & Stress Replay."""

from pathlib import Path
from eidos.core.state import create_initial_state, fold_events, reduce_event, compute_state_hash, TaskState
from eidos.core.exceptions import ContractViolationError


def test_state_fold_stress_and_determinism():
    """Level 6: Deterministic fold over 100 events yields identical SHA-256 hash across runs."""
    s0 = create_initial_state(project_id="PROJ-STRESS", name="StressProject")

    events = []
    # 1. Project initialized
    events.append({
        "event_id": "EVT-001",
        "event_type": "PROJECT_INITIALIZED",
        "timestamp": "2026-09-30T10:00:00Z",
        "git_commit": "c001",
        "payload": {"name": "StressProject", "lifecycle_state": "active"},
    })

    # 2. 90 session updates with tokens and cost
    for i in range(2, 92):
        events.append({
            "event_id": f"EVT-{i:03d}",
            "event_type": "SESSION_UPDATED",
            "timestamp": f"2026-09-30T10:01:{i%60:02d}Z",
            "git_commit": f"c{i:03d}",
            "payload": {"tokens": 150, "cost_usd": 0.003},
        })

    # 3. Create, verify, and converge a task
    events.extend([
        {
            "event_id": "EVT-092",
            "event_type": "TASK_CREATED",
            "timestamp": "2026-09-30T11:00:00Z",
            "git_commit": "c092",
            "payload": {"task_id": "TASK-STRESS-1", "title": "Stress Task"},
        },
        {
            "event_id": "EVT-093",
            "event_type": "VERIFICATION_COMPLETED",
            "timestamp": "2026-09-30T11:05:00Z",
            "git_commit": "c093",
            "payload": {"task_id": "TASK-STRESS-1", "converged": True, "test_passed": 50},
        },
        {
            "event_id": "EVT-094",
            "event_type": "FEATURE_PASSPORT_STAMPED",
            "timestamp": "2026-09-30T11:10:00Z",
            "git_commit": "c094",
            "payload": {"passport_id": "PASS-STRESS-1", "task_id": "TASK-STRESS-1", "passport_hash": "sha256:abc"},
        },
    ])

    run_1 = fold_events(s0, events)
    run_2 = fold_events(s0, events)

    assert run_1["state_hash"] == run_2["state_hash"]
    assert run_1["event_count"] == len(events)
    assert run_1["active_session"]["tokens_consumed"] == 90 * 150
    assert run_1["tasks"]["TASK-STRESS-1"]["status"] == TaskState.CONVERGED.value


def test_checkpoint_snapshot_resumption():
    """Level 6: S_t can be resumed from intermediate snapshot S_snap by folding remaining events."""
    s0 = create_initial_state()
    events_batch_1 = [
        {
            "event_id": f"EVT-{i:03d}",
            "event_type": "SESSION_UPDATED",
            "timestamp": f"2026-09-30T10:00:{i:02d}Z",
            "git_commit": f"c{i:03d}",
            "payload": {"tokens": 100, "cost_usd": 0.001},
        }
        for i in range(1, 26)
    ]
    events_batch_2 = [
        {
            "event_id": f"EVT-{i:03d}",
            "event_type": "SESSION_UPDATED",
            "timestamp": f"2026-09-30T10:01:{i-25:02d}Z",
            "git_commit": f"c{i:03d}",
            "payload": {"tokens": 200, "cost_usd": 0.002},
        }
        for i in range(26, 51)
    ]

    # Full fold of all 50 events from S_0
    full_run = fold_events(s0, events_batch_1 + events_batch_2)

    # Fold batch 1 to create snapshot S_snap
    snapshot = fold_events(s0, events_batch_1)
    assert snapshot["event_count"] == 25

    # Resume fold from snapshot using batch 2
    resumed_run = fold_events(snapshot, events_batch_2)

    assert resumed_run["event_count"] == 50
    assert resumed_run["state_hash"] == full_run["state_hash"]
    assert resumed_run["active_session"]["tokens_consumed"] == full_run["active_session"]["tokens_consumed"]
