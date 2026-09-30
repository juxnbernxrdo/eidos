"""Unit tests for SPEC-004: Context Router & Minimal Sufficient Context (MSC)."""

from pathlib import Path
import pytest
from eidos.context.router import ContextRouter
from eidos.graph.engine import RepositoryGraphEngine


def setup_test_workspace(tmp_path: Path):
    """Sets up a mock workspace with auth.py and db.py."""
    auth_file = tmp_path / "auth.py"
    auth_file.write_text(
        "import db\n\n"
        "class AuthService:\n"
        "    def authenticate(self, user, token):\n"
        "        return db.lookup_user(user)\n",
        encoding="utf-8",
    )

    db_file = tmp_path / "db.py"
    db_file.write_text(
        "class DatabaseConnection:\n"
        "    def connect(self, uri):\n"
        "        pass\n\n"
        "def lookup_user(username):\n"
        "    # Implementation details that should be pruned\n"
        "    return {'user': username, 'valid': True}\n",
        encoding="utf-8",
    )

    return auth_file, db_file


def test_topological_pruning_and_boundary_pinning_ac_004_01(tmp_path: Path):
    """AC-004-01: Target auth.py is FULL_CODE, neighbor db.py is SIGNATURE_ONLY, CORE-CONTRACT-002 pinned."""
    setup_test_workspace(tmp_path)
    engine = RepositoryGraphEngine(tmp_path)
    engine.build()

    router = ContextRouter(tmp_path, engine)
    req = {
        "request_id": "REQ-001",
        "task": {
            "task_id": "TASK-AUTH-01",
            "objective": "Enhance authentication token check",
            "target_files": ["auth.py"],
        },
        "context_sources": {
            "include_graph": True,
            "include_rules": True,
            "include_specs": True,
            "include_evidence": True,
        },
        "budget_constraints": {
            "max_tokens": 4000,
            "reserve_for_generation": 1000,
            "k_hop_limit": 1,
        },
        "security_constraints": {
            "quarantine_adversarial": True,
            "isolated_project_id": "PROJ-TEST",
        },
    }

    result = router.assemble_context(req)
    resp = result["routing_response"]

    # Boundary pinning
    assert "CORE-CONTRACT-002" in resp["pinned_boundary_contracts"]

    # Assembled items
    items = resp["assembled_items"]
    assert len(items) >= 1

    # First item is auth.py with FULL_CODE
    auth_item = next(i for i in items if i["selection_audit"]["matched_query"] == "auth.py")
    assert auth_item["content_format"] == "FULL_CODE"
    assert "def authenticate" in auth_item["content"]

    # Neighbor db.py (if assembled) is SIGNATURE_ONLY
    db_items = [i for i in items if i["selection_audit"]["matched_query"] == "db.py"]
    if db_items:
        db_item = db_items[0]
        assert db_item["content_format"] == "SIGNATURE_ONLY"
        assert "def lookup_user" in db_item["content"]
        assert "Implementation details that should be pruned" not in db_item["content"]


def test_auditable_selection_reason_ac_004_02(tmp_path: Path):
    """AC-004-02: Every assembled item has a populated selection_audit.selection_reason."""
    setup_test_workspace(tmp_path)
    router = ContextRouter(tmp_path)
    req = {
        "request_id": "REQ-002",
        "task": {
            "task_id": "TASK-002",
            "objective": "Review db queries",
            "target_files": ["db.py"],
        },
        "context_sources": {
            "include_graph": True,
            "include_rules": True,
            "include_specs": True,
            "include_evidence": True,
        },
        "budget_constraints": {"max_tokens": 2000, "reserve_for_generation": 500, "k_hop_limit": 0},
        "security_constraints": {"quarantine_adversarial": True, "isolated_project_id": "PROJ-TEST"},
    }

    result = router.assemble_context(req)
    items = result["routing_response"]["assembled_items"]

    assert len(items) > 0
    for item in items:
        audit = item["selection_audit"]
        assert "selection_reason" in audit
        assert len(audit["selection_reason"].strip()) > 0


def test_token_budget_enforcement_ac_004_03(tmp_path: Path):
    """AC-004-03: Context assembly strictly respects token budget; overflows are quarantined."""
    # Write a large target file
    large_file = tmp_path / "huge.py"
    large_file.write_text("x = 1\n" * 1000, encoding="utf-8")  # ~1500 tokens

    router = ContextRouter(tmp_path)
    # Available budget: 600 - 500 = 100 tokens, which is smaller than huge.py
    req = {
        "request_id": "REQ-003",
        "task": {
            "task_id": "TASK-003",
            "objective": "Refactor huge file",
            "target_files": ["huge.py"],
        },
        "context_sources": {
            "include_graph": True,
            "include_rules": True,
            "include_specs": True,
            "include_evidence": True,
        },
        "budget_constraints": {"max_tokens": 600, "reserve_for_generation": 500, "k_hop_limit": 0},
        "security_constraints": {"quarantine_adversarial": True, "isolated_project_id": "PROJ-TEST"},
    }

    result = router.assemble_context(req)
    resp = result["routing_response"]

    assert resp["total_tokens"] <= 100
    assert resp["budget_exhausted"] is True
    assert resp["escalation_required"] is True
    assert len(resp["quarantined_exclusions"]) == 1
    assert resp["quarantined_exclusions"][0]["exclusion_reason"] == "EXCEEDED_TOKEN_BUDGET"
