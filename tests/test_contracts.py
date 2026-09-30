"""Unit tests for Eidos Pydantic contract models."""

import pytest
from eidos.contracts.models import (
    ProjectContract,
    SpecModel,
    TaskModel,
    GraphNodeModel,
    NodeType,
    GraphEdgeModel,
    EdgeRelation,
    EpistemicType,
    EvidenceModel,
    VerificationResultModel,
    ProgressEventModel,
)

def test_project_contract_validation():
    contract = ProjectContract(
        project_id="PROJ-001",
        name="TestProject",
        documentation_language="es",
        lifecycle_state="existing",
        primary_harness="antigravity",
    )
    assert contract.project_id == "PROJ-001"
    assert contract.documentation_language == "es"
    assert contract.primary_harness == "antigravity"

def test_spec_and_task_models():
    spec = SpecModel(
        spec_id="SPEC-001",
        title="Authentication Spec",
        requirements=["Require JWT token validation"],
        acceptance_criteria=["Unit tests pass"],
    )
    assert spec.spec_id == "SPEC-001"
    
    task = TaskModel(
        task_id="TASK-001",
        spec_id=spec.spec_id,
        title="Implement JWT Handler",
        target_files=["src/auth/jwt.py"],
    )
    assert task.spec_id == "SPEC-001"
    assert task.status == "pending"

def test_graph_node_and_edge_models():
    node = GraphNodeModel(
        id="fn:auth#verify",
        type=NodeType.FUNCTION,
        label="verify",
        file_path="src/auth.py",
        line_range=(10, 25),
    )
    assert node.type == NodeType.FUNCTION
    
    edge = GraphEdgeModel(
        source="file:src/auth.py",
        target=node.id,
        relation=EdgeRelation.DEFINED_BY,
        epistemic_type=EpistemicType.EXTRACTED,
        confidence=1.0,
    )
    assert edge.relation == EdgeRelation.DEFINED_BY
    assert edge.epistemic_type == EpistemicType.EXTRACTED

def test_verification_result_model():
    result = VerificationResultModel(
        verification_id="VERIF-001",
        task_id="TASK-001",
        converged=True,
        test_passed=10,
        test_failed=0,
    )
    assert result.converged is True
    assert result.test_passed == 10
