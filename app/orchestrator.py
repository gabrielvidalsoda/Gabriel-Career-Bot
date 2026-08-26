"""Conversation state machine and LLM orchestration."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from openai import AsyncOpenAI

from app.config import get_settings
from app.prompts import build_system_prompt
from app.response_parser import parse_llm_response
from app.storage import ConversationState, Session, SessionStore, StoredMessage
from app.tracks import get_track

logger = logging.getLogger("careerbot.orchestrator")

GENERATE_TRIGGERS = {
    "sim",
    "pode gerar",
    "pode gerar o",
    "gera",
    "gerar",
    "pronto",
    "pode criar",
    "manda ver",
    "ok",
    "yes",
    "go ahead",
    "generate",
}


@dataclass
class OrchestratorResult:
    reply: str
    artifact: str | None
    artifact_filename: str | None
    missing_slots: list[str]


class ConversationOrchestrator:
    def __init__(
        self,
        client: AsyncOpenAI,
        store: SessionStore | None = None,
    ) -> None:
        self.client = client
        self.store = store or SessionStore()

    async def process(
        self,
        session: Session,
        user_message: str,
        track_id: str | None = None,
    ) -> OrchestratorResult:
        if track_id and not session.track_id:
            self._select_track(session, track_id)

        self._advance_state_on_input(session, user_message)

        session.messages.append(StoredMessage(role="user", content=user_message))
        self.store.save(session)

        if self._should_force_deliver(session, user_message):
            session.state = ConversationState.DELIVER

        reply, artifact = await self._call_llm(session)

        parsed = parse_llm_response(reply)
        visible = parsed.visible_text or reply

        if parsed.profile_update:
            session.profile.merge_update(parsed.profile_update)

        if parsed.artifact:
            session.artifact = parsed.artifact
            session.artifact_version += 1
            session.state = ConversationState.REVISE

        if parsed.ready_to_deliver and session.state == ConversationState.COLLECT:
            session.state = ConversationState.DELIVER
            deliver_result = await self._call_llm(session)
            parsed_deliver = parse_llm_response(deliver_result)
            visible = parsed_deliver.visible_text or deliver_result
            if parsed_deliver.artifact:
                session.artifact = parsed_deliver.artifact
                session.artifact_version += 1
                session.state = ConversationState.REVISE
            if parsed_deliver.profile_update:
                session.profile.merge_update(parsed_deliver.profile_update)

        if parsed.done:
            session.state = ConversationState.DONE

        session.messages.append(StoredMessage(role="assistant", content=visible))
        self.store.save(session)

        track = get_track(session.track_id) if session.track_id else None
        missing: list[str] = []
        if track and session.state in (ConversationState.COLLECT, ConversationState.DIAGNOSIS):
            missing = session.profile.missing_slots(list(track.required_slots))

        return OrchestratorResult(
            reply=visible,
            artifact=session.artifact,
            artifact_filename=track.artifact_name if track and session.artifact else None,
            missing_slots=missing,
        )

    def _select_track(self, session: Session, track_id: str) -> None:
        track = get_track(track_id)
        if not track:
            return
        session.track_id = track_id
        session.state = ConversationState.DIAGNOSIS

    def _advance_state_on_input(self, session: Session, user_message: str) -> None:
        if session.state == ConversationState.WELCOME and session.track_id:
            session.state = ConversationState.DIAGNOSIS
        elif session.state == ConversationState.WELCOME:
            lowered = user_message.lower()
            for track in ("improve_cv", "tailor_cv", "interview_prep"):
                labels = {
                    "improve_cv": ("melhorar cv", "melhorar currículo", "melhorar curriculo"),
                    "tailor_cv": ("adaptar cv", "adaptar à vaga", "adaptar a vaga"),
                    "interview_prep": (
                        "entrevista",
                        "preparar entrevista",
                        "rh",
                    ),
                }
                if any(phrase in lowered for phrase in labels.get(track, ())):
                    self._select_track(session, track)
                    break
        elif session.state == ConversationState.DIAGNOSIS:
            session.state = ConversationState.COLLECT
        elif session.state == ConversationState.REVISE:
            accept_words = ("aceito", "está bom", "esta bom", "perfeito", "obrigado", "thanks")
            if any(w in user_message.lower() for w in accept_words):
                session.state = ConversationState.DONE

    def _should_force_deliver(self, session: Session, user_message: str) -> bool:
        if session.state != ConversationState.COLLECT or not session.track_id:
            return False
        track = get_track(session.track_id)
        if not track:
            return False
        missing = session.profile.missing_slots(list(track.required_slots))
        if missing:
            return False
        lowered = user_message.lower().strip()
        return any(trigger in lowered for trigger in GENERATE_TRIGGERS)

    async def _call_llm(self, session: Session) -> tuple[str, str | None]:
        settings = get_settings()
        system = build_system_prompt(session)

        llm_messages: list[dict[str, str]] = [{"role": "system", "content": system}]
        for msg in session.messages[-settings.max_history_messages :]:
            if msg.role in ("user", "assistant"):
                llm_messages.append({"role": msg.role, "content": msg.content})

        kwargs: dict = {
            "model": settings.openai_model,
            "messages": llm_messages,
            "max_completion_tokens": settings.max_output_tokens,
        }
        if settings.temperature is not None:
            kwargs["temperature"] = settings.temperature

        completion = await self.client.chat.completions.create(**kwargs)
        text = completion.choices[0].message.content or ""
        return text, None
