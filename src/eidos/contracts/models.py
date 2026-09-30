"""Pydantic v2 data models for Eidos contracts, schemas, and graph entities."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    """The 21 formal heterogeneous entity types in the Repository Intelligence Graph."""
    FILE = "File"
    DIRECTORY = "Directory"
    MODULE = "Module"
    CLASS = "Class"
    FUNCTION = "Function"
    API = "API"
    DATABASE = "Database"
    DEPENDENCY = "Dependency"
    TEST = "Test"
    SPEC = "Spec"
    SUBSPEC = "SubSpec"
    TASK = "Task"
    CONTRACT = "Contract"
    AGENT = "Agent"
    SKILL = "Skill"
    RULE = "Rule"
    COMMIT = "Commit"
    FINDING = "Finding"
    SESSION = "Session"
    FEATURE = "Feature"
    EVIDENCE = "Evidence"


class EdgeRelation(str, Enum):
    """The 11 closed relational edge types in the Repository Intelligence Graph."""
    IMPLEMENTS = "IMPLEMENTS"
    DEPENDS_ON = "DEPENDS_ON"
    TESTED_BY = "TESTED_BY"
    DOCUMENTED_BY = "DOCUMENTED_BY"
    DEFINED_BY = "DEFINED_BY"
    MODIFIED_BY = "MODIFIED_BY"
    VIOLATES = "VIOLATES"
    SATISFIES = "SATISFIES"
    DERIVED_FROM = "DERIVED_FROM"
    CONFLICTS_WITH = "CONFLICTS_WITH"
    SUPERSEDES = "SUPERSEDES"


class EpistemicType(str, Enum):
    """Epistemic classification of knowledge and graph relations."""
    EXTRACTED = "EXTRACTED"
    INFERRED = "INFERRED"
    USER_CONFIRMED = "USER_CONFIRMED"
    AGENT_PROPOSED = "AGENT_PROPOSED"


class ProjectContract(BaseModel):
    """Formal Project Contract representation conforming to CORE-CONTRACT-001."""
    project_id: str
    name: str
    version: str = "0.1.0"
    description: str = ""
    author: str = ""
    documentation_language: str = "en"
    lifecycle_state: str = "greenfield"
    primary_harness: str = "antigravity"
    secondary_harnesses: list[str] = Field(default_factory=list)
    target_environments: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    governance: dict[str, Any] = Field(default_factory=dict)


class InvariantRuleModel(BaseModel):
    """Formal Architectural Invariant definition model."""
    id: str
    name: str
    description: str = ""
    severity: str = "CRITICAL"
    enforcement: str = "BLOCKING"
    scope_directory: str = ""
    forbidden_imports: list[str] = Field(default_factory=list)
    required_interfaces: list[str] = Field(default_factory=list)


class GraphNodeModel(BaseModel):
    """Representation of an entity node in the Repository Intelligence Graph."""
    id: str
    type: NodeType
    label: str
    file_path: Optional[str] = None
    line_range: Optional[tuple[int, int]] = None
    community_id: Optional[int] = None
    centrality: Optional[float] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphEdgeModel(BaseModel):
    """Representation of a directed relational edge in the Repository Intelligence Graph."""
    source: str
    target: str
    relation: EdgeRelation
    epistemic_type: EpistemicType = EpistemicType.EXTRACTED
    confidence: float = 1.0
    evidence_ref: Optional[str] = None


class TaskModel(BaseModel):
    """Contract-bounded task specification model conforming to CORE-CONTRACT-002."""
    task_id: str
    spec_id: str
    subspec_id: Optional[str] = None
    title: str
    status: str = "pending"
    target_files: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    assigned_agent_id: Optional[str] = None
    convergence_attempts: int = 0


class SpecModel(BaseModel):
    """Specification model conforming to Specification-Driven Development standards."""
    spec_id: str
    title: str
    status: str = "draft"
    requirements: list[str] = Field(default_factory=list)
    subspecs: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EvidenceModel(BaseModel):
    """Formal machine-verifiable evidence artifact model."""
    evidence_id: str
    claim: str
    type: str = "observed"
    source_file: Optional[str] = None
    line_range: Optional[tuple[int, int]] = None
    graph_node_id: Optional[str] = None
    verification_command: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    confidence: float = 1.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    git_commit: str = "HEAD"


class VerificationResultModel(BaseModel):
    """Multi-layer verification outcome model conforming to VERIF-CONTRACT-001."""
    verification_id: str
    task_id: str
    converged: bool
    verdict: str = "CONVERGED"
    test_passed: int = 0
    test_failed: int = 0
    type_errors: int = 0
    lint_violations: int = 0
    invariant_violations: list[str] = Field(default_factory=list)
    drift_detected: list[str] = Field(default_factory=list)
    oracle_trace: Optional[str] = None
    repair_eligibility: dict[str, Any] = Field(default_factory=dict)
    escalation_payload: Optional[dict[str, Any]] = None
    layer_results: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProgressEventModel(BaseModel):
    """Append-only progress event record conforming to EVENT-CONTRACT-001."""
    event_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    session_id: str
    task_id: Optional[str] = None
    agent_id: Optional[str] = None
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    git_commit: str = "HEAD"
