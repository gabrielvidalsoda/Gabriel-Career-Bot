const SESSION_KEY = "careerbot_session_id";

const messagesEl = document.getElementById("messages");
const tracksEl = document.getElementById("tracks");
const formEl = document.getElementById("chat-form");
const inputEl = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const artifactPanel = document.getElementById("artifact-panel");
const artifactContent = document.getElementById("artifact-content");
const downloadBtn = document.getElementById("download-btn");
const sessionInfo = document.getElementById("session-info");
const stateInfo = document.getElementById("state-info");
const mainEl = document.querySelector(".main");

let sessionId = localStorage.getItem(SESSION_KEY);
let artifactFilename = "artifact.md";

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setLoading(loading) {
  sendBtn.disabled = loading;
  inputEl.disabled = loading;
}

function renderTracks(tracks) {
  tracksEl.innerHTML = "";
  tracks.forEach((track) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "track-chip";
    btn.textContent = track.label;
    btn.title = track.description;
    btn.addEventListener("click", () => selectTrack(track));
    tracksEl.appendChild(btn);
  });
}

async function bootstrap() {
  const params = sessionId ? `?session_id=${encodeURIComponent(sessionId)}` : "";
  const res = await fetch(`/api/bootstrap${params}`);
  if (!res.ok) throw new Error("Bootstrap failed");
  const data = await res.json();

  sessionId = data.session_id;
  localStorage.setItem(SESSION_KEY, sessionId);
  sessionInfo.textContent = `Sessão: ${sessionId.slice(0, 8)}…`;
  stateInfo.textContent = `Estado: ${data.state}`;

  appendMessage("assistant", data.greeting);
  renderTracks(data.tracks);
  inputEl.maxLength = data.max_message_chars;
}

async function selectTrack(track) {
  const message = `Quero seguir a trilha: ${track.label}`;
  appendMessage("user", message);
  await sendChat(message, track.id);
}

async function sendChat(message, trackId = null) {
  setLoading(true);
  const typing = document.createElement("div");
  typing.className = "message assistant typing";
  typing.textContent = "Pensando…";
  messagesEl.appendChild(typing);

  try {
    const body = { session_id: sessionId, message };
    if (trackId) body.track_id = trackId;

    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    typing.remove();

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      appendMessage("assistant", err.detail || "Erro ao enviar mensagem.");
      return;
    }

    const data = await res.json();
    sessionId = data.session_id;
    localStorage.setItem(SESSION_KEY, sessionId);
    stateInfo.textContent = `Estado: ${data.state}`;

    appendMessage("assistant", data.reply);

    if (data.artifact) {
      artifactContent.textContent = data.artifact;
      artifactPanel.hidden = false;
      mainEl.classList.add("has-artifact");
      if (data.artifact_filename) {
        artifactFilename = data.artifact_filename;
      }
    }
  } catch (err) {
    typing.remove();
    appendMessage("assistant", "Falha de conexão. O servidor está rodando?");
    console.error(err);
  } finally {
    setLoading(false);
  }
}

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = inputEl.value.trim();
  if (!message) return;
  inputEl.value = "";
  appendMessage("user", message);
  await sendChat(message);
});

downloadBtn.addEventListener("click", () => {
  if (!sessionId) return;
  window.open(`/api/session/${sessionId}/artifact`, "_blank");
});

bootstrap().catch((err) => {
  appendMessage("assistant", "Não foi possível iniciar. Verifique se o servidor está no ar.");
  console.error(err);
});
