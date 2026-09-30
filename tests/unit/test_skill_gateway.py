"""Unit tests for SPEC-012: Skill Gateway & Lifecycle Verification."""

from pathlib import Path
import pytest
from eidos.core.exceptions import PermissionDeniedError
from eidos.skills.gateway import SkillGateway


def test_malicious_pattern_rejection_ac_012_01(tmp_path: Path):
    """AC-012-01: Skill containing raw socket network connection is rejected with risk >= 25."""
    gateway = SkillGateway(tmp_path, risk_threshold=25)

    malicious_skill_dir = tmp_path / "skills" / "malicious"
    malicious_skill_dir.mkdir(parents=True)
    (malicious_skill_dir / "exploit.py").write_text(
        "import socket\ns = socket.connect(('1.2.3.4', 8080))\n",
        encoding="utf-8",
    )

    with pytest.raises(PermissionDeniedError) as exc_info:
        gateway.audit_and_install_skill("malicious_skill", malicious_skill_dir)

    assert "exceeds threshold 25" in str(exc_info.value)
    assert not (tmp_path / ".eidos" / "skills-lock.json").exists()


def test_lockfile_hash_pinning_ac_012_02(tmp_path: Path):
    """AC-012-02: Valid, clean skill is installed and pinned in skills-lock.json with SHA-256."""
    gateway = SkillGateway(tmp_path, risk_threshold=25)

    safe_skill_dir = tmp_path / "skills" / "safe_skill"
    safe_skill_dir.mkdir(parents=True)
    script_path = safe_skill_dir / "helper.py"
    script_path.write_text("def format_text(s):\n    return s.strip().title()\n", encoding="utf-8")

    entry = gateway.audit_and_install_skill("safe_skill", safe_skill_dir)

    assert entry["skill_name"] == "safe_skill"
    assert entry["risk_score"] < 25
    assert "helper.py" in entry["script_hashes"]

    # Verify lockfile on disk
    assert (tmp_path / ".eidos" / "skills-lock.json").exists()
    assert gateway.verify_skill_integrity("safe_skill", safe_skill_dir) is True
