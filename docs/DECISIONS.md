# Decisões técnicas em aberto — Gabriel Career Bot

Registro das opções documentadas no plano MVP. **Decisão atual:** permanecer local com JSON até validação manual.

## Banco de dados

| Opção | Status | Quando migrar |
|-------|--------|---------------|
| **JSON por sessão** | **Ativo (MVP)** | — |
| SQLite | Candidato v2 | Listar/retomar sessões, queries simples |
| PostgreSQL (Docker/RDS) | Futuro | Beta multi-usuário, produção |

**Adapter:** `app/storage.py` — implementar `SessionStore` alternativo sem alterar `orchestrator.py`.

## Cloud / deploy

| Opção | Status | Quando |
|-------|--------|--------|
| **Local only** | **Ativo (MVP)** | — |
| PaaS (Railway, Render, Fly.io) | Candidato beta | 2–3 testers externos |
| AWS (ECS/Beanstalk + RDS) | Futuro | Auth, PII, escala, compliance |

**Nota:** diferente do Gabriel Bot (stateless), Career Bot exige volume persistente para perfis e sessões.

## RAG / knowledge

| Opção | Status | Quando |
|-------|--------|--------|
| **Seleção determinística por trilha** | **Ativo (MVP)** | — |
| RAG (Chroma/FAISS) | Candidato v2 | Pack crescer além do context window |
| Tool-use / file router | Candidato v2 | Muitas trilhas dinâmicas |

## Auth / PII

| Opção | Status |
|-------|--------|
| Sem login, session_id em localStorage | **Ativo (MVP)** |
| Magic link / OAuth | Futuro (pré-deploy público) |

**Recomendação:** validar qualidade das respostas localmente → PaaS com beta fechado → AWS após BRD de registro.
