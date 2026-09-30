"""Integration tests for SPEC-006: 7-Layer Verification Runner & Bounded Repair Loop."""

from pathlib import Path
from eidos.verification.runner import run_verification


def test_convergence_on_pass_ac_006_01(tmp_path: Path):
    """AC-006-01: When all active layers pass with 0 failures, verdict is CONVERGED."""
    # Create valid code and passing test
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "lib.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")

    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    (test_dir / "test_lib.py").write_text("from src.lib import add\ndef test_add(): assert add(2, 3) == 5\n", encoding="utf-8")

    res = run_verification(
        workspace_root=tmp_path,
        task_id="TASK-CONV-01",
        attempt_index=1,
        max_repair_attempts_k=5,
        active_layers=["tests", "static_types", "lint", "invariants", "security"],
    )

    assert res.converged is True
    assert res.verdict == "CONVERGED"
    assert res.test_failed == 0
    assert res.test_passed == 1
    assert res.repair_eligibility["is_eligible"] is False


def test_repair_eligibility_with_oracle_trace_ac_006_02(tmp_path: Path):
    """AC-006-02: Test failure with attempts=1 and K=5 yields REPAIR_ELIGIBLE with oracle trace."""
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "calc.py").write_text("def mul(a, b): return a + b  # Bug!\n", encoding="utf-8")

    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    (test_dir / "test_calc.py").write_text(
        "from src.calc import mul\n"
        "def test_mul():\n"
        "    assert mul(2, 3) == 6\n",
        encoding="utf-8",
    )

    res = run_verification(
        workspace_root=tmp_path,
        task_id="TASK-REPAIR-01",
        attempt_index=1,
        max_repair_attempts_k=5,
        active_layers=["tests", "static_types", "invariants"],
    )

    assert res.converged is False
    assert res.verdict == "REPAIR_ELIGIBLE"
    assert res.test_failed == 1
    assert res.repair_eligibility["is_eligible"] is True
    assert "assert mul(2, 3) == 6" in res.repair_eligibility.get("external_oracle_trace", "") or "assert 5 == 6" in res.repair_eligibility.get("external_oracle_trace", "")


def test_exhaustion_escalation_ac_006_03(tmp_path: Path):
    """AC-006-03: Test failure at attempt=5 with K=5 results in ESCALATED."""
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "stub.py").write_text("def fail(): return False\n", encoding="utf-8")

    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    (test_dir / "test_stub.py").write_text("from src.stub import fail\ndef test_stub(): assert fail() is True\n", encoding="utf-8")

    res = run_verification(
        workspace_root=tmp_path,
        task_id="TASK-ESC-01",
        attempt_index=5,
        max_repair_attempts_k=5,
        active_layers=["tests", "static_types", "invariants"],
    )

    assert res.converged is False
    assert res.verdict == "ESCALATED"
    assert res.repair_eligibility["is_eligible"] is False
    assert res.escalation_payload is not None
    assert res.escalation_payload["reason"] == "ATTEMPTS_EXHAUSTED"
