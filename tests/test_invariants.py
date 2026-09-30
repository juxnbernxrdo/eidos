"""Unit tests for the architectural invariant checker."""

from pathlib import Path
from eidos.intelligence.invariants import check_invariants, load_default_invariants
from eidos.contracts.models import InvariantRuleModel

def test_load_default_invariants():
    rules = load_default_invariants()
    assert len(rules) >= 2
    rule_ids = [r.id for r in rules]
    assert "ARCH-001" in rule_ids
    assert "ARCH-002" in rule_ids

def test_check_invariants_clean_workspace():
    root = Path(__file__).parent.parent
    violations = check_invariants(root)
    # The Eidos codebase must satisfy its own architectural invariants
    assert len(violations) == 0, f"Eidos violates its own invariants: {violations}"

def test_detect_synthetic_violation(tmp_path):
    # Create a synthetic violation
    core_file = tmp_path / "src" / "eidos" / "core" / "bad.py"
    core_file.parent.mkdir(parents=True)
    core_file.write_text("import eidos.cli.main\n")
    
    rule = InvariantRuleModel(
        id="ARCH-TEST",
        name="test-rule",
        scope_directory="src/eidos/core",
        forbidden_imports=["eidos.cli"],
    )
    violations = check_invariants(tmp_path, rules=[rule])
    assert len(violations) == 1
    assert violations[0]["rule_id"] == "ARCH-TEST"
