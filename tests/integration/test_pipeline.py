"""Integration tests for SPEC-002 (Pipeline) and SPEC-010 (Subagents)."""

from pathlib import Path
import pytest
from eidos.core.exceptions import ContractViolationError
from eidos.orchestration.pipeline import PhasedPipeline, PipelineStage
from eidos.orchestration.task import TaskRecord, TaskStatus
from eidos.agents.subagent import SubagentRunner


class DummyVerifResult:
    def __init__(self, converged: bool, oracle: str = ""):
        self.converged = converged
        self.oracle_trace = oracle


def test_non_bypassable_gating_ac_002_01(tmp_path: Path):
    """AC-002-01: Attempting to jump directly from DISCOVERY to IMPLEMENT fails closed."""
    pipeline = PhasedPipeline(tmp_path)
    assert pipeline.current_stage == PipelineStage.DISCOVERY

    with pytest.raises(ContractViolationError) as exc_info:
        pipeline.advance_stage(PipelineStage.IMPLEMENT)

    assert "Non-bypassable gating violation" in str(exc_info.value)
    assert pipeline.current_stage == PipelineStage.DISCOVERY


def test_repair_loop_bounding_at_k_ac_002_02(tmp_path: Path):
    """AC-002-02: After 5 failed attempts with K=5, pipeline transitions to ESCALATED without 6th attempt."""
    pipeline = PhasedPipeline(tmp_path, max_repair_k=5)
    task = TaskRecord(
        task_id="TASK-REPAIR-K",
        spec_id="SPEC-002",
        title="Repair Bound Test",
        objective="Verify K bound",
        workspace_root=tmp_path,
        target_files=["main.py"],
        acceptance_criteria=["Passes"],
    )

    call_count = 0
    repair_count = 0

    def mock_verifier(attempt: int):
        nonlocal call_count
        call_count += 1
        return DummyVerifResult(converged=False, oracle="AssertionError: Expected 10, got 5")

    def mock_repair(oracle: str):
        nonlocal repair_count
        repair_count += 1

    outcome = pipeline.execute_bounded_repair_loop(task, mock_verifier, mock_repair)

    assert outcome["verdict"] == "ESCALATED"
    assert outcome["converged"] is False
    assert outcome["attempts"] == 5
    assert call_count == 5
    assert repair_count == 4  # 4 repairs leading to 5th attempt
    assert pipeline.current_stage == PipelineStage.ESCALATED


def test_diagnostic_diff_on_escalation_ac_002_03(tmp_path: Path):
    """AC-002-03: Escalation payload contains diagnostic diff and failure summary."""
    pipeline = PhasedPipeline(tmp_path, max_repair_k=1)
    task = TaskRecord(
        task_id="TASK-DIFF-TEST",
        spec_id="SPEC-002",
        title="Diff Test",
        objective="Verify diff capture",
        workspace_root=tmp_path,
        target_files=["main.py"],
        acceptance_criteria=["Passes"],
    )

    def failing_verif(attempt: int):
        return DummyVerifResult(converged=False, oracle="SyntaxError on line 12")

    outcome = pipeline.execute_bounded_repair_loop(task, failing_verif, lambda o: None)
    esc = outcome["escalation_payload"]

    assert esc["reason"] == "ATTEMPTS_EXHAUSTED"
    assert "diagnostic_diff" in esc
    assert "failure_summary" in esc
    assert len(esc["suggested_actions"]) > 0


def test_subagent_fresh_context_isolation_ac_010_01(tmp_path: Path):
    """AC-010-01: Subagent spawned with 0 parent conversational turns."""
    subagent = SubagentRunner("SUBAGENT-TEST", tmp_path, max_turns=10)
    task = TaskRecord(
        task_id="TASK-SUB-01",
        spec_id="SPEC-010",
        title="Subagent Task",
        objective="Fresh context check",
        workspace_root=tmp_path,
        target_files=["src/test.py"],
        acceptance_criteria=["Clean prompt"],
    )
    msc = {
        "contract_id": "CTX-CONTRACT-001",
        "routing_response": {"msc_id": "MSC-TEST-01", "total_tokens": 120},
    }

    info = subagent.spawn(task, msc)
    assert info["context_turns"] == 0
    assert subagent.prior_conversation_turns == 0
    assert subagent.task_context["task_id"] == "TASK-SUB-01"


def test_codeact_sandboxed_execution_ac_010_02(tmp_path: Path):
    """AC-010-02: Subagent executes Python code block inside sandbox and captures stdout/traceback."""
    subagent = SubagentRunner("SUBAGENT-CODEACT", tmp_path, max_turns=5)
    task = TaskRecord(
        task_id="TASK-CA-01",
        spec_id="SPEC-010",
        title="CodeAct Test",
        objective="Run python block",
        workspace_root=tmp_path,
        target_files=["test.py"],
        acceptance_criteria=["stdout captured"],
    )
    subagent.spawn(task, {"routing_response": {"msc_id": "MSC-01"}})

    script = "print('Hello from CodeAct Sandbox')\nx = 10 + 20\nprint(f'Computed: {x}')\n"
    res = subagent.execute_codeact_block(script)

    assert res["exit_code"] == 0
    assert "Hello from CodeAct Sandbox" in res["stdout"]
    assert "Computed: 30" in res["stdout"]
    assert res["turn"] == 1
