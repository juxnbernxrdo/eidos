"""Finite state machine for Specification-Driven Development in Eidos."""

from enum import Enum

class TaskState(str, Enum):
    DISCOVERY = "DISCOVERY"
    SPECIFY = "SPECIFY"
    PLAN = "PLAN"
    IMPLEMENT = "IMPLEMENT"
    VERIFY = "VERIFY"
    REPAIR = "REPAIR"
    CONVERGED = "CONVERGED"
    DONE = "DONE"
    ESCALATED = "ESCALATED"

# Valid state transitions
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
}

def can_transition(current: TaskState, target: TaskState) -> bool:
    """Checks if a transition between two states is valid."""
    return target in VALID_TRANSITIONS.get(current, [])
