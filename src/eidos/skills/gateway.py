"""Skill Gateway governing static security inspection, risk scoring, and lockfile pinning.

Implements SPEC-012 (Skill Gateway & Lifecycle Verification) and satisfies
REQ-SKILL-001, REQ-SKILL-002, AC-012-01, AC-012-02:
    - Static AST and pattern inspection for malicious execution primitives
    - Rejection of skills exceeding risk score cutoff (risk >= 25)
    - Cryptographic SHA-256 hash pinning in skills-lock.json
"""

import ast
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from eidos.core.exceptions import (
    ContractViolationError,
    InvalidInputError,
    PermissionDeniedError,
)

DANGEROUS_CALLS = {
    "eval": 30,
    "exec": 30,
    "compile": 20,
    "__import__": 25,
}

DANGEROUS_ATTRIBUTES = {
    "system": 25,
    "popen": 25,
    "connect": 30,
    "bind": 30,
    "listen": 30,
}

DANGEROUS_MODULES = {
    "socket": 30,
    "subprocess": 20,
    "paramiko": 30,
    "ctypes": 30,
}


class SkillGateway:
    """Audits and pins external agent skills into the repository."""

    def __init__(self, workspace_root: Path, risk_threshold: int = 25):
        self.workspace_root = workspace_root.resolve()
        self.risk_threshold = risk_threshold
        self.lockfile_path = self.workspace_root / ".eidos" / "skills-lock.json"

    def scan_python_code(self, code: str) -> tuple[int, list[dict[str, Any]]]:
        """Performs static AST inspection and computes risk score."""
        findings: list[dict[str, Any]] = []
        total_risk = 0

        # Regex check for raw socket calls or obfuscated strings
        if re.search(r"socket\.connect\(", code):
            total_risk += 30
            findings.append({
                "rule": "RAW_SOCKET_CONNECT",
                "severity": "CRITICAL",
                "risk_points": 30,
                "message": "Raw socket network connection detected",
            })

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return 30, [{"rule": "SYNTAX_ERROR", "severity": "HIGH", "risk_points": 30, "message": str(e)}]

        for node in ast.walk(tree):
            # Check function calls
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id in DANGEROUS_CALLS:
                    pts = DANGEROUS_CALLS[func.id]
                    total_risk += pts
                    findings.append({
                        "rule": f"DANGEROUS_CALL_{func.id.upper()}",
                        "severity": "CRITICAL",
                        "risk_points": pts,
                        "message": f"Execution of dangerous built-in '{func.id}'",
                    })
                elif isinstance(func, ast.Attribute) and func.attr in DANGEROUS_ATTRIBUTES:
                    pts = DANGEROUS_ATTRIBUTES[func.attr]
                    total_risk += pts
                    findings.append({
                        "rule": f"DANGEROUS_METHOD_{func.attr.upper()}",
                        "severity": "CRITICAL",
                        "risk_points": pts,
                        "message": f"Invocation of dangerous attribute '{func.attr}'",
                    })

            # Check imports
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in DANGEROUS_MODULES:
                            pts = DANGEROUS_MODULES[alias.name]
                            total_risk += pts
                            findings.append({
                                "rule": f"SUSPICIOUS_IMPORT_{alias.name.upper()}",
                                "severity": "HIGH",
                                "risk_points": pts,
                                "message": f"Import of dangerous module '{alias.name}'",
                            })

        return total_risk, findings

    def audit_and_install_skill(self, skill_name: str, skill_dir: Path) -> dict[str, Any]:
        """Audits a skill package and pins it in skills-lock.json (AC-012-01, AC-012-02)."""
        if not skill_dir.exists():
            raise InvalidInputError(f"Skill directory '{skill_dir}' does not exist")

        scripts = list(skill_dir.rglob("*.py"))
        total_risk = 0
        all_findings: list[dict[str, Any]] = []
        hashes: dict[str, str] = {}

        for script in scripts:
            content = script.read_text(encoding="utf-8")
            h = hashlib.sha256(content.encode("utf-8")).hexdigest()
            hashes[script.name] = h

            risk, findings = self.scan_python_code(content)
            total_risk += risk
            all_findings.extend(findings)

        # AC-012-01: Reject skills exceeding the risk cutoff (risk >= 25)
        if total_risk >= self.risk_threshold:
            raise PermissionDeniedError(
                f"Skill '{skill_name}' rejected: Risk score {total_risk} exceeds threshold {self.risk_threshold}",
                details={"skill_name": skill_name, "risk_score": total_risk, "findings": all_findings},
            )

        # AC-012-02: Commit cryptographic hash pinning in skills-lock.json
        lock_entry = {
            "skill_name": skill_name,
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "risk_score": total_risk,
            "script_hashes": hashes,
        }

        self.lockfile_path.parent.mkdir(parents=True, exist_ok=True)
        current_lock = {}
        if self.lockfile_path.exists():
            try:
                current_lock = json.loads(self.lockfile_path.read_text(encoding="utf-8"))
            except Exception:
                current_lock = {}

        current_lock[skill_name] = lock_entry
        self.lockfile_path.write_text(json.dumps(current_lock, indent=2), encoding="utf-8")

        return lock_entry

    def verify_skill_integrity(self, skill_name: str, skill_dir: Path) -> bool:
        """Verifies that installed skill files match the cryptographic hashes in skills-lock.json."""
        if not self.lockfile_path.exists():
            return False

        try:
            lock = json.loads(self.lockfile_path.read_text(encoding="utf-8"))
        except Exception:
            return False

        entry = lock.get(skill_name)
        if not entry:
            return False

        recorded_hashes = entry.get("script_hashes", {})
        for script in skill_dir.rglob("*.py"):
            if script.name in recorded_hashes:
                curr_h = hashlib.sha256(script.read_bytes()).hexdigest()
                if curr_h != recorded_hashes[script.name]:
                    return False

        return True
