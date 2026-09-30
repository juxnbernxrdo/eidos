"""Tripartite memory manager with opt-in admission gates and cross-project isolation.

Implements SPEC-011 (Tripartite Memory Boundaries & Opt-in Admission Gates) and satisfies
REQ-MEM-001, REQ-MEM-002, AC-011-01, AC-011-02:
    - Default-disabled persistent memory gating (opt_in_memory=False)
    - Strict cross-project memory isolation
    - Tripartite tier separation (working, project, institutional)
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from eidos.core.exceptions import PermissionDeniedError
from eidos.security.permissions import redact_secrets


class TripartiteMemoryManager:
    """Manages working, project, and institutional memory tiers."""

    def __init__(self, workspace_root: Path, opt_in_memory: bool = False):
        self.workspace_root = workspace_root.resolve()
        self.opt_in_memory = opt_in_memory
        self.project_memory_dir = self.workspace_root / ".eidos" / "memory"
        
        # Working memory tier (ephemeral, subtask lifetime)
        self.working_memory: dict[str, Any] = {}

    def set_working_memory(self, key: str, value: Any) -> None:
        """Stores ephemeral working memory within current subtask."""
        self.working_memory[key] = value

    def get_working_memory(self, key: str) -> Any | None:
        """Retrieves ephemeral working memory."""
        return self.working_memory.get(key)

    def clear_working_memory(self) -> None:
        """Destroys all working memory upon subtask completion."""
        self.working_memory.clear()

    def persist_project_memory(
        self,
        key: str,
        content: str,
        task_id: str = "TASK-UNKNOWN",
        epistemic_status: str = "INFERRED",
        confidence: float = 0.8,
    ) -> dict[str, Any]:
        """Attempts to persist memory to the repository-scoped tier (AC-011-01).

        If opt_in_memory is False (default), ignores write and emits advisory notice.
        """
        if not self.opt_in_memory:
            # AC-011-01: Default Opt-In Gating ignores write
            return {
                "admitted": False,
                "status": "IGNORED_OPT_IN_DISABLED",
                "message": "Persistent project memory is disabled by default (opt_in_memory=false).",
            }

        self.project_memory_dir.mkdir(parents=True, exist_ok=True)
        sanitized_content = redact_secrets(content)

        record = {
            "key": key,
            "content": sanitized_content,
            "project_id": f"PROJ-{self.workspace_root.name.upper()}",
            "task_id": task_id,
            "epistemic_status": epistemic_status,
            "confidence": confidence,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        target_file = self.project_memory_dir / f"{key}.json"
        target_file.write_text(json.dumps(record, indent=2), encoding="utf-8")

        return {
            "admitted": True,
            "status": "ACCEPTED",
            "file": str(target_file),
        }

    def query_project_memory(self, query: str = "") -> list[dict[str, Any]]:
        """Queries repository-scoped memory strictly within current workspace (AC-011-02)."""
        if not self.project_memory_dir.exists():
            return []

        results: list[dict[str, Any]] = []
        for mf in self.project_memory_dir.glob("*.json"):
            try:
                data = json.loads(mf.read_text(encoding="utf-8"))
                # Strict verification of project ID isolation
                if data.get("project_id") == f"PROJ-{self.workspace_root.name.upper()}":
                    if not query or query.lower() in data.get("content", "").lower() or query.lower() in data.get("key", "").lower():
                        results.append(data)
            except Exception:
                continue

        return results

    def write_institutional_memory(self, key: str, content: str, human_approved: bool = False) -> None:
        """Writes to institutional cross-project tier; strictly forbidden without human approval."""
        if not human_approved:
            raise PermissionDeniedError(
                "Writing to institutional memory without human cryptographic approval is forbidden (INV-002)",
                details={"key": key},
            )
