"""Level 9 Verification Suite: Heterogeneous Graph Relational Semantics & Epistemic Taxonomy."""

from pathlib import Path
from eidos.contracts.models import NodeType, EdgeRelation, EpistemicType
from eidos.graph.engine import RepositoryGraphEngine


def test_closed_edge_relations_conformance():
    """Level 9: System defines and respects the 11 closed architectural edge relations."""
    expected_relations = {
        "IMPLEMENTS",
        "DEPENDS_ON",
        "TESTED_BY",
        "DOCUMENTED_BY",
        "DEFINED_BY",
        "MODIFIED_BY",
        "VIOLATES",
        "SATISFIES",
        "DERIVED_FROM",
        "CONFLICTS_WITH",
        "SUPERSEDES",
    }
    actual_relations = {e.value for e in EdgeRelation}
    assert actual_relations == expected_relations


def test_heterogeneous_21_node_types_conformance():
    """Level 9: System defines the complete set of 21 heterogeneous node entities."""
    expected_types = {
        "File", "Directory", "Module", "Class", "Function", "API",
        "Database", "Dependency", "Test", "Spec", "SubSpec", "Task",
        "Contract", "Skill", "Rule", "Commit", "Finding", "Session",
        "Agent", "Feature", "Evidence",
    }
    actual_types = {n.value for n in NodeType}
    assert actual_types == expected_types


def test_epistemic_provenance_types():
    """Level 9: Epistemic provenance contains EXTRACTED, INFERRED, USER_CONFIRMED, AGENT_PROPOSED."""
    expected = {"EXTRACTED", "INFERRED", "USER_CONFIRMED", "AGENT_PROPOSED"}
    actual = {e.value for e in EpistemicType}
    assert actual == expected
