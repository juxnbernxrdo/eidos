"""Deterministic pure core state reducer and event folding engine.

Implements SPEC-001 (Core State Reducer & Event Fold Engine) and satisfies
REQ-CORE-001 and REQ-CORE-002:
    S_t = Fold(S_0, [e_1, ..., e_t])
"""

import copy
import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from eidos.core.exceptions import (
    ContractViolationError,
    InvalidInputError,
)


class TaskState(str, Enum):
    """Pipeline and task lifecycle states."""
    # Pipeline stages
    DISCOVERY = "DISCOVERY"
    SPECIFY = "SPECIFY"
    PLAN = "PLAN"
    IMPLEMENT = "IMPLEMENT"
    VERIFY = "VERIFY"
    REPAIR = "REPAIR"
    CONVERGED = "CONVERGED"
    DONE = "DONE"
    ESCALATED = "ESCALATED"
    # Task specific lifecycle states
    CREATED = "CREATED"
    PENDING = "PENDING"
    PLANNED = "PLANNED"
    READY = "READY"
    RUNNING = "RUNNING"
    IN_PROGRESS = "IN_PROGRESS"
    VERIFYING = "VERIFYING"
    REPAIRING = "REPAIRING"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


# Valid pipeline state transitions
VALID_TRANSITIONS: dict[TaskState, list[TaskState]] = {
    TaskState.DISCOVERY: [TaskState.SPECIFY],
    TaskState.SPECIFY: [TaskState.PLAN],
    TaskState.PLAN: [TaskState.IMPLEMENT],
    TaskState.IMPLEMENT: [TaskState.VERIFY],
    TaskState.VERIFY: [TaskState.CONVERGED, TaskState.REPAIR],
    TaskState.REPAIR: [TaskState.VERIFY, TaskState.ESCALATED],
    TaskState.CONVERGED: [TaskState.DONE],
    TaskState.DONE: [],
    TaskState.ESCALATED: [TaskState.SPECIFY, TaskState.PLAN, TaskState.IMPLEMENT],
    # Atomic Task lifecycle transitions (SPEC-003)
    TaskState.CREATED: [TaskState.PLANNED, TaskState.CANCELLED],
    TaskState.PENDING: [TaskState.IN_PROGRESS, TaskState.RUNNING, TaskState.CANCELLED],
    TaskState.PLANNED: [TaskState.READY, TaskState.CANCELLED],
    TaskState.READY: [TaskState.RUNNING, TaskState.IN_PROGRESS, TaskState.CANCELLED],
    TaskState.RUNNING: [TaskState.VERIFYING, TaskState.FAILED, TaskState.ESCALATED, TaskState.CANCELLED],
    TaskState.IN_PROGRESS: [TaskState.VERIFYING, TaskState.VERIFY, TaskState.FAILED, TaskState.ESCALATED, TaskState.CANCELLED],
    TaskState.VERIFYING: [TaskState.CONVERGED, TaskState.VERIFIED, TaskState.REPAIRING, TaskState.REPAIR, TaskState.FAILED, TaskState.ESCALATED],
    TaskState.REPAIRING: [TaskState.RUNNING, TaskState.IN_PROGRESS, TaskState.VERIFYING, TaskState.ESCALATED, TaskState.FAILED],
    TaskState.VERIFIED: [TaskState.CONVERGED, TaskState.DONE],
    TaskState.FAILED: [],
    TaskState.CANCELLED: [],
}


def can_transition(current: TaskState | str, target: TaskState | str) -> bool:
    """Checks if a transition between two states is valid."""
    try:
        curr_enum = TaskState(current) if isinstance(current, str) else current
        tgt_enum = TaskState(target) if isinstance(target, str) else target
    except ValueError:
        return False
    return tgt_enum in VALID_TRANSITIONS.get(curr_enum, [])


def create_initial_state(project_id: str = "PROJ-DEFAULT", name: str = "EidosProject") -> dict[str, Any]:
    """Generates the clean initial baseline state S_0."""
    return {
        "project": {
            "project_id": project_id,
            "name": name,
            "lifecycle_state": "discovery",
            "primary_harness": "antigravity",
            "documentation_language": "en",
        },
        "active_session": {
            "session_id": "SESSION-INITIAL",
            "operator": "system",
            "tokens_consumed": 0,
            "total_cost_usd": 0.0,
            "active_tasks": [],
        },
        "tasks": {},
        "specs": {},
        "passports": {},
        "verifications": {},
        "history": [],
        "last_event_id": None,
        "git_head": "HEAD",
        "event_count": 0,
        "state_hash": "",
    }


