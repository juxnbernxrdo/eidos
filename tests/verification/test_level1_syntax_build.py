"""Level 1 Verification Suite: Syntax, AST Parsing, Compilation, and Packaging Entrypoints."""

import ast
import subprocess
import sys
from pathlib import Path


def test_all_source_files_syntactically_valid():
    """Level 1: Every Python source file under src/eidos must compile cleanly via ast.parse."""
    repo_root = Path(__file__).parent.parent.parent
    src_dir = repo_root / "src" / "eidos"
    py_files = list(src_dir.rglob("*.py"))
    assert len(py_files) > 0, "No source files discovered in src/eidos"

    for py_file in py_files:
        content = py_file.read_text(encoding="utf-8")
        try:
            tree = ast.parse(content, filename=str(py_file))
            assert tree is not None
        except SyntaxError as e:
            raise AssertionError(f"Syntax error in {py_file}: {e}")


def test_cli_entrypoint_execution():
    """Level 1: CLI entrypoint 'eidos' must execute without packaging or import failure."""
    res = subprocess.run(
        [sys.executable, "-m", "eidos.cli.main", "--help"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert res.returncode == 0
    assert "Engineering Intelligence for Deterministic, Orchestrated Software" in res.stdout


def test_clean_module_importability():
    """Level 1: All primary subsystems are directly importable without circular or missing dependencies."""
    import eidos.core.state
    import eidos.core.exceptions
    import eidos.orchestration.pipeline
    import eidos.orchestration.task
    import eidos.context.router
    import eidos.graph.engine
    import eidos.verification.runner
    import eidos.security.supervisor
    import eidos.security.permissions
    import eidos.progress.logger
    import eidos.progress.projector
    import eidos.progress.passport
    import eidos.harness.base
    import eidos.harness.headless
    import eidos.harness.antigravity
    import eidos.memory.manager
    import eidos.skills.gateway
    import eidos.evolution.pipeline

    assert True
