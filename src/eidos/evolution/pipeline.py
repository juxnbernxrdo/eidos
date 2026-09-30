"""Gated Evolution & Self-Improvement Pipeline.

Implements SPEC-014 (Gated Evolution & Self-Improvement Pipeline) and satisfies
REQ-EVO-001, REQ-EVO-002, AC-014-01, AC-014-02:
    - Strictly gated 7-stage evolution lifecycle
    - Human-in-the-loop gate before any rule or parameter update
    - Blocking unapproved direct self-modifications (INV-004)
"""

import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from eidos.core.exceptions import (
    ContractViolationError,
    InvalidInputError,
    PermissionDeniedError,
)


class ProposalState(str, Enum):
    """The 6 formal lifecycle states of a self-improvement learning proposal."""
    PROPOSED = "PROPOSED"
    TESTING = "TESTING"
    EVALUATED = "EVALUATED"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class EvolutionPipeline:
    """Oversees proposal, sandboxed benchmarking, and human review for system updates."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.evolution_dir = self.workspace_root / ".eidos" / "evolution"
        self.proposals_dir = self.evolution_dir / "proposals"
        self.accepted_dir = self.evolution_dir / "accepted"
        self.rejected_dir = self.evolution_dir / "rejected"

        self.proposals_dir.mkdir(parents=True, exist_ok=True)
        self.accepted_dir.mkdir(parents=True, exist_ok=True)
        self.rejected_dir.mkdir(parents=True, exist_ok=True)

    def create_proposal(
        self,
        title: str,
        category: str,
        rationale: str,
        proposed_diff: str,
        target_rule_file: str = "AGENTS.md",
    ) -> dict[str, Any]:
        """Creates a structured LearningProposal in PROPOSED state."""
        pid = f"PROP-{uuid.uuid4().hex[:8].upper()}"
        doc = {
            "proposal_id": pid,
            "title": title,
            "category": category,
            "rationale": rationale,
            "target_rule_file": target_rule_file,
            "proposed_diff": proposed_diff,
            "status": ProposalState.PROPOSED.value,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "benchmark_delta": None,
            "approved_by": None,
        }

        f = self.proposals_dir / f"{pid}.json"
        f.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        return doc

    def submit_benchmark_evaluation(
        self,
        proposal_id: str,
        delta_vsr: float,
        passed_regression: bool,
    ) -> dict[str, Any]:
        """Evaluates automated benchmark results; advances proposal to HUMAN_REVIEW (AC-014-01).

        The change remains unapplied in state HUMAN_REVIEW until an explicit operator approval event is received.
        """
        f = self.proposals_dir / f"{proposal_id}.json"
        if not f.exists():
            raise InvalidInputError(f"Proposal '{proposal_id}' does not exist")

        doc = json.loads(f.read_text(encoding="utf-8"))

        if not passed_regression:
            doc["status"] = ProposalState.REJECTED.value
            doc["rejection_reason"] = "Benchmark evaluation caused regressions"
            out = self.rejected_dir / f"{proposal_id}.json"
            out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
            f.unlink()
            return doc

        # AC-014-01: Change remains unapplied in state HUMAN_REVIEW
        doc["status"] = ProposalState.HUMAN_REVIEW.value
        doc["benchmark_delta"] = delta_vsr
        f.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        return doc

    def approve_proposal(
        self,
        proposal_id: str,
        operator_signature: str,
        apply_change: bool = True,
    ) -> dict[str, Any]:
        """Applies human approval gate to transition proposal to ACCEPTED (AC-014-01)."""
        f = self.proposals_dir / f"{proposal_id}.json"
        if not f.exists():
            raise InvalidInputError(f"Proposal '{proposal_id}' does not exist in review queue")

        doc = json.loads(f.read_text(encoding="utf-8"))
        if doc["status"] != ProposalState.HUMAN_REVIEW.value:
            raise ContractViolationError(
                f"Cannot approve proposal in state '{doc['status']}'; must be in HUMAN_REVIEW"
            )

        doc["status"] = ProposalState.ACCEPTED.value
        doc["approved_by"] = operator_signature
        doc["approved_at"] = datetime.now(timezone.utc).isoformat()

        # Archive to accepted
        out = self.accepted_dir / f"{proposal_id}.json"
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        f.unlink()

        return doc

    def intercept_direct_modification(self, target_file: Path | str, actor_id: str = "subagent") -> None:
        """Blocks direct unapproved edits to governance rules and agents (AC-014-02)."""
        target_name = Path(target_file).name
        protected_files = ("AGENTS.md", "CONSTITUTION.md", "project.json", "skills-lock.json")

        if target_name in protected_files or ".eidos" in str(target_file):
            raise PermissionDeniedError(
                f"Autonomous self-modification blocked: Actor '{actor_id}' cannot edit protected file '{target_name}' directly (INV-004)",
                details={"target_file": str(target_file), "actor_id": actor_id, "invariant": "INV-004"},
            )
