"""Conversation track definitions for the MVP."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Track:
    id: str
    label: str
    description: str
    knowledge_files: tuple[str, ...]
    required_slots: tuple[str, ...]
    artifact_name: str
    artifact_hint: str


TRACKS: dict[str, Track] = {
    "improve_cv": Track(
        id="improve_cv",
        label="Melhorar CV",
        description="Reescrever e estruturar seu currículo com bullets de impacto.",
        knowledge_files=(
            "CAREER-AGENT-KNOWLEDGE-BASE.md",
            "essentials.md",
            "prepare-resume/checklist.md",
            "prepare-resume/blank-model.md",
        ),
        required_slots=("current_cv", "target_role"),
        artifact_name="cv-melhorado.md",
        artifact_hint="Currículo completo em markdown seguindo o modelo da trilha.",
    ),
    "tailor_cv": Track(
        id="tailor_cv",
        label="Adaptar CV à vaga",
        description="Ajustar seu currículo para uma descrição de vaga específica.",
        knowledge_files=(
            "CAREER-AGENT-KNOWLEDGE-BASE.md",
            "essentials.md",
            "apply-to-jobs/how-to-tailor-resume.md",
            "prepare-resume/checklist.md",
            "prepare-resume/blank-model.md",
        ),
        required_slots=("current_cv", "target_role", "job_description"),
        artifact_name="cv-adaptado.md",
        artifact_hint="Versão do CV adaptada à vaga, mesma carreira, novo enquadramento.",
    ),
    "interview_prep": Track(
        id="interview_prep",
        label="Preparar entrevista RH",
        description="Roteiro de respostas comportamentais e perguntas para fazer.",
        knowledge_files=(
            "CAREER-AGENT-KNOWLEDGE-BASE.md",
            "essentials.md",
            "prepare-interview/checklist.md",
            "prepare-interview/questions-to-ask.md",
            "prepare-interview/case-framework.md",
        ),
        required_slots=("target_role",),
        artifact_name="roteiro-entrevista.md",
        artifact_hint="Roteiro STAR + perguntas para o entrevistador.",
    ),
}


def list_tracks() -> list[Track]:
    return list(TRACKS.values())


def get_track(track_id: str) -> Track | None:
    return TRACKS.get(track_id)
