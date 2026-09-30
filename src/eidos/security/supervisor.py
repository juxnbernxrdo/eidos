"""Sandbox supervisor enforcing Policy-as-Physics, capability confinement, and secret redaction.

Implements SPEC-008 (Security Boundaries, Capability Sandbox & Path Isolation) and satisfies
REQ-SEC-001, REQ-SEC-002, REQ-SEC-003, AC-008-01, AC-008-02, AC-008-03.
"""

import fnmatch
import os
import subprocess
from pathlib import Path
from typing import Any

from eidos.core.exceptions import (
    ExecutionTimeoutError,
    PermissionDeniedError,
)
from eidos.security.permissions import (
    canonicalize_and_confine_path,
    create_capability_grant,
    redact_secrets,
)


class SandboxSupervisor:
    """Policy-as-Physics supervisor intercepting tool, file, network, and execution operations."""

    def __init__(self, workspace_root: Path, capability_grant: dict[str, Any] | None = None):
        self.workspace_root = Path(os.path.realpath(str(workspace_root))).resolve()
        self.grant = capability_grant or create_capability_grant(
            subject_id="DEFAULT-SUPERVISOR",
            scope="WORKTREE_ONLY",
        )

    def validate_read(self, target_path: str | Path) -> Path:
        """Validates that reading target_path is authorized under the active capability grant."""
        resolved = canonicalize_and_confine_path(target_path, self.workspace_root)
        rel_str = str(resolved.relative_to(self.workspace_root))

        fs = self.grant.get("filesystem", {})
        denied_patterns = fs.get("denied_patterns", [])
        for pat in denied_patterns:
            if fnmatch.fnmatch(rel_str, pat) or fnmatch.fnmatch(resolved.name, pat):
                raise PermissionDeniedError(
                    f"Read denied by pattern '{pat}': {rel_str}",
                    details={"path": rel_str, "denied_pattern": pat},
                )

        return resolved

    def validate_write(self, target_path: str | Path) -> Path:
        """Validates that writing to target_path is authorized under the active capability grant."""
        fs = self.grant.get("filesystem", {})
        scope = fs.get("scope", "READ_ONLY")

        # AC-008-01: READ_ONLY grants fail-closed on write attempts
        if scope == "READ_ONLY":
            raise PermissionDeniedError(
                f"Write permission denied: Capability scope is strictly READ_ONLY for subject '{self.grant.get('subject', {}).get('id')}'",
                details={"scope": scope, "target": str(target_path)},
            )

        resolved = canonicalize_and_confine_path(target_path, self.workspace_root)
        rel_str = str(resolved.relative_to(self.workspace_root))

        # Check denied patterns
        denied_patterns = fs.get("denied_patterns", [])
        for pat in denied_patterns:
            if fnmatch.fnmatch(rel_str, pat) or fnmatch.fnmatch(resolved.name, pat):
                raise PermissionDeniedError(
                    f"Write denied by pattern '{pat}': {rel_str}",
                    details={"path": rel_str, "denied_pattern": pat},
                )

        # Check allowed write patterns
        allowed_write_patterns = fs.get("allowed_write_patterns", [])
        if allowed_write_patterns and not any(fnmatch.fnmatch(rel_str, pat) for pat in allowed_write_patterns):
            raise PermissionDeniedError(
                f"Path '{rel_str}' does not match any allowed write patterns: {allowed_write_patterns}",
                details={"path": rel_str, "allowed": allowed_write_patterns},
            )

        return resolved

    def validate_network(self, host: str) -> None:
        """Validates network egress request against capability grant."""
        net = self.grant.get("network", {})
        egress = net.get("egress", "DISABLED")

        if egress == "DISABLED":
            raise PermissionDeniedError(
                f"Network egress is DISABLED for subject '{self.grant.get('subject', {}).get('id')}'",
                details={"host": host, "egress": egress},
            )

        if egress == "LOOPBACK_ONLY":
            if host not in ("127.0.0.1", "localhost", "::1"):
                raise PermissionDeniedError(
                    f"Network egress restricted to LOOPBACK_ONLY; cannot connect to '{host}'",
                    details={"host": host, "egress": egress},
                )

        if egress == "HOST_WHITELIST":
            allowed = net.get("allowed_hosts", [])
            if host not in allowed:
                raise PermissionDeniedError(
                    f"Host '{host}' is not in allowed_hosts whitelist: {allowed}",
                    details={"host": host, "allowed_hosts": allowed},
                )

    def validate_execution(self, binary: str) -> None:
        """Validates subprocess binary execution against capability grant."""
        execution = self.grant.get("execution", {})
        if not execution.get("allow_subprocess", False):
            raise PermissionDeniedError(
                f"Subprocess execution is forbidden for subject '{self.grant.get('subject', {}).get('id')}'",
                details={"binary": binary},
            )

        allowed_binaries = execution.get("allowed_binaries", [])
        bin_name = Path(binary).name
        if allowed_binaries and bin_name not in allowed_binaries:
            raise PermissionDeniedError(
                f"Binary '{bin_name}' is not in allowed execution whitelist: {allowed_binaries}",
                details={"binary": bin_name, "allowed_binaries": allowed_binaries},
            )

    def sanitize_output(self, raw_text: str) -> str:
        """Scans and scrubs secrets from command or model outputs."""
        return redact_secrets(raw_text)

    def execute_sandboxed_command(
        self,
        command: list[str],
        cwd: Path | None = None,
        timeout: int | None = None,
    ) -> tuple[int, str, str]:
        """Executes a subprocess under sandbox supervision, redacting any secrets in stdout/stderr."""
        if not command:
            raise ValueError("Command list cannot be empty")

        binary = command[0]
        self.validate_execution(binary)

        effective_cwd = self.validate_read(cwd or self.workspace_root)
        exec_cfg = self.grant.get("execution", {})
        timeout_sec = timeout or exec_cfg.get("timeout_seconds", 30)

        try:
            res = subprocess.run(
                command,
                cwd=effective_cwd,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
            )
            stdout = self.sanitize_output(res.stdout)
            stderr = self.sanitize_output(res.stderr)
            return res.returncode, stdout, stderr
        except subprocess.TimeoutExpired as e:
            out = self.sanitize_output(e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or ""))
            err = self.sanitize_output(e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or ""))
            raise ExecutionTimeoutError(
                f"Command '{' '.join(command)}' exceeded timeout of {timeout_sec}s",
                details={"stdout": out, "stderr": err, "timeout": timeout_sec},
            )
