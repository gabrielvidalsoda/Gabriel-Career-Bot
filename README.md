# Gabriel Career Bot

Assistente interativo local para profissionais de tecnologia melhorarem currÃ­culo e se prepararem para entrevistas.

## Quick start

```powershell
cd Gabriel-Career-Bot
poetry install
Copy-Item .env.example .env
# Edite .env: OPENAI_API_KEY e, se necessÃ¡rio, KNOWLEDGE_PACK_PATH
poetry run uvicorn app.main:app --reload --port 8080
```

Abra http://127.0.0.1:8080

Health check: http://127.0.0.1:8080/api/health

## O que faz (MVP)

- Chat web com 3 trilhas: **Melhorar CV**, **Adaptar CV Ã  vaga**, **Preparar entrevista RH**
- Coleta guiada de informaÃ§Ãµes do candidato
- Entrega artefato em markdown + download `.md`
- SessÃµes persistidas em `data/sessions/*.json` (sobrevivem restart do servidor)
- MÃ©todo carregado do [knowledge-pack](../gabriel-resume-audits/knowledge-pack) via `KNOWLEDGE_PACK_PATH`

## Estrutura

```
app/
  main.py           API FastAPI + static web
  orchestrator.py   mÃ¡quina de estados + LLM
  tracks.py         definiÃ§Ã£o das trilhas
  knowledge.py      carrega MD por trilha
  storage.py        JSON por sessÃ£o (adapter trocÃ¡vel)
  profile.py        fatos do candidato
web/                UI estÃ¡tica
data/               sessÃµes (gitignored)
```

## API

| Endpoint | DescriÃ§Ã£o |
|----------|-----------|
| `GET /api/health` | Status + knowledge pack |
| `GET /api/bootstrap?session_id=` | Greeting, trilhas, sessÃ£o |
| `POST /api/chat` | `{ session_id, message, track_id? }` |
| `GET /api/session/{id}` | Estado da sessÃ£o |
| `GET /api/session/{id}/artifact` | Download do entregÃ¡vel |

## DecisÃµes em aberto (pÃ³s-MVP)

Detalhes em [docs/DECISIONS.md](docs/DECISIONS.md). Resumo:

### Banco de dados

| Caminho | Quando |
|---------|--------|
| **JSON** (atual) | MVP local, 1 mÃ¡quina |
| **SQLite** | HistÃ³rico pesquisÃ¡vel, retomar sessÃµes em lista |
| **PostgreSQL** | Beta multi-usuÃ¡rio, espelhar produÃ§Ã£o |

Trocar storage = implementar novo adapter em `storage.py` sem mudar orchestrator.

### Cloud

| Caminho | Quando |
|---------|--------|
| **Adiar** | Validar qualidade das respostas localmente |
| **PaaS** (Railway/Render/Fly) | 2â€“3 beta testers |
| **AWS** | Produto com auth, PII, escala |

Career Bot precisa de **volume persistente** (diferente do Gabriel Bot portfolio, que Ã© stateless).

### RAG

MVP usa **seleÃ§Ã£o determinÃ­stica** de 2â€“5 arquivos MD por trilha. Migrar para RAG (Chroma/FAISS) se o knowledge-pack crescer muito.

## Teste manual sugerido

1. Escolha "Melhorar CV"
2. Informe cargo-alvo e cole um CV
3. Confirme com "pode gerar"
4. PeÃ§a ajuste em um bullet
5. Baixe o `.md`
6. Reinicie o servidor â€” a sessÃ£o deve continuar (mesmo `session_id` no localStorage)

