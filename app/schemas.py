"""Request and response models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.config import get_settings


class TrackInfo(BaseModel):
    id: str
    label: str
    description: str


class BootstrapResponse(BaseModel):
    greeting: str
    tracks: list[TrackInfo]
    session_id: str
    state: str
    max_message_chars: int


class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(min_length=1)
    track_id: str | None = None

    @field_validator("message")
    @classmethod
    def _check_length(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("message cannot be blank")
        limit = get_settings().max_message_chars
        if len(stripped) > limit:
            raise ValueError(f"message exceeds {limit} characters")
        return stripped


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    state: str
    track_id: str | None = None
    artifact: str | None = None
    artifact_filename: str | None = None
    missing_slots: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    model: str
    knowledge_pack_path: str
    knowledge_files_count: int
    openai_key_configured: bool
    data_dir: str


class SessionResponse(BaseModel):
    session_id: str
    state: str
    track_id: str | None
    message_count: int
    has_artifact: bool
    profile: dict
