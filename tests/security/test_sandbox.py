"""Unit & security tests for SPEC-008: Security Boundaries, Capability Sandbox & Path Isolation."""

from pathlib import Path
import pytest

from eidos.core.exceptions import PermissionDeniedError
from eidos.security.permissions import (
    create_capability_grant,
    redact_secrets,
)
from eidos.security.supervisor import SandboxSupervisor


def test_default_deny_file_write_ac_008_01(tmp_path: Path):
    """AC-008-01: Subagent granted READ_ONLY cannot write to any file."""
    grant = create_capability_grant(
        subject_id="SUBAGENT-RO",
        scope="READ_ONLY",
    )
    supervisor = SandboxSupervisor(tmp_path, grant)

    target_file = tmp_path / "src" / "main.py"
    with pytest.raises(PermissionDeniedError) as exc_info:
        supervisor.validate_write(target_file)

    assert "strictly READ_ONLY" in str(exc_info.value)
    assert exc_info.value.code == "PERMISSION_DENIED"


def test_cross_project_path_confinement_ac_008_02(tmp_path: Path):
    """AC-008-02: Operations attempting to access paths outside workspace root fail closed."""
    proj_a = tmp_path / "project-a"
    proj_b = tmp_path / "project-b"
    proj_a.mkdir()
    proj_b.mkdir()

    secret_in_b = proj_b / "secret.txt"
    secret_in_b.write_text("classified", encoding="utf-8")

    grant = create_capability_grant(subject_id="AGENT-A", scope="WORKTREE_ONLY")
    supervisor = SandboxSupervisor(proj_a, grant)

    # Attempt to read project-b from project-a context
    with pytest.raises(PermissionDeniedError) as exc_info:
        supervisor.validate_read(secret_in_b)

    assert "Path traversal violation" in str(exc_info.value)
    assert exc_info.value.details.get("invariant") == "INV-002"

    # Attempt path traversal via ../project-b
    traversal_path = proj_a / ".." / "project-b" / "secret.txt"
    with pytest.raises(PermissionDeniedError) as exc_info2:
        supervisor.validate_read(traversal_path)

    assert "Path traversal violation" in str(exc_info2.value)


def test_secret_redaction_ac_008_03(tmp_path: Path):
    """AC-008-03: Sensitive API key patterns are replaced with [REDACTED_SECRET]."""
    grant = create_capability_grant(subject_id="TEST-SEC", scope="WORKTREE_ONLY")
    supervisor = SandboxSupervisor(tmp_path, grant)

    raw_output = "Connected to model using token sk-proj-123456789abcdef0123456789 and ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 successfully."
    sanitized = supervisor.sanitize_output(raw_output)

    assert "sk-proj-123456789abcdef0123456789" not in sanitized
    assert "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" not in sanitized
    assert "[REDACTED_SECRET]" in sanitized
    assert sanitized == "Connected to model using token [REDACTED_SECRET] and [REDACTED_SECRET] successfully."


def test_network_egress_blocking(tmp_path: Path):
    """Network egress fails closed when set to DISABLED."""
    grant = create_capability_grant(subject_id="NET-TEST", network_egress="DISABLED")
    supervisor = SandboxSupervisor(tmp_path, grant)

    with pytest.raises(PermissionDeniedError) as exc_info:
        supervisor.validate_network("api.openai.com")

    assert "Network egress is DISABLED" in str(exc_info.value)


def test_execution_whitelist(tmp_path: Path):
    """Executing binary outside allowed_binaries fails closed."""
    grant = create_capability_grant(
        subject_id="EXEC-TEST",
        allow_subprocess=True,
        allowed_binaries=["pytest", "git"],
    )
    supervisor = SandboxSupervisor(tmp_path, grant)

    # Allowed binary
    supervisor.validate_execution("pytest")

    # Disallowed binary
    with pytest.raises(PermissionDeniedError) as exc_info:
        supervisor.validate_execution("curl")

    assert "Binary 'curl' is not in allowed execution whitelist" in str(exc_info.value)
