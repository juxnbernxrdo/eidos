"""Append-only progress event logging and Git HEAD anchoring.

Implements SPEC-007 (Append-Only Progress Logger & Git HEAD Anchoring) and satisfies
REQ-EVT-001, REQ-EVT-002, AC-007-01, AC-007-02:
    - Immutable JSONL append
    - Process-safe atomic write using fcntl.flock
    - Automatic Git HEAD commit anchoring
    - Superseding corrections without modifying historical entries
"""

import fcntl
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from eidos.core.exceptions import InvalidInputError, ResourceUnavailableError
from eidos.intelligence.fingerprint import get_git_info


class ProgressLogger:
    """Manages append-only persistence of the Eidos event stream."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.progress_dir = workspace_root / ".eidos" / "progress"
        self.events_file = self.progress_dir / "events.jsonl"
        self.state_file = self.progress_dir / "state.json"
        
        try:
            self.progress_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ResourceUnavailableError(f"Cannot initialize progress directory: {e}")

    def log_event(
        self,
        event_type: str,
        session_id: str = "SESSION-DEFAULT",
        task_id: str | None = None,
        actor_type: str = "SYSTEM",
        actor_id: str = "eidos-core",
        payload: dict[str, Any] | None = None,
        commit_override: str | None = None,
    ) -> dict[str, Any]:
        """Appends an event atomically to the immutable progress stream.

        Returns:
            The normalized persisted event dictionary.
        """
        git_commit = commit_override
        if not git_commit:
            git_info = get_git_info(self.workspace_root)
            git_commit = git_info.get("head") or "HEAD"

        event = {
            "event_id": f"EVT-{uuid.uuid4().hex[:12].upper()}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "task_id": task_id,
            "event_type": event_type,
            "actor": {
                "type": actor_type,
                "id": actor_id,
            },
            "payload": payload or {},
            "git_commit": git_commit,
        }

        event_line = json.dumps(event, separators=(",", ":"), default=str) + "\n"

        try:
            with open(self.events_file, "a", encoding="utf-8") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    f.write(event_line)
                    f.flush()
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except OSError as e:
            raise ResourceUnavailableError(f"Failed to append to event log: {e}")

        self._update_state(event)
        return event

    def log_superseding_correction(
        self,
        target_event_id: str,
        reason: str,
        corrected_payload: dict[str, Any] | None = None,
        session_id: str = "SESSION-DEFAULT",
        actor_id: str = "eidos-operator",
    ) -> dict[str, Any]:
        """Logs a superseding correction for an earlier event without mutating history."""
        if not target_event_id:
            raise InvalidInputError("Target event ID must be specified for correction")

        payload = {
            "supersedes_event_id": target_event_id,
            "reason": reason,
            "corrected_payload": corrected_payload or {},
        }
        return self.log_event(
            event_type="SUPERSEDING_CORRECTION",
            session_id=session_id,
            actor_type="HUMAN",
            actor_id=actor_id,
            payload=payload,
        )

    def stream_events(self) -> Iterator[dict[str, Any]]:
        """Yields events from the log sequentially."""
        if not self.events_file.exists():
            return

        with open(self.events_file, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                clean = line.strip()
                if not clean:
                    continue
                try:
                    yield json.loads(clean)
                except json.JSONDecodeError as err:
                    # Report provenance failure on corrupted line
                    raise InvalidInputError(f"Corrupted event line at line {line_no}: {err}")

    def get_events(self) -> list[dict[str, Any]]:
        """Returns all events as a list."""
        return list(self.stream_events())

    def _update_state(self, last_event: dict[str, Any]) -> None:
        """Materializes the lightweight pointer state for quick status lookups."""
        state = {
            "last_event_id": last_event["event_id"],
            "last_event_type": last_event["event_type"],
            "last_updated": last_event["timestamp"],
            "git_commit": last_event["git_commit"],
        }
        try:
            self.state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")
        except OSError:
            pass
