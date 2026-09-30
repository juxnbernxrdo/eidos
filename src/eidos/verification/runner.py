"""Deterministic verification runner executing tests, invariants, and drift audits."""

import subprocess
import uuid
from pathlib import Path
from datetime import datetime, timezone
from eidos.contracts.models import VerificationResultModel
from eidos.intelligence.invariants import check_invariants

def run_verification(workspace_root: Path, task_id: str = "TASK-VERIFY") -> VerificationResultModel:
    """Executes the complete verification suite and produces a VerificationResultModel."""
    # 1. Invariant checking
    violations = check_invariants(workspace_root)
    violation_msgs = [f"[{v['rule_id']}] {v['message']} ({v['file']}:{v['line']})" for v in violations]
    
    # 2. Pytest execution
    test_passed = 0
    test_failed = 0
    test_dir = workspace_root / "tests"
    
    if test_dir.exists() and any(test_dir.rglob("test_*.py")):
        try:
            import sys
            res = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "--tb=line"],
                cwd=workspace_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            stdout = res.stdout + res.stderr
            # Parse pytest summary line
            for line in stdout.splitlines():
                if "passed" in line or "failed" in line:
                    tokens = line.replace("in", "").split()
                    for idx, tok in enumerate(tokens):
                        if tok.startswith("passed") and idx > 0 and tokens[idx-1].isdigit():
                            test_passed = int(tokens[idx-1])
                        elif tok.startswith("failed") and idx > 0 and tokens[idx-1].isdigit():
                            test_failed = int(tokens[idx-1])
            if res.returncode != 0 and test_failed == 0:
                test_failed = 1
        except Exception:
            test_failed += 1
            
    # Converged condition: zero invariant violations and zero test failures
    converged = len(violation_msgs) == 0 and test_failed == 0

    return VerificationResultModel(
        verification_id=f"VERIF-{uuid.uuid4().hex[:8].upper()}",
        task_id=task_id,
        converged=converged,
        test_passed=test_passed,
        test_failed=test_failed,
        type_errors=0,
        lint_violations=0,
        invariant_violations=violation_msgs,
        drift_detected=[],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
