"""Headless CI reference harness adapter for automated pipeline evaluation.

Implements SPEC-009 headless mode for deterministic continuous evaluation (EXP-001).
"""

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from eidos.core.exceptions import InvalidInputError, ResourceUnavailableError
from eidos.harness.base import BaseHarnessAdapter


class HeadlessHarnessAdapter(BaseHarnessAdapter):
    """Reference headless CI harness adapter."""

    def detect(self) -> bool:
        """Headless adapter is always available as fallback."""
        return True

    def capabilities(self) -> dict[str, Any]:
        return {
            "subagents": True,
            "codeact": True,
            "mcp": True,
            "worktrees": True,
            "trace_fidelity": "full_raw_stream",
        }

    def configure(self, mcp_servers: list[dict[str, Any]] | None = None) -> bool:
        return True

    def invoke(self, dispatch_request: dict[str, Any]) -> str:
        exec_id = f"EXEC-HEADLESS-{uuid.uuid4().hex[:8].upper()}"
        task = dispatch_request.get("task", {})

        # Simulate execution turns and recording
        turns = dispatch_request.get("simulated_turns") or [
            {"turn": 1, "action": "inspect_target_file", "exit_code": 0},
            {"turn": 2, "action": "apply_patch", "exit_code": 0},
            {"turn": 3, "action": "run_tests", "exit_code": 0},
        ]

        trace = []
        for t in turns:
            trace.append({
                "turn": t.get("turn", 1),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": t.get("action", "execute"),
                "exit_code": t.get("exit_code", 0),
            })

        self.active_executions[exec_id] = {
            "execution_id": exec_id,
            "task_id": task.get("task_id", "TASK-UNKNOWN"),
            "status": "COMPLETED",
            "patch_diff": dispatch_request.get("patch_diff", ""),
            "artifacts": dispatch_request.get("artifacts", []),
            "errors": [],
            "trace": trace,
        }
        return exec_id

    def collect_output(self, execution_id: str) -> dict[str, Any]:
        if execution_id not in self.active_executions:
            raise ResourceUnavailableError(f"Execution '{execution_id}' not found")
        data = self.active_executions[execution_id]
        return {
            "execution_id": execution_id,
            "status": data["status"],
            "patch_diff": data["patch_diff"],
            "artifacts": data["artifacts"],
            "errors": data["errors"],
        }

    def collect_trace(self, execution_id: str) -> list[dict[str, Any]]:
        """Collects the turn-by-turn observation trace (AC-009-02)."""
        if execution_id not in self.active_executions:
            raise ResourceUnavailableError(f"Execution '{execution_id}' not found")
        return self.active_executions[execution_id]["trace"]
