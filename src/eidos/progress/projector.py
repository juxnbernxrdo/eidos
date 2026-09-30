"""Event-derived progress projection and observability engine.

Implements SPEC-015 (Event-Derived Progress & Observability) and satisfies
REQ-OBS-003, REQ-OBS-004, AC-015-01, AC-015-02:
    - Derives progress strictly from immutable event logs and Git anchors
    - Explicitly rejects unverified verbal agent claims of completion
    - Aggregates tokens, costs, and verification success rates (VSR) deterministically
"""

from typing import Any, Iterable
from pathlib import Path

from eidos.progress.logger import ProgressLogger


class ProgressProjector:
    """Projects immutable event streams into verified progress summaries."""

    def __init__(self, workspace_root: Path | None = None):
        self.workspace_root = workspace_root

    def project_events(self, events: Iterable[dict[str, Any]]) -> dict[str, Any]:
        """Reduces an event stream into an evidence-anchored progress summary.

        Verbal claims from agents (e.g. natural language messages stating 'complete')
        are not machine verification events and do not count toward convergence.
        """
        total_tokens = 0
        total_cost = 0.0
        tasks: dict[str, dict[str, Any]] = {}
        verifications: dict[str, bool] = {}
        repairs_count = 0
        tool_invocations = 0

        for event in events:
            etype = event.get("event_type")
            payload = event.get("payload", {})
            actor = event.get("actor", {})

            # 1. Token and cost accounting
            if "tokens" in payload and isinstance(payload["tokens"], (int, float)):
                total_tokens += int(payload["tokens"])
            elif "tokens_consumed" in payload and isinstance(payload["tokens_consumed"], (int, float)):
                total_tokens += int(payload["tokens_consumed"])

            if "cost_usd" in payload and isinstance(payload["cost_usd"], (int, float)):
                total_cost += float(payload["cost_usd"])
            elif "cost" in payload and isinstance(payload["cost"], (int, float)):
                total_cost += float(payload["cost"])

            # 2. Tool invocations
            if etype in ("TOOL_INVOKED", "TOOL_COMPLETED"):
                tool_invocations += 1

            # 3. Task registrations
            if etype == "TASK_CREATED":
                tid = payload.get("task_id")
                if tid:
                    tasks[tid] = {
                        "task_id": tid,
                        "title": payload.get("title", ""),
                        "converged": False,
                        "status": "PENDING",
                        "verbal_claim_only": False,
                    }

            # 4. Agent verbal claims (without verification)
            elif etype in ("AGENT_MESSAGE", "AGENT_RESPONSE", "TOOL_COMPLETED"):
                msg = str(payload.get("message", "") or payload.get("output", "")).lower()
                tid = event.get("task_id") or payload.get("task_id")
                if tid and tid in tasks and any(w in msg for w in ("done", "complete", "converged")):
                    # Mark that agent asserted verbal completion, but keep converged=False
                    tasks[tid]["verbal_claim_only"] = True

            # 5. Machine verification events
            elif etype in ("VERIFICATION_COMPLETED", "VERIFICATION_PASSED", "VERIFICATION_FAILED"):
                tid = event.get("task_id") or payload.get("task_id")
                converged = (etype == "VERIFICATION_PASSED") or bool(payload.get("converged", False))
                verif_id = payload.get("verification_id", event.get("event_id"))
                if verif_id:
                    verifications[verif_id] = converged

                if tid and tid in tasks:
                    if converged:
                        tasks[tid]["converged"] = True
                        tasks[tid]["status"] = "CONVERGED"
                        tasks[tid]["verbal_claim_only"] = False
                    else:
                        tasks[tid]["converged"] = False
                        tasks[tid]["status"] = "REPAIR"
                        repairs_count += 1

            elif etype == "REPAIR_ATTEMPTED":
                repairs_count += 1

        total_tasks = len(tasks)
        converged_tasks = sum(1 for t in tasks.values() if t["converged"])
        unconverged_tasks = total_tasks - converged_tasks
        vsr = (converged_tasks / total_tasks * 100.0) if total_tasks > 0 else 0.0

        return {
            "total_tasks": total_tasks,
            "converged_tasks": converged_tasks,
            "unconverged_tasks": unconverged_tasks,
            "verified_success_rate": round(vsr, 2),
            "total_tokens_consumed": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "total_repairs": repairs_count,
            "total_tool_invocations": tool_invocations,
            "tasks": tasks,
        }

    def project_workspace(self) -> dict[str, Any]:
        """Projects the active workspace event stream."""
        if not self.workspace_root:
            raise ValueError("workspace_root must be set to project from disk")
        logger = ProgressLogger(self.workspace_root)
        return self.project_events(logger.stream_events())
