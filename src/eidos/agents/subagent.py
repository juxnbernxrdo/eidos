"""Contract-bounded subagents operating in star topology with sandboxed CodeAct execution.

Implements SPEC-010 (Contract-Bounded Subagents & CodeAct Execution) and satisfies
REQ-AGENT-001, REQ-AGENT-002, AC-010-01, AC-010-02:
    - Guaranteed fresh context per dispatch (0 parent conversational turns)
    - Programmatic CodeAct execution space in isolated sandbox
    - Hard turn limit enforcement (turns <= 30)
"""

import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

from eidos.core.exceptions import (
    ContractViolationError,
    InvalidInputError,
    PermissionDeniedError,
)
from eidos.orchestration.task import TaskRecord
from eidos.security.permissions import create_capability_grant
from eidos.security.supervisor import SandboxSupervisor


class SubagentRunner:
    """Manages ephemeral, contract-bounded subagent instances."""

    def __init__(
        self,
        agent_id: str,
        workspace_root: Path,
        max_turns: int = 30,
        capability_grant: dict[str, Any] | None = None,
    ):
        self.agent_id = agent_id
        self.workspace_root = workspace_root.resolve()
        self.max_turns = min(max_turns, 30)  # Hard bound <= 30
        self.current_turn = 0
        self.terminated = False

        # Fresh context isolation guarantee (AC-010-01)
        self.prior_conversation_turns: int = 0
        self.task_context: dict[str, Any] | None = None
        self.msc_payload: dict[str, Any] | None = None

        self.grant = capability_grant or create_capability_grant(
            subject_id=self.agent_id,
            scope="WORKTREE_ONLY",
            allow_subprocess=True,
            allowed_binaries=["python3", "python", "pytest"],
        )
        self.supervisor = SandboxSupervisor(self.workspace_root, self.grant)

    def spawn(self, task: TaskRecord, msc_payload: dict[str, Any]) -> dict[str, Any]:
        """Initializes a fresh context execution environment for the subagent (AC-010-01)."""
        if not task or not msc_payload:
            raise InvalidInputError("Subagent requires TaskRecord and msc_payload")

        # Zero parent conversational history
        self.prior_conversation_turns = 0
        self.current_turn = 0
        self.terminated = False

        self.task_context = task.to_contract_dict()
        self.msc_payload = msc_payload

        return {
            "agent_id": self.agent_id,
            "status": "INITIALIZED",
            "context_turns": self.prior_conversation_turns,
            "task_id": task.task_id,
            "msc_id": msc_payload.get("routing_response", {}).get("msc_id"),
        }

    def execute_codeact_block(self, python_code: str) -> dict[str, Any]:
        """Executes a Python code block inside the sandbox for programmatic exploration (AC-010-02)."""
        if self.terminated:
            raise ContractViolationError("Cannot execute CodeAct on terminated subagent")

        self.current_turn += 1
        if self.current_turn > self.max_turns:
            self.terminate()
            raise ContractViolationError(
                f"Subagent '{self.agent_id}' exceeded max turn limit ({self.max_turns}); terminating"
            )

        # Write script to temporary sandbox scratch file
        with tempfile.NamedTemporaryFile("w", suffix=".py", dir=self.workspace_root, delete=False, encoding="utf-8") as tf:
            tf.write(python_code)
            temp_script = Path(tf.name)

        try:
            cmd = [sys.executable, str(temp_script)]
            code, stdout, stderr = self.supervisor.execute_sandboxed_command(cmd, cwd=self.workspace_root, timeout=15)

            return {
                "turn": self.current_turn,
                "exit_code": code,
                "stdout": stdout,
                "stderr": stderr,
                "traceback": stderr if code != 0 else "",
            }
        finally:
            if temp_script.exists():
                try:
                    temp_script.unlink()
                except OSError:
                    pass

    def terminate(self) -> dict[str, Any]:
        """Terminates subagent and cleans up ephemeral working context."""
        self.terminated = True
        return {
            "agent_id": self.agent_id,
            "status": "TERMINATED",
            "final_turns": self.current_turn,
        }
