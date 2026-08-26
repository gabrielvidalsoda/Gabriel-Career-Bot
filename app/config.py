"""Application settings loaded from environment or a local .env file."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    max_output_tokens: int = 2000
    temperature: float | None = 0.4

    knowledge_pack_path: str = "../gabriel-resume-audits/knowledge-pack"
    data_dir: str = "data"

    max_message_chars: int = 8000
    max_history_messages: int = 40
    rate_limit_requests: int = 30
    rate_limit_window_seconds: int = 300
    daily_token_budget: int = 500_000

    cors_origins_raw: str = Field(default="", validation_alias="CORS_ORIGINS")

    @property
    def cors_origins(self) -> list[str]:
        if not self.cors_origins_raw.strip():
            return []
        return [
            item.strip()
            for item in self.cors_origins_raw.split(",")
            if item.strip()
        ]

    @field_validator("temperature", mode="before")
    @classmethod
    def _blank_to_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @property
    def knowledge_pack_dir(self) -> Path:
        path = Path(self.knowledge_pack_path)
        if not path.is_absolute():
            path = ROOT / path
        return path.resolve()

    @property
    def data_path(self) -> Path:
        path = Path(self.data_dir)
        if not path.is_absolute():
            path = ROOT / path
        return path.resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()
