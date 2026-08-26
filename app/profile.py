"""Candidate profile collected during a conversation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ExperienceEntry(BaseModel):
    company: str = ""
    title: str = ""
    start: str = ""
    end: str = ""
    bullets: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    """Structured facts gathered from the user — never invent beyond this."""

    name: str = ""
    target_role: str = ""
    seniority: str = ""
    language: str = "pt"
    location: str = ""
    current_cv: str = ""
    job_description: str = ""
    summary: str = ""
    education: list[str] = Field(default_factory=list)
    experience: list[ExperienceEntry] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    extra_notes: str = ""
    raw_facts: dict[str, Any] = Field(default_factory=dict)

    def filled_slots(self, slots: list[str]) -> list[str]:
        """Return slot names that have non-empty values."""
        filled: list[str] = []
        for slot in slots:
            value = getattr(self, slot, None)
            if value is None:
                continue
            if isinstance(value, str) and value.strip():
                filled.append(slot)
            elif isinstance(value, list) and value:
                filled.append(slot)
        return filled

    def missing_slots(self, slots: list[str]) -> list[str]:
        return [s for s in slots if s not in self.filled_slots(slots)]

    def merge_update(self, data: dict[str, Any]) -> None:
        """Merge a partial update dict into the profile."""
        for key, value in data.items():
            if value is None or value == "" or value == []:
                continue
            if key == "experience" and isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        entry = ExperienceEntry.model_validate(item)
                        if entry.company or entry.title:
                            self.experience.append(entry)
                    elif isinstance(item, ExperienceEntry):
                        self.experience.append(item)
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                self.raw_facts[key] = value
