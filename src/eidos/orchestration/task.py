"""Task Lifecycle & Bounded Transitions.

Implements SPEC-003 (Task Lifecycle & Bounded Transitions) and satisfies
REQ-TASK-001, REQ-TASK-002, AC-003-01, AC-003-02:
    - 10 formal lifecycle states
    - Atomic transition validation and history tracking
    - Enforcement of preconditions, target file bounds, and turn limits
"""

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from eidos.core.exceptions import (
    ContractViolationError,
    InvalidInputError,
    PermissionDeniedError,
)
from eidos.security.permissions import canonicalize_and_confine_path


class TaskStatus(str, Enum):
    CREATED = "CREATED"
    PLANNED = "PLANNED"
    READY = "READY"
    RUNNING = "RUNNING"
    VERIFYING = "VERIFYING"
    REPAIRING = "REPAIRING"
    CONVERGED = "CONVERGED"
    FAILED = "FAILED"
    ESCALATED = "ESCALATED"
    CANCELLED = "CANCELLED"


# Allowed state transitions per SPEC-003 §8
TASK_TRANSITIONS: dict[TaskStatus, list[TaskStatus]] = {
    TaskStatus.CREATED: [TaskStatus.PLANNED, TaskStatus.CANCELLED],
    TaskStatus.PLANNED: [TaskStatus.READY, TaskStatus.CANCELLED],
    TaskStatus.READY: [TaskStatus.RUNNING, TaskStatus.CANCELLED],
    TaskStatus.RUNNING: [TaskStatus.VERIFYING, TaskStatus.FAILED, TaskStatus.ESCALATED, TaskStatus.CANCELLED],
    TaskStatus.VERIFYING: [TaskStatus.CONVERGED, TaskStatus.REPAIRING, TaskStatus.FAILED, TaskStatus.ESCALATED],
    TaskStatus.REPAIRING: [TaskStatus.RUNNING, TaskStatus.VERIFYING, TaskStatus.FAILED, TaskStatus.ESCALATED],
    TaskStatus.CONVERGED: [],
    TaskStatus.FAILED: [],
    TaskStatus.ESCALATED: [],
    TaskStatus.CANCELLED: [],
}


class TaskRecord:
    """Encapsulates a contract-bounded task unit conforming to CORE-CONTRACT-002."""

    def __init__(
        self,
        task_id: str,
        spec_id: str,
        title: str,
        objective: str,
        workspace_root: Path,
        target_files: list[str] | None = None,
        allowed_tools: list[str] | None = None,
        acceptance_criteria: list[str] | None = None,
        assigned_agent_id: str | None = None,
        max_turns: int = 30,
        max_repair_k: int = 5,
    ):
        if not task_id or not spec_id or not title or not objective:
            raise InvalidInputError("task_id, spec_id, title, and objective are mandatory")

        self.workspace_root = workspace_root.resolve()
        self.task_id = task_id
        self.spec_id = spec_id
        self.title = title
        self.objective = objective
        self.target_files = target_files or []
        self.allowed_tools = allowed_tools or ["view_file", "edit_file", "run_tests"]
        self.acceptance_criteria = acceptance_criteria or ["Pass unit tests"]
        self.assigned_agent_id = assigned_agent_id
        self.max_turns = max_turns
        self.max_repair_k = max_repair_k

        self.status = TaskStatus.CREATED
        self.current_turns = 0
        self.convergence_attempts = 0
        self.completion_timestamp: str | None = None
        self.history: list[dict[str, Any]] = [
            {"from": None, "to": TaskStatus.CREATED.value, "timestamp": datetime.now(timezone.utc).isoformat()}
        ]

        # Verify initial target files bounds if provided
        for tf in self.target_files:
            canonicalize_and_confine_path(tf, self.workspace_root)

    def transition_to(
        self,
        target_status: TaskStatus | str,
        verification_result: Any | None = None,
        operator_reason: str | None = None,
    ) -> None:
        """Transitions task to target_status after validating formal preconditions."""
        tgt = TaskStatus(target_status) if isinstance(target_status, str) else target_status
        allowed = TASK_TRANSITIONS.get(self.status, [])

        if tgt not in allowed:
            raise ContractViolationError(
                f"Illegal task transition from '{self.status.value}' to '{tgt.value}'",
                details={
                    "task_id": self.task_id,
                    "current_status": self.status.value,
                    "target_status": tgt.value,
                    "allowed_transitions": [s.value for s in allowed],
                },
            )

        # Precondition checks per state
        if tgt == TaskStatus.PLANNED:
            if not self.target_files or not self.acceptance_criteria:
                raise ContractViolationError("Transition to PLANNED requires target_files and acceptance_criteria")

        elif tgt == TaskStatus.READY:
            if not self.assigned_agent_id:
                raise ContractViolationError("Transition to READY requires assigned_agent_id")

        elif tgt == TaskStatus.RUNNING:
            if self.current_turns >= self.max_turns:
                raise ContractViolationError(f"Turn limit {self.max_turns} reached; cannot transition to RUNNING")

        elif tgt == TaskStatus.CONVERGED:
            # Invariant INV-003: CONVERGED requires passing verification
            if not verification_result or not getattr(verification_result, "converged", False):
                raise ContractViolationError(
                    f"Cannot transition task '{self.task_id}' to CONVERGED without passing verification",
                    details={"task_id": self.task_id, "status": self.status.value},
                )
            self.completion_timestamp = datetime.now(timezone.utc).isoformat()

        elif tgt == TaskStatus.REPAIRING:
            self.convergence_attempts += 1
            if self.convergence_attempts >= self.max_repair_k:
                raise ContractViolationError(
                    f"Repair bounds exceeded (attempts {self.convergence_attempts} >= K={self.max_repair_k}); must escalate"
                )

        # Apply state transition
        prev_status = self.status
        self.status = tgt
        self.history.append({
            "from": prev_status.value,
            "to": tgt.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "reason": operator_reason or "",
        })

    def to_contract_dict(self) -> dict[str, Any]:
        """Serializes task record conforming to CORE-CONTRACT-002."""
        return {
            "contract_id": "CORE-CONTRACT-002",
            "contract_version": "1.0.0",
            "task_id": self.task_id,
            "spec_id": self.spec_id,
            "title": self.title,
            "objective": self.objective,
            "status": self.status.value,
            "target_files": self.target_files,
            "allowed_tools": self.allowed_tools,
            "acceptance_criteria": self.acceptance_criteria,
            "assigned_agent_id": self.assigned_agent_id or "AGENT-UNASSIGNED",
            "max_turns": self.max_turns,
            "convergence_attempts": self.convergence_attempts,
        }
