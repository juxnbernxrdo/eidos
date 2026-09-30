"""Phased non-bypassable engineering orchestration pipeline.

Implements SPEC-002 (Phased Orchestration Pipeline) and satisfies
REQ-PIPE-001, REQ-PIPE-002, REQ-PIPE-003, AC-002-01, AC-002-02, AC-002-03:
    - Sequential non-bypassable stage progression
    - Bounded automated repair loop (K <= 5 iterations)
    - Comprehensive diagnostic diff and error summary on escalation
"""

import subprocess
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable

from eidos.core.exceptions import (
    ContractViolationError,
    InvalidInputError,
    VerificationError,
)
from eidos.orchestration.task import TaskRecord, TaskStatus


class PipelineStage(str, Enum):
    DISCOVERY = "DISCOVERY"
    SPECIFY = "SPECIFY"
    PLAN = "PLAN"
    IMPLEMENT = "IMPLEMENT"
    VERIFY = "VERIFY"
    REPAIR = "REPAIR"
    CONVERGED = "CONVERGED"
    ESCALATED = "ESCALATED"
    DONE = "DONE"


PIPELINE_TRANSITIONS: dict[PipelineStage, list[PipelineStage]] = {
    PipelineStage.DISCOVERY: [PipelineStage.SPECIFY],
    PipelineStage.SPECIFY: [PipelineStage.PLAN],
    PipelineStage.PLAN: [PipelineStage.IMPLEMENT],
    PipelineStage.IMPLEMENT: [PipelineStage.VERIFY],
    PipelineStage.VERIFY: [PipelineStage.CONVERGED, PipelineStage.REPAIR, PipelineStage.ESCALATED],
    PipelineStage.REPAIR: [PipelineStage.VERIFY, PipelineStage.ESCALATED],
    PipelineStage.CONVERGED: [PipelineStage.DONE],
    PipelineStage.DONE: [],
    PipelineStage.ESCALATED: [PipelineStage.SPECIFY, PipelineStage.PLAN, PipelineStage.IMPLEMENT],
}


class PhasedPipeline:
    """Coordinates non-bypassable sequential progression across engineering phases."""

    def __init__(self, workspace_root: Path, max_repair_k: int = 5):
        self.workspace_root = workspace_root.resolve()
        self.max_repair_k = max_repair_k
        self.current_stage = PipelineStage.DISCOVERY
        self.stage_history: list[dict[str, Any]] = [
            {"stage": self.current_stage.value, "timestamp": datetime.now(timezone.utc).isoformat()}
        ]

    def advance_stage(self, target_stage: PipelineStage | str) -> None:
        """Advances pipeline to target_stage verifying strict sequential progression (AC-002-01)."""
        tgt = PipelineStage(target_stage) if isinstance(target_stage, str) else target_stage
        allowed = PIPELINE_TRANSITIONS.get(self.current_stage, [])

        if tgt not in allowed:
            raise ContractViolationError(
                f"Non-bypassable gating violation: Cannot advance pipeline from '{self.current_stage.value}' to '{tgt.value}'",
                details={
                    "current_stage": self.current_stage.value,
                    "target_stage": tgt.value,
                    "allowed_transitions": [s.value for s in allowed],
                    "invariant": "INV-001",
                },
            )

        self.current_stage = tgt
        self.stage_history.append({
            "stage": tgt.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def capture_diagnostic_diff(self) -> str:
        """Captures Git working tree diff for escalation payloads (AC-002-03)."""
        try:
            res = subprocess.run(
                ["git", "diff", "HEAD"],
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=10,
            )
            diff = res.stdout.strip()
            return diff if diff else "# [No uncommitted changes in working tree]"
        except Exception as e:
            return f"# [Error capturing git diff: {e}]"

    def execute_bounded_repair_loop(
        self,
        task: TaskRecord,
        verifier_fn: Callable[[int], Any],
        repair_fn: Callable[[str], None],
    ) -> dict[str, Any]:
        """Executes bounded repair loop up to K iterations (AC-002-02, AC-002-03)."""
        attempt = 1

        while attempt <= self.max_repair_k:
            # 1. Run verification
            self.current_stage = PipelineStage.VERIFY
            verif_result = verifier_fn(attempt)

            if getattr(verif_result, "converged", False):
                self.current_stage = PipelineStage.CONVERGED
                task.status = TaskStatus.CONVERGED
                return {
                    "verdict": "CONVERGED",
                    "converged": True,
                    "attempts": attempt,
                    "verification_result": verif_result,
                }

            # 2. Check exhaustion bound
            if attempt >= self.max_repair_k:
                # AC-002-02: Strict upper bound at K iterations; transitions to ESCALATED
                self.current_stage = PipelineStage.ESCALATED
                task.status = TaskStatus.ESCALATED
                diff = self.capture_diagnostic_diff()
                oracle_trace = getattr(verif_result, "oracle_trace", "") or str(verif_result)
                
                return {
                    "verdict": "ESCALATED",
                    "converged": False,
                    "attempts": attempt,
                    "escalation_payload": {
                        "reason": "ATTEMPTS_EXHAUSTED",
                        "failure_summary": f"Task '{task.task_id}' failed after {attempt} attempts (K={self.max_repair_k})",
                        "diagnostic_diff": diff,
                        "oracle_trace": oracle_trace,
                        "suggested_actions": ["Review diagnostic diff", "Refactor task specification"],
                    },
                }

            # 3. Trigger repair cycle
            self.current_stage = PipelineStage.REPAIR
            task.status = TaskStatus.REPAIRING
            oracle_trace = getattr(verif_result, "oracle_trace", "") or "Unknown test failure"
            repair_fn(oracle_trace)
            attempt += 1

        # Fallback (should not be reached)
        self.current_stage = PipelineStage.ESCALATED
        task.status = TaskStatus.ESCALATED
        return {"verdict": "ESCALATED", "converged": False, "attempts": attempt}
