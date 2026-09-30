"""Unit tests for SPEC-014: Gated Evolution & Self-Improvement Pipeline."""

from pathlib import Path
import pytest
from eidos.core.exceptions import PermissionDeniedError
from eidos.evolution.pipeline import EvolutionPipeline, ProposalState


def test_human_approval_gate_enforcement_ac_014_01(tmp_path: Path):
    """AC-014-01: Proposal remains unapplied in HUMAN_REVIEW until operator approves."""
    pipeline = EvolutionPipeline(tmp_path)

    prop = pipeline.create_proposal(
        title="Refine Subagent Turn Allocation",
        category="PROMPT_OPTIMIZATION",
        rationale="Improve single-turn resolution",
        proposed_diff="--- a/prompt.txt\n+++ b/prompt.txt\n",
    )
    pid = prop["proposal_id"]

    # Automated benchmark passes with +15% VSR
    updated = pipeline.submit_benchmark_evaluation(pid, delta_vsr=15.0, passed_regression=True)

    # Must remain unapplied in HUMAN_REVIEW
    assert updated["status"] == ProposalState.HUMAN_REVIEW.value
    assert updated["benchmark_delta"] == 15.0

    # Operator approves
    approved = pipeline.approve_proposal(pid, operator_signature="HUMAN-OPERATOR-01")
    assert approved["status"] == ProposalState.ACCEPTED.value
    assert approved["approved_by"] == "HUMAN-OPERATOR-01"


def test_blocking_unapproved_self_modification_ac_014_02(tmp_path: Path):
    """AC-014-02: Direct edits to AGENTS.md without approved proposal raise PERMISSION_DENIED."""
    pipeline = EvolutionPipeline(tmp_path)

    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# Agent Navigation\n", encoding="utf-8")

    with pytest.raises(PermissionDeniedError) as exc_info:
        pipeline.intercept_direct_modification(agents_md, actor_id="subagent-42")

    assert "Autonomous self-modification blocked" in str(exc_info.value)
    assert exc_info.value.details.get("invariant") == "INV-004"
