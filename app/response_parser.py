"""Response parsing helpers for LLM sentinel blocks."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass

from app.prompts import (
    ARTIFACT_SENTINEL_END,
    ARTIFACT_SENTINEL_START,
    PROFILE_SENTINEL_END,
    PROFILE_SENTINEL_START,
    READY_SENTINEL,
)

logger = logging.getLogger("careerbot.orchestrator")

DONE_SENTINEL = "[[DONE]]"


@dataclass
class ParsedResponse:
    visible_text: str
    profile_update: dict | None
    artifact: str | None
    ready_to_deliver: bool
    done: bool


def _extract_block(text: str, start: str, end: str) -> tuple[str, str | None]:
    """Remove block from text and return (cleaned_text, block_content)."""
    pattern = re.escape(start) + r"(.*?)" + re.escape(end)
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        return text, None
    content = match.group(1).strip()
    cleaned = text[: match.start()] + text[match.end() :]
    return cleaned.strip(), content


def parse_llm_response(raw: str) -> ParsedResponse:
    text = raw
    artifact: str | None = None
    profile_update: dict | None = None

    text, artifact = _extract_block(text, ARTIFACT_SENTINEL_START, ARTIFACT_SENTINEL_END)
    text, profile_raw = _extract_block(text, PROFILE_SENTINEL_START, PROFILE_SENTINEL_END)

    if profile_raw:
        try:
            profile_update = json.loads(profile_raw)
        except json.JSONDecodeError:
            logger.warning("Invalid profile JSON from model: %s", profile_raw[:200])

    ready = READY_SENTINEL in text
    text = text.replace(READY_SENTINEL, "").strip()

    done = DONE_SENTINEL in text
    text = text.replace(DONE_SENTINEL, "").strip()

    return ParsedResponse(
        visible_text=text.strip(),
        profile_update=profile_update,
        artifact=artifact,
        ready_to_deliver=ready,
        done=done,
    )
