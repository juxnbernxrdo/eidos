from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TaskDifficulty(str, Enum):
    """Classification of benchmark task complexity."""
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    SYSTEM = "SYSTEM"


class TaskType(str, Enum):
    """Categorical classification of software engineering task types."""
    BUG_FIX = "BUG_FIX"
    FEATURE_IMPL = "FEATURE_IMPL"
    REFACTORING = "REFACTORING"
    SECURITY_FIX = "SECURITY_FIX"
    CONTRACT_REPAIR = "CONTRACT_REPAIR"
    ARCH_INVARIANT_FIX = "ARCH_INVARIANT_FIX"
    TEST_REPAIR = "TEST_REPAIR"
    CROSS_MODULE_INTEGRATION = "CROSS_MODULE_INTEGRATION"
    PERF_OPTIMIZATION = "PERF_OPTIMIZATION"
    SYSTEM_INTEGRATION = "SYSTEM_INTEGRATION"


class ExperimentalArm(str, Enum):
    """Experimental baselines and ablation arms."""
    B0_RAW_AGENT = "B0_RAW_AGENT"
    B1_BASIC_HARNESS = "B1_BASIC_HARNESS"
    B2_FULL_EIDOS = "B2_FULL_EIDOS"
    A0_BASELINE = "A0_BASELINE"
    A1_PLUS_SPECS = "A1_PLUS_SPECS"
    A2_PLUS_CONTRACTS = "A2_PLUS_CONTRACTS"
    A3_PLUS_GRAPH = "A3_PLUS_GRAPH"
    A4_PLUS_CONTEXT_ROUTER = "A4_PLUS_CONTEXT_ROUTER"
    A5_PLUS_SKILLS = "A5_PLUS_SKILLS"
    A6_PLUS_SUBAGENTS = "A6_PLUS_SUBAGENTS"
    A7_PLUS_VERIFICATION = "A7_PLUS_VERIFICATION"
    A8_PLUS_MEMORY = "A8_PLUS_MEMORY"
    A9_FULL_EIDOS = "A9_FULL_EIDOS"


class TaskDefinition(BaseModel):
    """Specification of an empirical benchmark task."""
    task_id: str = Field(..., description="Unique task identifier, e.g. TSK-EVAL-001")
    title: str = Field(..., description="Short descriptive title of the task")
    task_type: TaskType = Field(..., description="Category of engineering work")
    difficulty: TaskDifficulty = Field(..., description="Complexity bin (SMALL..SYSTEM)")
    description: str = Field(..., description="Complete prompt and instructions presented to agent")
    initial_files: Dict[str, str] = Field(default_factory=dict, description="Pre-existing file contents")
    ground_truth_patch: Dict[str, str] = Field(default_factory=dict, description="Reference solution patch")
    public_tests: List[str] = Field(default_factory=list, description="Public verification test cases")
    hidden_tests: List[str] = Field(default_factory=list, description="Held-out tests to screen false confidence")
    invariants: List[str] = Field(default_factory=list, description="Architectural/security invariants to satisfy")
    is_security_sensitive: bool = Field(default=False, description="Whether task contains security boundaries")
    token_budget: int = Field(default=8000, description="Max token allocation")


class TaskResult(BaseModel):
    """Recorded outcome from executing a single trial of a benchmark task under an experimental arm."""
    trial_id: str
    task_id: str
    arm: ExperimentalArm
    seed: int
    success: bool = Field(..., description="True if both public and hidden test suites passed")
    public_tests_passed: bool
    hidden_tests_passed: bool
    verification_passed: bool
    invariant_passed: bool
    regressions_count: int = Field(default=0, description="Number of previously passing tests broken")
    repair_iterations: int = Field(default=0, description="Number of feedback loop iterations")
    tokens_prompt: int = Field(default=0)
    tokens_completion: int = Field(default=0)
    tokens_total: int = Field(default=0)
    wall_clock_ms: float = Field(default=0.0)
    tool_calls_count: int = Field(default=0)
    context_size_tokens: int = Field(default=0)
    cost_usd: float = Field(default=0.0)
    failure_mode: Optional[str] = Field(default=None)
    trace_log: List[Dict[str, Any]] = Field(default_factory=list)


class ArmSummaryStats(BaseModel):
    """Aggregated statistical metrics for an experimental arm across trials."""
    arm: ExperimentalArm
    total_trials: int
    task_success_rate: float = Field(..., description="Proportion of trials passing all oracles (VSR)")
    public_pass_rate: float
    hidden_pass_rate: float
    mean_regressions: float
    mean_repair_iterations: float
    mean_tokens: float
    std_tokens: float
    ci95_tokens: tuple[float, float]
    mean_latency_ms: float
    mean_tool_calls: float
    mean_cost_usd: float
    failure_distribution: Dict[str, int] = Field(default_factory=dict)


class EvaluationRun(BaseModel):
    """A complete reproducible evaluation experiment execution package."""
    run_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    git_commit: str
    model_identifier: str = Field(default="mock-frontier-2026")
    arms_evaluated: List[ExperimentalArm]
    tasks_evaluated: List[str]
    trials_per_task: int
    random_seeds: List[int]
    results: List[TaskResult] = Field(default_factory=list)
    arm_statistics: Dict[str, ArmSummaryStats] = Field(default_factory=dict)
    ablation_deltas: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    statistical_tests: Dict[str, Any] = Field(default_factory=dict)