def compute_state_hash(state: dict[str, Any]) -> str:
    """Computes a deterministic SHA-256 digest of the state."""
    state_copy = {k: v for k, v in state.items() if k != "state_hash"}
    canonical_json = json.dumps(state_copy, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def reduce_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    """Pure mathematical event reducer: (S_{t-1}, e_t) -> S_t.

    Raises:
        InvalidInputError: If event format is invalid.
        ContractViolationError: If event violates ordering, monotonicity, or state invariants.
    """
    if not isinstance(event, dict):
        raise InvalidInputError("Event must be a dictionary conforming to EVENT-CONTRACT-001")

    event_id = event.get("event_id")
    event_type = event.get("event_type")
    payload = event.get("payload", {})
    git_commit = event.get("git_commit", "HEAD")

    if not event_id or not event_type:
        raise InvalidInputError("Event requires 'event_id' and 'event_type'")

    # Invariant INV-007: Event reduction is strictly monotonic
    last_event_id = state.get("last_event_id")
    if last_event_id is not None and event_id == last_event_id:
        raise ContractViolationError(
            f"Monotonicity violation: Event '{event_id}' has already been applied",
            details={"last_event_id": last_event_id, "event_id": event_id},
        )

    # Deep-copy to guarantee pure functional transformation
    new_state = copy.deepcopy(state)

    if event_type == "PROJECT_INITIALIZED":
        project_data = payload.get("project") or payload
        for key in ("project_id", "name", "lifecycle_state", "primary_harness", "documentation_language"):
            if key in project_data:
                new_state["project"][key] = project_data[key]

    elif event_type == "SESSION_STARTED":
        session_id = payload.get("session_id", event.get("session_id", "SESSION-DEFAULT"))
        new_state["active_session"]["session_id"] = session_id
        if "operator" in payload:
            new_state["active_session"]["operator"] = payload["operator"]

    elif event_type in ("SESSION_UPDATED", "METRICS_RECORDED"):
        if "tokens" in payload:
            new_state["active_session"]["tokens_consumed"] += payload["tokens"]
        if "cost_usd" in payload:
            new_state["active_session"]["total_cost_usd"] += payload["cost_usd"]

    elif event_type == "SPEC_CREATED":
        spec_id = payload.get("spec_id")
        if not spec_id:
            raise InvalidInputError("SPEC_CREATED requires 'spec_id' in payload")
        new_state["specs"][spec_id] = {
            "spec_id": spec_id,
            "title": payload.get("title", ""),
            "status": payload.get("status", "draft"),
            "requirements": payload.get("requirements", []),
            "created_at": event.get("timestamp"),
        }

    elif event_type == "TASK_CREATED":
        task_id = payload.get("task_id")
        if not task_id:
            raise InvalidInputError("TASK_CREATED requires 'task_id' in payload")
        status = payload.get("status", TaskState.PENDING.value)
        new_state["tasks"][task_id] = {
            "task_id": task_id,
            "spec_id": payload.get("spec_id", ""),
            "title": payload.get("title", ""),
            "objective": payload.get("objective", ""),
            "status": status,
            "target_files": payload.get("target_files", []),
            "allowed_tools": payload.get("allowed_tools", []),
            "acceptance_criteria": payload.get("acceptance_criteria", []),
            "attempts": 0,
            "repairs": 0,
            "last_verification_id": None,
            "converged": False,
        }

    elif event_type == "TASK_TRANSITION":
        task_id = payload.get("task_id")
        target_status = payload.get("target_status")
        if not task_id or not target_status:
            raise InvalidInputError("TASK_TRANSITION requires 'task_id' and 'target_status'")
        if task_id not in new_state["tasks"]:
            raise ContractViolationError(f"Task '{task_id}' does not exist in state")

        current_status = new_state["tasks"][task_id]["status"]
        if not can_transition(current_status, target_status):
            raise ContractViolationError(
                f"Illegal task transition from '{current_status}' to '{target_status}'",
                details={"task_id": task_id, "current": current_status, "target": target_status},
            )
        new_state["tasks"][task_id]["status"] = target_status

    elif event_type == "VERIFICATION_COMPLETED":
        verif_id = payload.get("verification_id", f"VERIF-{event_id}")
        task_id = payload.get("task_id")
        converged = bool(payload.get("converged", False))
        new_state["verifications"][verif_id] = {
            "verification_id": verif_id,
            "task_id": task_id,
            "converged": converged,
            "test_passed": payload.get("test_passed", 0),
            "test_failed": payload.get("test_failed", 0),
            "invariant_violations": payload.get("invariant_violations", []),
            "timestamp": event.get("timestamp"),
        }
        if task_id and task_id in new_state["tasks"]:
            task = new_state["tasks"][task_id]
            task["last_verification_id"] = verif_id
            task["attempts"] = task.get("attempts", 0) + 1
            if converged:
                task["converged"] = True
                task["status"] = TaskState.CONVERGED.value
            else:
                task["repairs"] = task.get("repairs", 0) + 1
                task["status"] = TaskState.REPAIR.value if can_transition(task["status"], TaskState.REPAIR.value) else TaskState.REPAIRING.value

    elif event_type == "TASK_CONVERGED":
        task_id = payload.get("task_id")
        if not task_id or task_id not in new_state["tasks"]:
            raise ContractViolationError(f"Task '{task_id}' does not exist in state")

        task = new_state["tasks"][task_id]
        # Invariant INV-003: Task cannot transition to CONVERGED without a passing VerificationResult
        if not task.get("converged") and not payload.get("verified", False):
            raise ContractViolationError(
                f"Cannot mark task '{task_id}' as CONVERGED without passing verification",
                details={"task_id": task_id, "current_status": task["status"]},
            )
        task["status"] = TaskState.CONVERGED.value
        task["converged"] = True

    elif event_type in ("TASK_FAILED", "TASK_ESCALATED"):
        task_id = payload.get("task_id")
        if not task_id or task_id not in new_state["tasks"]:
            raise ContractViolationError(f"Task '{task_id}' does not exist in state")
        target_state = TaskState.FAILED.value if event_type == "TASK_FAILED" else TaskState.ESCALATED.value
        new_state["tasks"][task_id]["status"] = target_state

    elif event_type == "FEATURE_PASSPORT_STAMPED":
        passport_id = payload.get("passport_id")
        task_id = payload.get("task_id")
        if not passport_id or not task_id:
            raise InvalidInputError("FEATURE_PASSPORT_STAMPED requires 'passport_id' and 'task_id'")
        if task_id not in new_state["tasks"] or not new_state["tasks"][task_id].get("converged"):
            raise ContractViolationError(
                f"Cannot stamp Feature Passport for unconverged task '{task_id}'",
                details={"task_id": task_id},
            )
        new_state["passports"][passport_id] = {
            "passport_id": passport_id,
            "task_id": task_id,
            "stamped_at": event.get("timestamp"),
            "hash": payload.get("passport_hash", ""),
        }

    elif event_type == "SUPERSEDING_CORRECTION":
        ref_event_id = payload.get("supersedes_event_id")
        if not ref_event_id:
            raise InvalidInputError("SUPERSEDING_CORRECTION requires 'supersedes_event_id'")
        # Preserves event log; records correction metadata
        new_state.setdefault("superseded_events", {})[ref_event_id] = {
            "correction_event_id": event_id,
            "reason": payload.get("reason", "manual_correction"),
            "timestamp": event.get("timestamp"),
        }

    else:
        # Generic event logging to history
        pass

    # Update metadata
    new_state["last_event_id"] = event_id
    new_state["git_head"] = git_commit
    new_state["event_count"] = new_state.get("event_count", 0) + 1
    new_state["history"].append(event_id)
    new_state["state_hash"] = compute_state_hash(new_state)

    return new_state


def fold_events(initial_state: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    """Pure left-fold over a sequence of events: S_t = Fold(S_0, [e_1 ... e_t])."""
    current_state = copy.deepcopy(initial_state)
    if not current_state.get("state_hash"):
        current_state["state_hash"] = compute_state_hash(current_state)

    for event in events:
        current_state = reduce_event(current_state, event)

    return current_state
