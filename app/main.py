"""Gabriel Career Bot API."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from openai import APIError, AsyncOpenAI

from app.config import ROOT, get_settings
from app.knowledge import KnowledgeError, list_available_files
from app.orchestrator import ConversationOrchestrator
from app.ratelimit import RateLimiter, TokenBudget
from app.schemas import (
    BootstrapResponse,
    ChatRequest,
    ChatResponse,
    HealthResponse,
    SessionResponse,
    TrackInfo,
)
from app.storage import SessionStore
from app.tracks import list_tracks

logger = logging.getLogger("careerbot")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

WEB_DIR = ROOT / "web"

GREETING = (
    "Olá! Sou o Gabriel Career Bot — assistente para profissionais de tecnologia "
    "que querem melhorar currículo ou se preparar para entrevistas.\n\n"
    "Escolha uma trilha abaixo ou me diga o que você precisa."
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.store = SessionStore()
    app.state.client = (
        AsyncOpenAI(api_key=settings.openai_api_key)
        if settings.openai_api_key
        else None
    )
    app.state.limiter = RateLimiter(
        settings.rate_limit_requests, settings.rate_limit_window_seconds
    )
    app.state.budget = TokenBudget(settings.daily_token_budget)

    try:
        file_count = len(list_available_files())
        logger.info(
            "Knowledge pack at %s (%d files), model=%s",
            settings.knowledge_pack_dir,
            file_count,
            settings.openai_model,
        )
    except KnowledgeError as exc:
        logger.warning("%s", exc)
        file_count = 0

    app.state.knowledge_files_count = file_count

    if not settings.openai_api_key:
        logger.warning("OPENAI_API_KEY is not set. /api/chat will return 503.")

    yield


app = FastAPI(
    title="Gabriel Career Bot",
    version="0.1.0",
    lifespan=lifespan,
)

_settings = get_settings()
if _settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )


def client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def guard(request: Request) -> None:
    if app.state.client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OPENAI_API_KEY is not set. Add it to .env and restart.",
        )
    allowed, retry_after = app.state.limiter.check(client_key(request))
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many messages. Wait a moment and try again.",
            headers={"Retry-After": str(retry_after)},
        )
    if not app.state.budget.has_capacity():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Daily token budget reached. Try again tomorrow.",
        )


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    try:
        file_count = len(list_available_files())
    except KnowledgeError:
        file_count = 0
    return HealthResponse(
        status="ok",
        model=settings.openai_model,
        knowledge_pack_path=str(settings.knowledge_pack_dir),
        knowledge_files_count=file_count,
        openai_key_configured=bool(settings.openai_api_key),
        data_dir=str(settings.data_path),
    )


@app.get("/api/bootstrap", response_model=BootstrapResponse)
async def bootstrap(
    session_id: str | None = Query(default=None),
) -> BootstrapResponse:
    settings = get_settings()
    store: SessionStore = app.state.store
    session = store.get_or_create(session_id)

    return BootstrapResponse(
        greeting=GREETING,
        tracks=[
            TrackInfo(id=t.id, label=t.label, description=t.description)
            for t in list_tracks()
        ],
        session_id=session.id,
        state=session.state.value,
        max_message_chars=settings.max_message_chars,
    )


@app.get("/api/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str) -> SessionResponse:
    store: SessionStore = app.state.store
    session = store.load(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionResponse(
        session_id=session.id,
        state=session.state.value,
        track_id=session.track_id,
        message_count=len(session.messages),
        has_artifact=bool(session.artifact),
        profile=session.profile.model_dump(exclude_defaults=True),
    )


@app.get("/api/session/{session_id}/artifact")
async def download_artifact(session_id: str) -> PlainTextResponse:
    store: SessionStore = app.state.store
    session = store.load(session_id)
    if not session or not session.artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    from app.tracks import get_track

    track = get_track(session.track_id) if session.track_id else None
    filename = track.artifact_name if track else "artifact.md"

    return PlainTextResponse(
        content=session.artifact,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    guard(request)
    store: SessionStore = app.state.store
    session = store.load(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    orchestrator = ConversationOrchestrator(app.state.client, store)

    try:
        result = await orchestrator.process(
            session,
            payload.message,
            track_id=payload.track_id,
        )
    except APIError as exc:
        logger.error("OpenAI error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Model call failed. Try again in a moment.",
        ) from exc

    reloaded = store.load(payload.session_id)
    state = reloaded.state.value if reloaded else session.state.value
    track_id = reloaded.track_id if reloaded else session.track_id

    return ChatResponse(
        reply=result.reply,
        session_id=payload.session_id,
        state=state,
        track_id=track_id,
        artifact=result.artifact,
        artifact_filename=result.artifact_filename,
        missing_slots=result.missing_slots,
    )


if WEB_DIR.is_dir():
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
