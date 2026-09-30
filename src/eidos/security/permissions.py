"""Security capability grant definitions, path canonicalization, and secret redaction.

Implements SPEC-008 (Security Boundaries & Sandbox Supervisor) and satisfies
REQ-SEC-001, REQ-SEC-002, REQ-SEC-003, AC-008-01, AC-008-02, AC-008-03:
    - Path isolation via os.path.realpath
    - Secret redaction via pattern scrubbing
    - Capability grant representation conforming to CORE-CONTRACT-008
"""

import fnmatch
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from eidos.core.exceptions import InvalidInputError, PermissionDeniedError

# Regex patterns for common secret keys and tokens
SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}", re.IGNORECASE),
    re.compile(r"ghp_[a-zA-Z0-9]{36,}", re.IGNORECASE),
    re.compile(r"github_pat_[a-zA-Z0-9_]{40,}", re.IGNORECASE),
    re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE),
    re.compile(r"AIza[0-9A-Za-z-_]{35}", re.IGNORECASE),
    re.compile(r"bearer\s+[a-zA-Z0-9\._-]{20,}", re.IGNORECASE),
]


def redact_secrets(text: str) -> str:
    """Sanitizes text by replacing high-entropy secrets and API tokens with [REDACTED_SECRET]."""
    if not text:
        return text
    sanitized = text
    for pattern in SECRET_PATTERNS:
        sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
    return sanitized


def canonicalize_and_confine_path(target_path: str | Path, workspace_root: str | Path) -> Path:
    """Resolves target_path to its canonical real path and verifies it resides within workspace_root.

    Detects directory traversal (../../) and symlink bypass.
    Raises:
        PermissionDeniedError: If the resolved path falls outside the workspace root.
    """
    root_resolved = Path(os.path.realpath(str(workspace_root))).resolve()
    target_str = str(target_path)

    # If relative, resolve against workspace root
    if not os.path.isabs(target_str):
        candidate = root_resolved / target_str
    else:
        candidate = Path(target_str)

    target_resolved = Path(os.path.realpath(str(candidate))).resolve()

    try:
        target_resolved.relative_to(root_resolved)
    except ValueError:
        raise PermissionDeniedError(
            f"Path traversal violation: Target '{target_path}' resolves to '{target_resolved}', "
            f"which is outside workspace root '{root_resolved}'",
            details={
                "target_path": str(target_path),
                "resolved_path": str(target_resolved),
                "workspace_root": str(root_resolved),
                "invariant": "INV-002",
            },
        )

    return target_resolved


def create_capability_grant(
    subject_id: str,
    subject_type: str = "AGENT",
    scope: str = "WORKTREE_ONLY",
    allowed_read_patterns: list[str] | None = None,
    allowed_write_patterns: list[str] | None = None,
    denied_patterns: list[str] | None = None,
    allow_subprocess: bool = False,
    allowed_binaries: list[str] | None = None,
    timeout_seconds: int = 30,
    network_egress: str = "DISABLED",
    allowed_hosts: list[str] | None = None,
) -> dict[str, Any]:
    """Builds a formal CapabilityPermissionContract dictionary conforming to CORE-CONTRACT-008."""
    return {
        "contract_id": "CORE-CONTRACT-008",
        "contract_version": "1.0.0",
        "grant_id": f"GRANT-{subject_id.upper()}",
        "subject": {
            "type": subject_type,
            "id": subject_id,
        },
        "filesystem": {
            "scope": scope,
            "allowed_read_patterns": allowed_read_patterns or ["*"],
            "allowed_write_patterns": allowed_write_patterns or ([] if scope == "READ_ONLY" else ["*"]),
            "denied_patterns": denied_patterns or [".git/*", ".env*", "*.pem", "*.key"],
        },
        "network": {
            "egress": network_egress,
            "allowed_hosts": allowed_hosts or [],
        },
        "execution": {
            "allow_subprocess": allow_subprocess,
            "allowed_binaries": allowed_binaries or [],
            "timeout_seconds": timeout_seconds,
        },
        "secret_access": False,
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }
