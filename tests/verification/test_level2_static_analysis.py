"""Level 2 Verification Suite: Static Analysis, Boundary Separation & Circular Dependency Audit."""

import ast
from pathlib import Path
import networkx as nx
from eidos.intelligence.parser import parse_python_file


def test_circular_dependency_audit():
    """Level 2: Internal module import dependency graph must be a Directed Acyclic Graph (DAG)."""
    repo_root = Path(__file__).parent.parent.parent
    src_dir = repo_root / "src" / "eidos"
    py_files = list(src_dir.rglob("*.py"))

    import_graph = nx.DiGraph()

    for py_file in py_files:
        rel_mod = "eidos." + ".".join(py_file.relative_to(src_dir).with_suffix("").parts)
        parsed = parse_python_file(py_file, repo_root)
        if not parsed:
            continue
        import_graph.add_node(rel_mod)
        for imp in parsed["imports"]:
            mod = imp["module"]
            if mod.startswith("eidos.") and mod != rel_mod:
                import_graph.add_edge(rel_mod, mod)

    # Detect cycles
    cycles = list(nx.simple_cycles(import_graph))
    assert len(cycles) == 0, f"Circular module dependencies detected: {cycles}"


def test_public_api_docstrings_present():
    """Level 2: All top-level classes and functions must possess descriptive docstrings."""
    repo_root = Path(__file__).parent.parent.parent
    src_dir = repo_root / "src" / "eidos"

    for py_file in src_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                doc = ast.get_docstring(node)
                assert doc is not None and len(doc.strip()) > 0, (
                    f"Entity '{node.name}' in {py_file.name} lacks a docstring"
                )
