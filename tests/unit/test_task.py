"""Unit tests for SPEC-003: Task Lifecycle & Bounded Transitions."""

from pathlib import Path
import pytest
from eidos.core.exceptions import ContractViolationError, PermissionDeniedError
from eidos.orchestration.task import TaskRecord, TaskStatus


class MockVerificationResult:
    def __init__(self, converged: bool):
        self.converged = converged


def test_task_lifecycle_transitions(tmp_path: Path):
    """Happy path transition through CREATED -> PLANNED -> READY -> RUNNING -> VERIFYING -> CONVERGED."""
    task = TaskRecord(
        task_id="TASK-001",
        spec_id="SPEC-001",
        title="Test Task",
        objective="Implement feature",
        workspace_root=tmp_path,
        target_files=["src/main.py"],
        allowed_tools=["view_file"],
        acceptance_criteria=["Passes all checks"],
    )
    assert task.status == TaskStatus.CREATED

    # CREATED -> PLANNED
    task.transition_to(TaskStatus.PLANNED)
    assert task.status == TaskStatus.PLANNED

    # PLANNED -> READY (requires assigned_agent_id)
    task.assigned_agent_id = "AGENT-01"
    task.transition_to(TaskStatus.READY)
    assert task.status == TaskStatus.READY

    # READY -> RUNNING
    task.transition_to(TaskStatus.RUNNING)
    assert task.status == TaskStatus.RUNNING

    # RUNNING -> VERIFYING
    task.transition_to(TaskStatus.VERIFYING)
    assert task.status == TaskStatus.VERIFYING

    # VERIFYING -> CONVERGED (requires passing verification)
    passing_verif = MockVerificationResult(converged=True)
    task.transition_to(TaskStatus.CONVERGED, verification_result=passing_verif)
    assert task.status == TaskStatus.CONVERGED
    assert task.completion_timestamp is not None


def test_illegal_unconverged_transition_rejection(tmp_path: Path):
    """Cannot transition to CONVERGED if verification failed."""
    task = TaskRecord(
        task_id="TASK-002",
        spec_id="SPEC-001",
        title="Failing Task",
        objective="Fix bug",
        workspace_root=tmp_path,
        target_files=["src/bug.py"],
        acceptance_criteria=["Must pass"],
        assigned_agent_id="AGENT-02",
    )
    task.transition_to(TaskStatus.PLANNED)
    task.transition_to(TaskStatus.READY)
    task.transition_to(TaskStatus.RUNNING)
    task.transition_to(TaskStatus.VERIFYING)

    failing_verif = MockVerificationResult(converged=False)
    with pytest.raises(ContractViolationError) as exc_info:
        task.transition_to(TaskStatus.CONVERGED, verification_result=failing_verif)

    assert "Cannot transition task 'TASK-002' to CONVERGED without passing verification" in str(exc_info.value)
    assert task.status == TaskStatus.VERIFYING


def test_target_files_confinement(tmp_path: Path):
    """Target files outside workspace root are rejected at creation."""
    outside_file = tmp_path / ".." / "external.py"
    with pytest.raises(PermissionDeniedError):
        TaskRecord(
            task_id="TASK-003",
            spec_id="SPEC-001",
            title="External Task",
            objective="Touch outside",
            workspace_root=tmp_path,
            target_files=[str(outside_file)],
        )
