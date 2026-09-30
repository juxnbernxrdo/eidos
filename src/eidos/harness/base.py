"""Base contract-bounded host harness adapter interface.

Implements SPEC-009 (Host Harness Adapters & Trace Streaming) and satisfies
REQ-HARN-001, REQ-HARN-002, AC-009-01, AC-009-02:
    - 6 formal operations: detect, capabilities, configure, invoke, collect_output, collect_trace
    - Zero host-specific leakage into Eidos Core
    - Full turn-by-turn observation trace streaming
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseHarnessAdapter(ABC):
    """Abstract host harness adapter insulating Eidos Core from host idiosyncrasies."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.active_executions: dict[str, dict[str, Any]] = {}

    @abstractmethod
    def detect(self) -> bool:
        """Scans environment or workspace markers to identify active host harness."""
        pass

    @abstractmethod
    def capabilities(self) -> dict[str, Any]:
        """Returns the capability matrix for the harness."""
        pass

    @abstractmethod
    def configure(self, mcp_servers: list[dict[str, Any]] | None = None) -> bool:
        """Mounts governance rules and MCP server configurations into the host."""
        pass

    @abstractmethod
    def invoke(self, dispatch_request: dict[str, Any]) -> str:
        """Dispatches a contract-bounded task and returns a unique execution_id."""
        pass

    @abstractmethod
    def collect_output(self, execution_id: str) -> dict[str, Any]:
        """Gathers task completion summary, patch diffs, created artifacts, and errors."""
        pass

    @abstractmethod
    def collect_trace(self, execution_id: str) -> list[dict[str, Any]]:
        """Gathers the full raw turn-by-turn observation trace stream (AC-009-02)."""
        pass
