"""Unit tests for the Repository Intelligence Graph engine."""

from pathlib import Path
from eidos.graph.engine import RepositoryGraphEngine

def test_graph_builder_and_analyzer():
    root = Path(__file__).parent.parent
    engine = RepositoryGraphEngine(root)
    G = engine.build()
    
    assert len(G) > 0
    metrics = engine.analyze()
    assert metrics["node_count"] > 0
    assert metrics["edge_count"] > 0
    assert "god_nodes" in metrics
    assert metrics["community_count"] > 0

def test_graph_path_query():
    root = Path(__file__).parent.parent
    engine = RepositoryGraphEngine(root)
    engine.build()
    
    # Query path between two known files
    path = engine.query_path("main.py", "models.py")
    # Even if no direct path exists, method should execute safely without unhandled exception
    assert isinstance(path, list)
