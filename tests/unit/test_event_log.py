"""Unit tests for SPEC-007: Append-Only Progress Logger & Git HEAD Anchoring."""

import json
from pathlib import Path
from eidos.progress.logger import ProgressLogger


def test_append_only_immutability_ac_007_01(tmp_path: Path):
    """AC-007-01: Logging an event increases file length by 1 line without altering past lines."""
    logger = ProgressLogger(tmp_path)
    
    # Pre-populate with 10 events
    for i in range(10):
        logger.log_event("SESSION_UPDATED", payload={"step": i}, commit_override="commit001")
        
    initial_content = logger.events_file.read_text(encoding="utf-8")
    initial_lines = initial_content.splitlines()
    assert len(initial_lines) == 10
    
    # Append 1 new event
    logger.log_event("TOOL_INVOKED", payload={"tool": "pytest"}, commit_override="commit002")
    
    new_content = logger.events_file.read_text(encoding="utf-8")
    new_lines = new_content.splitlines()
    
    assert len(new_lines) == 11
    # Prior 10 lines must be byte-identical
    assert new_lines[:10] == initial_lines


def test_git_head_anchoring_ac_007_02(tmp_path: Path):
    """AC-007-02: Logged event records exact Git commit hash."""
    logger = ProgressLogger(tmp_path)
    target_sha = "abc123456789"
    
    event = logger.log_event(
        "TASK_INITIALIZED",
        task_id="TASK-001",
        payload={"spec_id": "SPEC-001"},
        commit_override=target_sha,
    )
    
    assert event["git_commit"] == target_sha
    
    # Read back from stream
    events = logger.get_events()
    assert len(events) == 1
    assert events[0]["git_commit"] == target_sha


def test_superseding_correction(tmp_path: Path):
    """Superseding correction appends a new event referencing the target event without deleting history."""
    logger = ProgressLogger(tmp_path)
    evt1 = logger.log_event("SESSION_UPDATED", payload={"wrong_val": True}, commit_override="c1")
    
    corr = logger.log_superseding_correction(
        target_event_id=evt1["event_id"],
        reason="Erroneous flag set",
        corrected_payload={"wrong_val": False},
    )
    
    events = logger.get_events()
    assert len(events) == 2
    assert events[1]["event_type"] == "SUPERSEDING_CORRECTION"
    assert events[1]["payload"]["supersedes_event_id"] == evt1["event_id"]
    # Original event still exists byte-intact
    assert events[0]["payload"]["wrong_val"] is True
