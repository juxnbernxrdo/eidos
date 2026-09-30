"""Unit tests for SPEC-005: Storage-Agnostic Repository Graph Engine."""

from pathlib import Path
import networkx as nx
from eidos.contracts.models import NodeType, EdgeRelation, EpistemicType
from eidos.graph.engine import RepositoryGraphEngine


def test_heterogeneous_nodes_and_extracted_provenance_ac_005_01(tmp_path: Path):
    """AC-005-01: Extracts File, Class, and Function nodes with EXTRACTED DEFINED_BY edges."""
    py_file = tmp_path / "sample.py"
    py_file.write_text(
        "class Order:\n"
        "    def checkout(self):\n"
        "        pass\n\n"
        "def helper():\n"
        "    pass\n",
        encoding="utf-8",
    )

    engine = RepositoryGraphEngine(tmp_path)
    G = engine.build()

    # Verify nodes
    file_id = "file:sample.py"
    cls_id = "class:sample.py#Order"
    fn_id = "fn:sample.py#helper"

    assert G.has_node(file_id)
    assert G.has_node(cls_id)
    assert G.has_node(fn_id)

    assert G.nodes[file_id]["type"] == NodeType.FILE.value
    assert G.nodes[cls_id]["type"] == NodeType.CLASS.value
    assert G.nodes[fn_id]["type"] == NodeType.FUNCTION.value

    # Verify EXTRACTED DEFINED_BY edges
    assert G.has_edge(file_id, cls_id)
    edge_cls = G.edges[file_id, cls_id]
    assert edge_cls["relation"] == EdgeRelation.DEFINED_BY.value
    assert edge_cls["epistemic_provenance"] == EpistemicType.EXTRACTED.value
    assert edge_cls["confidence"] == 1.0

    assert G.has_edge(file_id, fn_id)
    edge_fn = G.edges[file_id, fn_id]
    assert edge_fn["relation"] == EdgeRelation.DEFINED_BY.value
    assert edge_fn["epistemic_provenance"] == EpistemicType.EXTRACTED.value
    assert edge_fn["confidence"] == 1.0


def test_epistemic_precedence_over_inference_ac_005_02(tmp_path: Path):
    """AC-005-02: Conflicting INFERRED definition is quarantined as CONFLICTS_WITH."""
    py_file = tmp_path / "service.py"
    py_file.write_text("def process_payment(): pass\n", encoding="utf-8")

    engine = RepositoryGraphEngine(tmp_path)
    G = engine.build()

    true_file = "file:service.py"
    fn_node = "fn:service.py#process_payment"
    assert G.has_edge(true_file, fn_node)

    # Agent proposes an inferred edge claiming process_payment is defined in other_file.py
    fake_source = "file:other_file.py"
    res = engine.propose_edge(
        source=fake_source,
        target=fn_node,
        relation=EdgeRelation.DEFINED_BY.value,
        epistemic_provenance=EpistemicType.INFERRED.value,
        confidence=0.6,
    )

    assert res["status"] == "QUARANTINED"
    assert res["relation"] == EdgeRelation.CONFLICTS_WITH.value

    # Ground truth remains EXTRACTED
    assert G.edges[true_file, fn_node]["relation"] == EdgeRelation.DEFINED_BY.value
    assert G.edges[true_file, fn_node]["epistemic_provenance"] == EpistemicType.EXTRACTED.value

    # Proposed edge was recorded as CONFLICTS_WITH
    assert G.has_edge(fake_source, fn_node)
    assert G.edges[fake_source, fn_node]["relation"] == EdgeRelation.CONFLICTS_WITH.value


def test_hop_bounded_neighborhood_traversal_ac_005_03(tmp_path: Path):
    """AC-005-03: Neighborhood query from seed A with k_hops=2 returns only {A, B, C}."""
    engine = RepositoryGraphEngine(tmp_path)
    G = engine.graph
    # Build linear chain A -> B -> C -> D -> E
    G.add_edge("node:A", "node:B")
    G.add_edge("node:B", "node:C")
    G.add_edge("node:C", "node:D")
    G.add_edge("node:D", "node:E")

    subgraph = engine.traverse_neighborhood("node:A", k_hops=2)

    assert set(subgraph.nodes()) == {"node:A", "node:B", "node:C"}
    assert "node:D" not in subgraph.nodes()
    assert "node:E" not in subgraph.nodes()


def test_snapshot_export_conformance(tmp_path: Path):
    """Snapshot export contains valid contract structure."""
    py_file = tmp_path / "hello.py"
    py_file.write_text("def hello(): pass\n", encoding="utf-8")

    engine = RepositoryGraphEngine(tmp_path)
    engine.build()
    out_file = tmp_path / ".eidos" / "graph" / "snapshot.json"
    doc = engine.export_snapshot(out_file)

    assert doc["contract_id"] == "GRAPH-CONTRACT-001"
    assert "snapshot" in doc
    assert doc["snapshot"]["node_count"] > 0
    assert out_file.exists()
