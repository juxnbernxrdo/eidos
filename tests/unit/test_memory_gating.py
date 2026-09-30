"""Unit tests for SPEC-011: Tripartite Memory Boundaries & Opt-in Admission Gates."""

from pathlib import Path
from eidos.memory.manager import TripartiteMemoryManager


def test_default_opt_in_gating_ac_011_01(tmp_path: Path):
    """AC-011-01: Default configuration (opt_in_memory=False) ignores write and emits advisory."""
    memory_mgr = TripartiteMemoryManager(tmp_path, opt_in_memory=False)

    res = memory_mgr.persist_project_memory(
        key="heuristics_01",
        content="Always run tests before commit",
        task_id="TASK-011",
    )

    assert res["admitted"] is False
    assert res["status"] == "IGNORED_OPT_IN_DISABLED"
    assert "disabled by default" in res["message"]
    # No file written to disk
    assert not (tmp_path / ".eidos" / "memory" / "heuristics_01.json").exists()


def test_cross_project_isolation_ac_011_02(tmp_path: Path):
    """AC-011-02: Query in Repo-A returns only Repo-A memories, zero from Repo-B."""
    repo_a = tmp_path / "repo_a"
    repo_b = tmp_path / "repo_b"
    repo_a.mkdir()
    repo_b.mkdir()

    mgr_a = TripartiteMemoryManager(repo_a, opt_in_memory=True)
    mgr_b = TripartiteMemoryManager(repo_b, opt_in_memory=True)

    # Persist in Repo-A
    mgr_a.persist_project_memory("key_a", "Specific insight for repo A")
    # Persist in Repo-B
    mgr_b.persist_project_memory("key_b", "Specific insight for repo B")

    # Query in Repo-A
    results_a = mgr_a.query_project_memory()
    keys_a = [r["key"] for r in results_a]

    assert "key_a" in keys_a
    assert "key_b" not in keys_a
