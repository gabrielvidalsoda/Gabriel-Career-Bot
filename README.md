# Gabriel Career Bot

Assistente interativo local para profissionais de tecnologia melhorarem currículo e se prepararem para entrevistas.

## Quick start

```powershell
cd "c:\Users\gabri\OneDrive\Documentos\Gabriel Career Bot"
poetry install
Copy-Item .env.example .env
# Edite .env: OPENAI_API_KEY e, se necessário, KNOWLEDGE_PACK_PATH
poetry run uvicorn app.main:app --reload --port 8080
```

Abra http://127.0.0.1:8080

Health check: http://127.0.0.1:8080/api/health

## O que faz (MVP)

- Chat web com 3 trilhas: **Melhorar CV**, **Adaptar CV à vaga**, **Preparar entrevista RH**
- Coleta guiada de informações do candidato
- Entrega artefato em markdown + download `.md`
- Sessões persistidas em `data/sessions/*.json` (sobrevivem restart do servidor)
- Método carregado do [knowledge-pack](../gabriel-resume-audits/knowledge-pack) via `KNOWLEDGE_PACK_PATH`

## Estrutura

```
app/
  main.py           API FastAPI + static web
  orchestrator.py   máquina de estados + LLM
  tracks.py         definição das trilhas
  knowledge.py      carrega MD por trilha
  storage.py        JSON por sessão (adapter trocável)
  profile.py        fatos do candidato
web/                UI estática
data/               sessões (gitignored)
```

## API

| Endpoint | Descrição |
|----------|-----------|
| `GET /api/health` | Status + knowledge pack |
| `GET /api/bootstrap?session_id=` | Greeting, trilhas, sessão |
| `POST /api/chat` | `{ session_id, message, track_id? }` |
| `GET /api/session/{id}` | Estado da sessão |
| `GET /api/session/{id}/artifact` | Download do entregável |

## Decisões em aberto (pós-MVP)

Detalhes em [docs/DECISIONS.md](docs/DECISIONS.md). Resumo:

### Banco de dados

| Caminho | Quando |
|---------|--------|
| **JSON** (atual) | MVP local, 1 máquina |
| **SQLite** | Histórico pesquisável, retomar sessões em lista |
| **PostgreSQL** | Beta multi-usuário, espelhar produção |

Trocar storage = implementar novo adapter em `storage.py` sem mudar orchestrator.

### Cloud

| Caminho | Quando |
|---------|--------|
| **Adiar** | Validar qualidade das respostas localmente |
| **PaaS** (Railway/Render/Fly) | 2–3 beta testers |
| **AWS** | Produto com auth, PII, escala |

Career Bot precisa de **volume persistente** (diferente do Gabriel Bot portfolio, que é stateless).

### RAG

MVP usa **seleção determinística** de 2–5 arquivos MD por trilha. Migrar para RAG (Chroma/FAISS) se o knowledge-pack crescer muito.

## Teste manual sugerido

1. Escolha "Melhorar CV"
2. Informe cargo-alvo e cole um CV
3. Confirme com "pode gerar"
4. Peça ajuste em um bullet
5. Baixe o `.md`
6. Reinicie o servidor — a sessão deve continuar (mesmo `session_id` no localStorage)
