"""Loads knowledge-pack markdown files by track."""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

from app.config import get_settings
from app.tracks import Track

logger = logging.getLogger("careerbot.knowledge")


class KnowledgeError(RuntimeError):
    pass


def _pack_root() -> Path:
    root = get_settings().knowledge_pack_dir
    if not root.is_dir():
        raise KnowledgeError(
            f"Knowledge pack not found at {root}. "
            "Set KNOWLEDGE_PACK_PATH in .env to the knowledge-pack folder."
        )
    return root


def load_file(relative_path: str) -> str:
    path = _pack_root() / relative_path
    if not path.is_file():
        raise KnowledgeError(f"Missing knowledge file: {relative_path}")
    return path.read_text(encoding="utf-8").strip()


def load_for_track(track: Track) -> dict[str, str]:
    """Load all knowledge files for a track. Missing files are logged, not fatal."""
    pack: dict[str, str] = {}
    for name in track.knowledge_files:
        try:
            pack[name] = load_file(name)
        except KnowledgeError as exc:
            logger.warning("%s", exc)
    return pack


def load_core_rules() -> str:
    """Base career-agent rules used before a track is selected."""
    try:
        return load_file("CAREER-AGENT-KNOWLEDGE-BASE.md")
    except KnowledgeError:
        return (
            "Never invent employers, dates, metrics, or tools. "
            "Ask the user when facts are missing."
        )


@lru_cache
def list_available_files() -> tuple[str, ...]:
    root = _pack_root()
    files: list[str] = []
    for path in sorted(root.rglob("*.md")):
        files.append(str(path.relative_to(root)).replace("\\", "/"))
    return tuple(files)


def approx_tokens(text: str) -> int:
    return len(text) // 4
