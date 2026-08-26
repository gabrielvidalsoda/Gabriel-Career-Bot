"""JSON file storage for sessions — swappable adapter for future SQLite/Postgres."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

from app.config import get_settings
from app.profile import CandidateProfile

logger = logging.getLogger("careerbot.storage")


class ConversationState(StrEnum):
    WELCOME = "welcome"
    DIAGNOSIS = "diagnosis"
    COLLECT = "collect"
    DELIVER = "deliver"
    REVISE = "revise"
    DONE = "done"


class StoredMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    state: ConversationState = ConversationState.WELCOME
    track_id: str | None = None
    profile: CandidateProfile = Field(default_factory=CandidateProfile)
    messages: list[StoredMessage] = Field(default_factory=list)
    artifact: str | None = None
    artifact_version: int = 0
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def touch(self) -> None:
        self.updated_at = datetime.now(UTC).isoformat()


class SessionStore:
    """Persists one JSON file per session under DATA_DIR/sessions/."""

    def __init__(self, base_dir: Path | None = None) -> None:
        settings = get_settings()
        root = base_dir or settings.data_path
        self.sessions_dir = root / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, session_id: str) -> Path:
        safe = session_id.replace("/", "").replace("\\", "")
        return self.sessions_dir / f"{safe}.json"

    def create(self) -> Session:
        session = Session()
        self.save(session)
        return session

    def load(self, session_id: str) -> Session | None:
        path = self._path(session_id)
        if not path.is_file():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return Session.model_validate(data)

    def save(self, session: Session) -> None:
        session.touch()
        path = self._path(session.id)
        path.write_text(
            session.model_dump_json(indent=2),
            encoding="utf-8",
        )

    def get_or_create(self, session_id: str | None) -> Session:
        if session_id:
            existing = self.load(session_id)
            if existing:
                return existing
        return self.create()
