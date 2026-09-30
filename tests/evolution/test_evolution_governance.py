"""Verification and governance tests for Phase 8 Evolution subsystem."""

from pathlib import Path
from typer.testing import CliRunner
import pytest

from eidos.cli.main import app
from eidos.core.exceptions import PermissionDeniedError, ContractViolationError
from eidos.evolution.pipeline import EvolutionPipeline, ProposalState
from eidos.orchestration.pipeline import PhasedPipeline, PipelineStage
from eidos.orchestration.task import TaskRecord, TaskStatus

runner = CliRunner()


def test_evolution_lifecycle_complete_progression(tmp_path: Path):
    """Verifies the complete 7-stage evolution lifecycle."""
    pipeline = EvolutionPipeline(tmp_path)

    # 1. Proposal
    prop = pipeline.create_proposal(
        title="Dynamic Context Budget Allocation",
        category="CONTEXT_OPTIMIZATION",
        rationale="Optimize token allocation under tight budgets",
        proposed_diff="--- a/router.py\n+++ b/router.py\n",
    )
    pid = prop["proposal_id"]
    assert prop["status"] == ProposalState.PROPOSED.value

    # 2. Evaluation with regressions fails immediately
    pipeline_fail = EvolutionPipeline(tmp_path)
    prop_fail = pipeline_fail.create_proposal(
        title="Flawed Modification",
        category="TEST",
        rationale="Testing regression veto",
        proposed_diff="error",
    )
    rej = pipeline_fail.submit_benchmark_evaluation(prop_fail["proposal_id"], delta_vsr=-5.0, passed_regression=False)
    assert rej["status"] == ProposalState.REJECTED.value

    # 3. Successful evaluation advances to HUMAN_REVIEW (unapplied)
    evaluated = pipeline.submit_benchmark_evaluation(pid, delta_vsr=12.5, passed_regression=True)
    assert evaluated["status"] == ProposalState.HUMAN_REVIEW.value

    # 4. Operator approval ratifies to ACCEPTED
    accepted = pipeline.approve_proposal(pid, operator_signature="OPERATOR-KEY-42")
    assert accepted["status"] == ProposalState.ACCEPTED.value
    assert accepted["approved_by"] == "OPERATOR-KEY-42"


def test_blocking_direct_unapproved_edits(tmp_path: Path):
    """AC-014-02: Direct modification of governance rules without proposal raises PERMISSION_DENIED."""
    pipeline = EvolutionPipeline(tmp_path)
    agents_file = tmp_path / "AGENTS.md"
    agents_file.write_text("# Agents\n", encoding="utf-8")

    with pytest.raises(PermissionDeniedError) as exc_info:
        pipeline.intercept_direct_modification(agents_file, actor_id="autonomous-subagent")
    assert "Autonomous self-modification blocked" in str(exc_info.value)
    assert exc_info.value.details.get("invariant") == "INV-004"


def test_evo_001_adaptive_early_stopping(tmp_path: Path):
    """Verifies PROP-EVO-001: Adaptive early-stopping when repetitive error cycles occur."""
    pipeline = PhasedPipeline(tmp_path, max_repair_k=5)
    task = TaskRecord(
        task_id="TSK-CYCLE-TEST",
        spec_id="SPEC-002",
        title="Repetitive failure test",
        objective="Verify early stopping",
        workspace_root=tmp_path,
        target_files=["main.py"],
        acceptance_criteria=["Cycle stops at attempt 2"],
    )

    pipeline.advance_stage(PipelineStage.SPECIFY)
    pipeline.advance_stage(PipelineStage.PLAN)
    pipeline.advance_stage(PipelineStage.IMPLEMENT)

    # Mock verifier that emits identical failing error trace across all attempts
    class MockFailingResult:
        converged = False
        oracle_trace = "IndexError: list index out of range at line 14"

    def mock_cyclic_verifier(attempt: int):
        return MockFailingResult()

    repaired_calls = []
    def mock_repair_fn(trace: str):
        repaired_calls.append(trace)

    # Execute with adaptive early stopping enabled
    res = pipeline.execute_bounded_repair_loop(
        task=task,
        verifier_fn=mock_cyclic_verifier,
        repair_fn=mock_repair_fn,
        adaptive_early_stopping=True,
    )

    # Should escalate early at attempt 2 due to repetitive error trace, saving attempts 3, 4, 5
    assert res["verdict"] == "ESCALATED"
    assert res["attempts"] == 2
    assert res["escalation_payload"]["reason"] == "REPETITIVE_ERROR_CYCLE_DETECTED"
    assert pipeline.current_stage == PipelineStage.ESCALATED
    assert task.status == TaskStatus.ESCALATED


def test_cli_evolve_subcommands(tmp_path: Path):
    """Verifies CLI evolve commands function properly."""
    res_list = runner.invoke(app, ["evolve", "list"])
    assert res_list.exit_code == 0
    assert "Eidos Evolution Proposals Ledger" in res_list.stdout

    res_prop = runner.invoke(app, [
        "evolve", "propose",
        "--title", "Test CLI Proposal",
        "--rationale", "Testing CLI propose command",
    ])
    assert res_prop.exit_code == 0
    assert "Proposal Created:" in res_prop.stdout

    # Clean up created test proposal from repository
    for p in Path(".eidos/evolution/proposals").glob("PROP-*.json"):
        p.unlink(missing_ok=True)
