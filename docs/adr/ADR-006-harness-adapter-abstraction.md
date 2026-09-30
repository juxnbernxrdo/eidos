# ADR-006: Portable Harness Adapter Abstraction Layer

**Status:** Accepted  
**Date:** 2024-09-30 (Updated 2026)  
**Deciders:** Juan Bernardo Ordóñez (Author), AI Agent Systems Architecture Team  

---

## Context
Eidos must operate across multiple coding harnesses: Google Antigravity, Claude Code, OpenCode, Codex, Cursor, and Hermes Agent. Each harness has different runtime environments, process invocation mechanisms, file tracking formats, and subagent leasing protocols. Hardcoding Eidos to any single vendor or harness would violate the fundamental requirement of portability.

## Decision
Eidos decouples all host interaction via an abstract base class: `HarnessAdapter`.

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class HarnessAdapter(ABC):
    @abstractmethod
    def detect(self, workspace_root: str) -> bool:
        """Determines if the active environment matches this harness."""
        pass

    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """Returns feature flags: subagents, background_tasks, mcp, worktrees."""
        pass

    @abstractmethod
    def configure(self, project_contract: Dict[str, Any]) -> None:
        """Injects rules (AGENTS.md, CLAUDE.md, etc.) and mounts tool definitions."""
        pass

    @abstractmethod
    def dispatch_subagent(self, task_contract: Dict[str, Any]) -> str:
        """Leases and executes a contract-bounded subagent on the host harness."""
        pass

    @abstractmethod
    def collect_execution_trace(self, execution_id: str) -> Dict[str, Any]:
        """Extracts tool calls, token usage, stderr/stdout, and execution diffs."""
        pass
```

### Initial Target Implementations
1. `AntigravityAdapter`: Google Antigravity IDE and CLI (`.agents/skills`, subagent tools, background tasks, artifacts).
2. `ClaudeCodeAdapter`: Anthropic Claude Code (`.claude/skills`, `CLAUDE.md`, slash commands).
3. `OpenCodeAdapter`: OpenCode CLI/TUI (`AGENTS.md`, LSP bridge).
4. `HeadlessAdapter`: Standalone Docker / CLI runner for SWE-bench evaluation and CI/CD pipelines.

## Consequences

### Positive
- True multi-harness portability: Eidos functions as an engineering layer regardless of whether the developer uses Antigravity, Claude Code, or OpenCode.
- Core Eidos logic (spec engine, graph intelligence, verification rules) remains 100% agnostic of host platform idiosyncrasies.
- Enables direct empirical benchmarking of the central hypothesis ($Model \times Harness$) on identical tasks across different harnesses.

### Negative
- Requires maintaining adapter compatibility as external harnesses update their proprietary CLI flags or configuration file formats.
