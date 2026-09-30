"""Event-sourced progress logging and state projection."""

import json
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Any
from eidos.contracts.models import ProgressEventModel
from eidos.intelligence.fingerprint import get_git_info

class ProgressLogger:
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.progress_dir = workspace_root / ".eidos" / "progress"
        self.events_file = self.progress_dir / "events.jsonl"
        self.state_file = self.progress_dir / "state.json"
        self.progress_dir.mkdir(parents=True, exist_ok=True)

    def log_event(self, event_type: str, session_id: str = "SESSION-DEFAULT", task_id: str | None = None, payload: dict[str, Any] | None = None) -> ProgressEventModel:
        """Appends an event to the immutable progress stream."""
        git_info = get_git_info(self.workspace_root)
        event = ProgressEventModel(
            event_id=f"EVT-{uuid.uuid4().hex[:8].upper()}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            session_id=session_id,
            task_id=task_id,
            event_type=event_type,
            payload=payload or {},
            git_commit=git_info.get("head") or "HEAD",
        )
        
        with open(self.events_file, "a", encoding="utf-8") as f:
            f.write(event.model_dump_json() + "\n")
            
        self._update_state(event)
        return event

    def _update_state(self, last_event: ProgressEventModel):
        """Materializes the active project progress state."""
        state = {
            "last_event_id": last_event.event_id,
            "last_event_type": last_event.event_type,
            "last_updated": last_event.timestamp,
            "git_commit": last_event.git_commit,
        }
        self.state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")
