"""Level 8 Verification Suite: Security Boundaries, Symlink Attacks, and Secret Redaction."""

import os
from pathlib import Path
import pytest
from eidos.core.exceptions import PermissionDeniedError
from eidos.security.permissions import canonicalize_and_confine_path, redact_secrets
from eidos.security.supervisor import SandboxSupervisor


def test_symlink_directory_traversal_attack(tmp_path: Path):
    """Level 8: Symlink inside workspace pointing to external file is caught via realpath and blocked."""
    external_dir = tmp_path / "outside_sandbox"
    external_dir.mkdir()
    secret_file = external_dir / "confidential.txt"
    secret_file.write_text("SUPER_SECRET", encoding="utf-8")

    workspace = tmp_path / "workspace"
    workspace.mkdir()

    symlink_attack = workspace / "innocent_link.txt"
    try:
        os.symlink(secret_file, symlink_attack)
    except OSError:
        pytest.skip("Symlinks unsupported on host environment")

    supervisor = SandboxSupervisor(workspace)
    with pytest.raises(PermissionDeniedError) as exc_info:
        supervisor.validate_read(symlink_attack)

    assert "Path traversal violation" in str(exc_info.value)
    assert exc_info.value.details.get("invariant") == "INV-002"


def test_comprehensive_secret_scrubbing():
    """Level 8: Redacts diverse token formats (OpenAI, GitHub, AWS, Google, Bearer)."""
    samples = [
        ("sk-ant-api03-1234567890abcdefghijklmnopqrstuvwxyz", "[REDACTED_SECRET]"),
        ("ghp_123456789012345678901234567890123456", "[REDACTED_SECRET]"),
        ("github_pat_12345678901234567890123456789012345678901234567890", "[REDACTED_SECRET]"),
        ("AKIAIOSFODNN7EXAMPLE", "[REDACTED_SECRET]"),
        ("AIzaSyD-1234567890abcdef1234567890abcd", "[REDACTED_SECRET]"),
        ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.payload.signature", "[REDACTED_SECRET]"),
    ]

    for raw, expected in samples:
        sanitized = redact_secrets(f"Authentication token: {raw}")
        assert expected in sanitized
        assert raw not in sanitized
