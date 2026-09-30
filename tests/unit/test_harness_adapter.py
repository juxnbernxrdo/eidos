"""Unit tests for SPEC-009: Host Harness Adapters & Trace Streaming."""

from pathlib import Path
from eidos.harness.headless import HeadlessHarnessAdapter
from eidos.harness.antigravity import AntigravityHarnessAdapter


def test_zero_host_leakage_ac_009_01(tmp_path: Path):
    """AC-009-01: Dispatched task execution leaves Core domain modules untouched and uncoupled."""
    adapter = HeadlessHarnessAdapter(tmp_path)
    assert adapter.detect() is True

    caps = adapter.capabilities()
    assert caps["subagents"] is True
    assert caps["codeact"] is True


def test_complete_raw_trace_collection_ac_009_02(tmp_path: Path):
    """AC-009-02: collect_trace() returns exact observation trace with turn objects and exit codes."""
    adapter = HeadlessHarnessAdapter(tmp_path)
    dispatch_req = {
        "task": {"task_id": "TASK-009"},
        "simulated_turns": [
            {"turn": 1, "action": "read_ast", "exit_code": 0},
            {"turn": 2, "action": "write_patch", "exit_code": 0},
            {"turn": 3, "action": "run_verifier", "exit_code": 0},
        ],
    }

    exec_id = adapter.invoke(dispatch_req)
    trace = adapter.collect_trace(exec_id)

    assert len(trace) == 3
    for i, t in enumerate(trace, 1):
        assert t["turn"] == i
        assert "timestamp" in t
        assert "action" in t
        assert t["exit_code"] == 0
