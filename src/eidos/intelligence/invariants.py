"""Architectural invariants engine validating boundary rules."""

from pathlib import Path
from typing import Any
from eidos.contracts.models import InvariantRuleModel
from eidos.intelligence.parser import parse_python_file

def load_default_invariants() -> list[InvariantRuleModel]:
    """Provides foundational architectural invariants for Eidos."""
    return [
        InvariantRuleModel(
            id="ARCH-001",
            name="core-layer-isolation",
            description="Core domain must not depend on CLI or outer adapters",
            severity="CRITICAL",
            enforcement="BLOCKING",
            scope_directory="src/eidos/core",
            forbidden_imports=["eidos.cli", "eidos.harness"],
        ),
        InvariantRuleModel(
            id="ARCH-002",
            name="contracts-independence",
            description="Contracts must not depend on CLI, Intelligence, or Graph engines",
            severity="CRITICAL",
            enforcement="BLOCKING",
            scope_directory="src/eidos/contracts",
            forbidden_imports=["eidos.cli", "eidos.intelligence", "eidos.graph", "eidos.verification"],
        ),
    ]

def check_invariants(workspace_root: Path, rules: list[InvariantRuleModel] | None = None) -> list[dict[str, Any]]:
    """Evaluates all invariant rules against the workspace AST."""
    if rules is None:
        rules = load_default_invariants()
        
    violations = []
    py_files = [f for f in workspace_root.rglob("*.py") if not any(p.startswith((".", "venv", "__pycache__")) for p in f.parts)]
    
    for py_file in py_files:
        rel_path = str(py_file.relative_to(workspace_root))
        parsed = parse_python_file(py_file, workspace_root)
        if not parsed:
            continue
            
        for rule in rules:
            if rule.scope_directory and not rel_path.startswith(rule.scope_directory):
                continue
                
            for imp in parsed["imports"]:
                mod = imp["module"]
                for forbidden in rule.forbidden_imports:
                    if mod == forbidden or mod.startswith(f"{forbidden}."):
                        violations.append({
                            "rule_id": rule.id,
                            "rule_name": rule.name,
                            "severity": rule.severity,
                            "file": rel_path,
                            "line": imp["line"],
                            "message": f"File '{rel_path}' illegally imports forbidden module '{mod}'",
                        })
                        
    return violations
