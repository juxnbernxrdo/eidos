"""Eidos Evaluation Subsystem implementing Phase 7 empirical benchmarking and statistical analysis."""

from eidos.evaluation.models import (
    TaskDefinition,
    TaskResult,
    EvaluationRun,
    ExperimentalArm,
    TaskDifficulty,
    TaskType,
    ArmSummaryStats,
)
from eidos.evaluation.benchmark import get_benchmark_suite
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

__all__ = [
    "TaskDefinition",
    "TaskResult",
    "EvaluationRun",
    "ExperimentalArm",
    "TaskDifficulty",
    "TaskType",
    "ArmSummaryStats",
    "get_benchmark_suite",
    "EvaluationRunner",
    "mean",
    "median",
    "variance",
    "std_dev",
    "confidence_interval_95",
    "bootstrap_ci_95",
    "cohens_d",
    "permutation_test_p_value",
    "compute_relative_change",
]
