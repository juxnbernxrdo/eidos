"""Verification and integration tests for Eidos Phase 7 Evaluation engine."""

import math
from typer.testing import CliRunner
from eidos.cli.main import app
from eidos.evaluation.benchmark import get_benchmark_suite
from eidos.evaluation.models import ExperimentalArm, TaskDifficulty, TaskType
from eidos.evaluation.runner import EvaluationRunner
from eidos.evaluation.stats import (
    mean,
    median,
    variance,
    std_dev,
    confidence_interval_95,
    bootstrap_ci_95,
    cohens_d,
    permutation_test_p_value,
    compute_relative_change,
)

runner = CliRunner()


def test_benchmark_suite_integrity():
    """Verifies that the benchmark suite contains 10 diverse tasks covering all requirements."""
    suite = get_benchmark_suite()
    assert len(suite) == 10
    
    task_types = {t.task_type for t in suite.values()}
    assert len(task_types) == 10  # All 10 distinct task types represented
    assert TaskType.BUG_FIX in task_types
    assert TaskType.SECURITY_FIX in task_types
    assert TaskType.SYSTEM_INTEGRATION in task_types

    for tid, task in suite.items():
        assert task.task_id == tid
        assert len(task.initial_files) > 0
        assert len(task.ground_truth_patch) > 0
        assert len(task.public_tests) > 0
        assert len(task.hidden_tests) > 0
        assert len(task.invariants) > 0


def test_statistical_engine_calculations():
    """Verifies precision and correctness of the statistical calculations."""
    data = [10.0, 12.0, 14.0, 16.0, 18.0]
    assert mean(data) == 14.0
    assert median(data) == 14.0
    assert variance(data) == 10.0
    assert math.isclose(std_dev(data), math.sqrt(10.0), rel_tol=1e-4)

    ci = confidence_interval_95(data)
    assert ci[0] < 14.0 < ci[1]

    bci = bootstrap_ci_95(data, num_resamples=500, seed=42)
    assert bci[0] < 14.0 < bci[1]

    data2 = [20.0, 22.0, 24.0, 26.0, 28.0]
    d = cohens_d(data, data2)
    assert d > 2.0  # Very large positive effect

    p_val = permutation_test_p_value(data, data2, num_permutations=200, seed=42)
    assert p_val < 0.05  # Statistically significant difference

    rel = compute_relative_change(100.0, 150.0)
    assert rel == 50.0
    rel_neg = compute_relative_change(100.0, 40.0)
    assert rel_neg == -60.0


def test_evaluation_runner_controlled_trial(tmp_path):
    """Verifies that EvaluationRunner executes controlled trials and produces valid TaskResult."""
    eval_runner = EvaluationRunner(workspace_root=tmp_path, seed=42)
    task = eval_runner.tasks["TSK-EVAL-001"]
    
    # Run B0 trial
    res_b0 = eval_runner.run_trial(task, ExperimentalArm.B0_RAW_AGENT, trial_seed=42)
    assert res_b0.task_id == "TSK-EVAL-001"
    assert res_b0.arm == ExperimentalArm.B0_RAW_AGENT
    assert res_b0.tokens_total > 0
    assert res_b0.wall_clock_ms > 0
    assert res_b0.cost_usd > 0

    # Run B2 trial
    res_b2 = eval_runner.run_trial(task, ExperimentalArm.B2_FULL_EIDOS, trial_seed=42)
    assert res_b2.arm == ExperimentalArm.B2_FULL_EIDOS
    assert res_b2.tokens_total < res_b0.tokens_total  # MSC reduces tokens


def test_evaluation_run_matrix_execution(tmp_path):
    """Verifies execution of multi-arm evaluation matrix and JSON serialization."""
    eval_runner = EvaluationRunner(workspace_root=tmp_path, seed=123)
    arms = [ExperimentalArm.B0_RAW_AGENT, ExperimentalArm.B2_FULL_EIDOS]
    tasks = ["TSK-EVAL-001", "TSK-EVAL-004"]
    
    run_result = eval_runner.execute_evaluation(
        arms=arms,
        task_ids=tasks,
        trials_per_task=2,
        model_id="test-model"
    )
    assert len(run_result.results) == 8  # 2 arms * 2 tasks * 2 trials
    assert len(run_result.arm_statistics) == 2
    assert ExperimentalArm.B2_FULL_EIDOS.value in run_result.ablation_deltas

    # Verify JSON file written to disk
    runs_dir = tmp_path / ".eidos" / "evaluation" / "runs"
    assert len(list(runs_dir.glob("*.json"))) == 1


def test_cli_eval_commands():
    """Verifies CLI eval subcommands execute cleanly."""
    res_tasks = runner.invoke(app, ["eval", "tasks"])
    assert res_tasks.exit_code == 0
    assert "Phase 7 Benchmark Task Suite" in res_tasks.stdout
    assert "TSK-EVAL-001" in res_tasks.stdout

    res_report = runner.invoke(app, ["eval", "report"])
    assert res_report.exit_code == 0
    assert "Evaluation Run Artifact" in res_report.stdout
