# Checklist de ideia inicial de produto

**Para que serve:** narrar requisitos e ideias o suficiente para *ver* como o produto pode funcionar e gerar perguntas para um solution design (conexões, integrações, tecnologias).  
**Para que não serve:** fechar arquitetura, contratos de API, stack, estimativas ou todas as regras de negócio. Isso vem depois, no BRD e no solution design.


| Campo                                | Preencher                     |
| ------------------------------------ | ----------------------------- |
| Nome provisório do produto / feature | Gabriel Career Bot            |
| Autor                                | Gabriel                       |
| Data                                 | Today                         |
| Status                               | Rascunho de ideia (não é BRD) |
| BRD relacionado (quando existir)     |                               |


---

## Como usar

Preencha em prosa, como se estivesse explicando o produto a alguém que vai desenhá-lo. Marque o item quando a resposta estiver *boa o bastante para gerar perguntas*, não quando estiver completa.

- **Obrigatório** = sem isso o solution design ainda não consegue visualizar o produto.
- **Opcional nesta fase** = útil, mas pode ficar como pergunta aberta.
- Itens com *“pergunta para o SD”* não pedem decisão: pedem que a dúvida fique explícita, com dono se você já souber.

Este checklist alimenta, nesta ordem:

1. **BRD** — o quê, por quê, para quem, o que entra / sai de escopo.
2. **Solution design** — como os sistemas se conectam, de onde vêm os dados, o que acontece quando algo falha, quais tecnologias *podem* servir.
3. **Contrato de dados / mapping** — só depois que as perguntas de integração tiverem forma.

Modelo de referência interno: `AM/BRD/BRD_template.md`, BRDs de Account Analyzer, Project Status Tracker e Carrier Allocation.

---



## 0. Identidade da ideia

Obrigatório.

- [ ] Consigo nomear o produto ou a feature em uma frase.
- [ ] Sei se isto é **produto novo**, **feature em produto existente**, ou **integração entre sistemas que já existem**.
- [ ] Sei o contexto de uso: ferramenta interna, experiência para um usuário de campo, serviço de backend, assistente/IA, relatório, etc.

**Narrativa (2–4 frases):** o que é isto, em linguagem de negócio.

> Exemplo de padrão (Account Analyzer): “Dar ao Account Manager, no assistente, o mesmo perfil de líder que hoje só existe no Workspace, para ele não sair da análise para buscar contexto.”

```
Dar aos profissionais da área de tecnologia um assistente interativo para construção de currículo e preparação para buscar novas vagas. Consolida base de conhecimento de várias consultorias de carreira e experiência prática de desenvolvedores. Problema que soluciona: dificuldade de aplicar melhorias e fazer grandes mudanças para sua carreira.
```

**Perguntas que isto já gera para o solution design**

- [x] Isto vive *dentro* de um produto existente ou é uma superfície nova? Nova
- [x] Há um sistema de registro hoje, ou o registro ainda vai nascer? Registro vai nascer

---



## 1. Problema, pessoa e valor

Obrigatório. Equivale à seção *Use Case (Goal)* do template de BRD.

Escreva como história, não como slogan. Evite tautologia do tipo “o problema é não ter a feature”.

- [ ] **Persona(s):** quem usa, no papel real (não “o usuário”). Pode haver mais de uma, com objetivos diferentes.
- [ ] **Momento:** quando esta pessoa sente a dor (antes de uma call, no download do pedido, depois da reunião de status…).
- [ ] **Problema:** o que ela faz hoje que é lento, inconsistente, arriscado ou invisível.
- [ ] **Objetivo:** o que ela consegue concluir de ponta a ponta se isto existir.
- [ ] **Valor para o negócio:** decisão melhor, menos retrabalho, governança, receita, retenção, compliance — seja específico o bastante para ser discutido.

```
Persona(s): jovem brasileiro da área de tecnologia
Momento: busca novas oportunidades. pesquisa no google vagas e dicas de carreira
Problema hoje: fica sobrecarregado de conteúdos e ações para melhorar seu currículo
Objetivo da pessoa: ser aprovado em uma nova vaga
Valor para o negócio: retorno financeiro e aumento salarial
```

**Perguntas para o solution design**

- [ ] A persona tem papéis / mercados / permissões diferentes que mudam o que ela pode ver? Não
- [ ] O valor depende de velocidade, de fidelidade dos dados, ou dos dois? Fidelidade dos dados

---



## 2. Como a pessoa pede ou dispara isto

Obrigatório. Equivale a *Example Inputs / User Engagement*.

Mesmo que o produto não seja conversacional: descreva o gatilho (botão, upload, job, evento de outro sistema, prompt).

- [ ] Há **2–5 exemplos concretos** de como a pessoa começa (frase, clique, arquivo, evento).
- [ ] Há pelo menos **uma variação** (outro papel, outro mercado, outro jeito de pedir).
- [ ] Está claro o que acontece **depois da primeira resposta** (seguir, editar, confirmar, abandonar).

```
Gatilho principal: Acessa curso, comunidade, workshop ou similares de carreira e está no momento de aplicar o conhecimento aprendido
Outras formas de começar: Sabe que precisa melhorar o cv mas não sabe como
O que a pessoa faz em seguida: Busca ajuda de amigos, professores, mentores e influencers
```

> Padrão visto nos BRDs de AA: “Show me the profile of `[affiliate]-[abo]`” + follow-up por chip ou sim/não.  
> Padrão visto no Status Tracker: o tech lead *sobe* a transcrição da reunião no projeto certo.  
> Padrão visto no Carrier Allocation: o WMS *chama* o serviço no download do pedido.

**Perguntas para o solution design**

- [ ] O gatilho é humano, sistêmico, ou os dois?
- [ ] O contexto (entidade, mercado, arquivo, página de origem) precisa ser *passado* de um sistema para outro? Como?

---



## 3. Como um especialista faria isso hoje, sem o produto

Obrigatório. Equivale a *Manual Process*. É o que mais ajuda a visualizar o produto.

Se a resposta for “N/A”, o solution design ainda não tem chão. Mesmo um fluxo novo tem um equivalente manual (planilha, reunião, e-mail, tela em outro sistema).

- [ ] **Passos ordenados** do gatilho até o entregável.
- [ ] **Fontes consultadas:** sistemas, relatórios, documentos, pessoas.
- [ ] **Regras que a pessoa aplica de cabeça** (limites, prioridade, “se X então Y”).
- [ ] **O que ela faz quando falta dado**, o dado está velho, ou duas fontes discordam.

```
Passo 1: Receber o cv atual da pessoa
Passo 2: Coletar dados da pessoa para melhorar o cv
Passo 3: Enviar cv atualizado
...
Fontes que ela abre: Google, sistemas de ATS, conhecimento próprio
Regras que ela aplica: Particularidades de mercado, vagas, nível de senioridade, localização da vaga
O que ela faz quando algo falta: Pergunta para o usuário, busca parcerias de profissionais
```

**Um cenário concreto (opcional, mas muito útil)**

Uma entidade real ou realista (um ABO, um projeto, um pedido) atravessando o fluxo. Não precisa ser dado de produção.

```
[cenário]
```

**Perguntas para o solution design**

- [ ] Quais desses passos o produto deve **automatizar**, quais deve **assistir**, e quais continuam **humanos**?
- [ ] Alguma regra precisa virar pseudocódigo (se / então, com ordem de prioridade) já nesta fase?

---



## 4. Jornada desejada — como o produto deve funcionar

Obrigatório. Equivale ao *Proposed Design / high-level flow* dos BRDs mais maduros.

Conte o caminho feliz em 5–8 passos. Isto é visualização, não arquitetura.

- [ ] Consigo descrever o fluxo **do gatilho ao resultado** sem nomear frameworks.
- [ ] Está claro **quem faz o quê** em cada passo (pessoa vs. sistema vs. outro sistema).
- [ ] Existe um **ponto de revisão humana** se o produto infere, extrai ou recomenda algo.
- [ ] Consigo apontar **2–3 telas, mensagens ou artefatos** que a pessoa vê (mesmo que só em texto).

```
1. Usuário acessa página do chatbot, recebe boas vindas e diagnóstico inicial
2. Chatbot recomenda próximos passos e usuário escolhe um caminho
3. Chatbot coleta informações necessárias do usuário e fornece sugestões
4. Usuário recebe versão melhorada do cv, guia para entrevistas ou outros arquivos
5.
O que a pessoa vê no final: Arquivo / texto pronto
Onde um humano confirma ou corrige: Informa ao chatbot que aceita a entrega ou que quer mudanças
```

> Padrão Status Tracker: reunião → upload → transcrição → extração de status → revisão do tech lead → relatório de portfólio para o manager.  
> Padrão AI Context: AM está no LOS → clica em investigar com IA → chega no Analyzer com o prompt já preenchido.  
> Padrão Carrier Allocation: WMS envia o pedido → regras de mercado escolhem carrier/serviço → a mesma escolha vale para o pedido inteiro → se o serviço cair, devolve o original.

**Esboço visual (opcional)**

Caixas e setas em texto bastam. Não precisa de diagrama formal.

```
[Persona / Sistema A] --gatilho--> [Produto] --consulta--> [Fonte 1]
                                      |
                                      +--entrega--> [Artefato / tela / mensagem]
```

**Perguntas para o solution design**

- [ ] Isto é síncrono (a pessoa espera) ou assíncrono (job, processamento, status)? Síncrono
- [ ] O fluxo atravessa **mais de um produto** (ex.: Workspace → Analyzer)? Quem é dono de cada hop? Não

---



## 5. O que “bom” parece — resultado esperado

Obrigatório. Equivale a *Expected Output Format*.

Defina o entregável, não a implementação.

- [ ] **Estrutura:** seções, tabela, labels, arquivo, e-mail, payload, relatório.
- [ ] **Fidelidade:** o que precisa ser igual à fonte; o que pode ser resumido; o que **não** pode ser inventado.
- [ ] **Tom e limites:** linguagem, tamanho, o que não dizer.
- [ ] **Estados vazios:** o que mostrar quando não há dado, quando o dado é parcial, quando o usuário não tem acesso.
- [ ] **Critérios objetivos de aceite** (3–6 itens que um revisor conseguiria marcar sim/não).

```
Entregável: texto no chat, arquivo (pode ser por email)
Deve incluir: melhorias e fidelidade aos dados inseridos pelo usuário
Não pode incluir / inventar: dados que o usuário não forneceu, dados que não tenha como comprovar
Se faltar dado: informar ao usuário que não consegue complementar a resposta por falta de contexto
Checklist de “está bom”:
- [ ]
- [ ]
- [ ]
```

> Padrão repetido nos BRDs de AA: grounding em dado real, gaps explícitos, sugestões rastreáveis a um KPI ou campo.  
> Padrão Status Tracker: as mesmas dimensões e labels (Healthy / At Risk / Critical) em todos os projetos.

---



## 6. Escopo da primeira versão

Obrigatório. Equivale a *Requirements* + *Out of Scope*.

Nesta fase, requisitos podem ser frases de intenção. Ainda não precisam estar todos em linguagem de teste. Precisam ser suficientes para o solution design não desenhar o universo.

**Deve fazer nesta versão**

- [ ] Liste 5–12 capacidades. Prefira *must* / *shall* quando já estiver claro.
- [ ] Separe o que é **núcleo do fluxo** do que é **apoio** (admin, export, histórico).

```
1. Receber e responder mensagens de usuário em linguagem natural
2. Sugerir trilhas de conversa de acordo com contexto inicial do usuário
3. Fazer perguntas ao usuário para coletar informações
```

**Não faz nesta versão (mesmo que alguém peça)**

- [ ] Pelo menos 4 exclusões concretas (plataforma, integração, canal, analytics, edição, outro mercado, etc.).

```
- Não recebe ou interpreta áudio/vídeo
- Não faz pesquisas na web em tempo real
- Não cita fontes ou referências
- Não lida com carreiras fora da área de tecnologia
```

**Perguntas para o solution design**

- [ ] Alguma exclusão *muda o desenho* se voltar (ex.: “não tem notificação no MVP” vs. “nunca terá”)?
- [ ] Existe um sistema que **não** deve ser substituído — só consultado ou espelhado?

---



## 7. Dados que o produto precisa ver

Obrigatório como *mapa de perguntas*. Opcional como dicionário completo.

Sem isto, o solution design não sabe o que conectar. Não precisa fechar campos; precisa nomear **entidades** e **fontes candidatas**.

- [ ] Quais **entidades** o produto manipula (projeto, ABO, pedido, documento, usuário, mercado…)?
- [ ] Para cada entidade, **quem é a fonte da verdade hoje** (mesmo que seja “planilha” ou “a pessoa sabe”)?
- [ ] O produto **lê**, **escreve**, ou os dois?
- [ ] Há identificadores que já existem (`affiliate-abo`, código de warehouse, id de projeto)?
- [ ] Há dados sensíveis (reunião, risco, PII, documento de mercado)?


| Entidade | Para que serve no fluxo | Fonte candidata hoje | Lê / escreve | Sensível? | Ainda não sei |
| -------- | ----------------------- | -------------------- | ------------ | --------- | ------------- |
|          |                         |                      |              |           |               |


**Perguntas para o solution design (não responda tudo agora)**

- [ ] A fonte já expõe API / arquivo / evento, ou alguém precisa criar um endpoint?
- [ ] Qual a **frescor** aceitável (tempo real, diário, “igual à tela X”)?
- [ ] Se duas fontes divergirem, qual ganha?
- [ ] O que é obrigatório vs. opcional para o fluxo ainda funcionar?
- [ ] Precisaremos de **amostra de payload** e **mapeamento de campos** antes de desenvolver? (quase sempre sim, quando há integração)

---



## 8. Conexões, integrações e handoff

Obrigatório gerar as perguntas. Não é obrigatório ter as respostas.

Esta seção existe para o solution design desenhar o *como os pedaços se falam*. Nos BRDs reais, os buracos mais caros estavam aqui: botão no Workspace sem contrato de contexto; growth plan sem endpoint; WMS sem mapping de campo; fallback indefinido.

Para cada sistema que aparece na jornada:


| Sistema / time | Papel no fluxo (origem, destino, orquestrador) | O que precisa enviar ou receber | Gatilho | Se este sistema falhar | Dono (se souber) | Aberto? |
| -------------- | ---------------------------------------------- | ------------------------------- | ------- | ---------------------- | ---------------- | ------- |
|                |                                                |                                 |         |                        |                  |         |


Responda o que souber; deixe o resto como pergunta.

- [ ] Quem **inicia** a conversa entre sistemas (UI, job, webhook, usuário)?
- [ ] O que precisa **viajar no handoff** (id da entidade, mercado, prompt, arquivo, KPI da tela)?
- [ ] Autenticação / autorização: a pessoa já está logada em algum lugar que deve valer aqui?
- [ ] Comportamento se o outro lado estiver fora: erro visível, fallback, fila, “usar o original”?
- [ ] Ambientes (dev / qa / prod) importam já nesta conversa, ou só depois?

**Perguntas típicas para levar ao solution design**

- Como o sistema A passa contexto para o sistema B sem o usuário redigitar?
- A integração é síncrona (request/response) ou por arquivo / lote?
- Existe gateway, fila ou chamada direta?
- Quem é dono da regra: o produto novo ou o sistema de origem?
- Precisamos de feature toggle por mercado / warehouse / papel?

---



## 9. Regras, exceções e o que pode dar errado

Opcional detalhar; obrigatório *listar* os casos que você já enxerga.

- [ ] Regras de negócio conhecidas (mesmo em linguagem natural).
- [ ] Ordem de prioridade, se duas regras puderem se aplicar.
- [ ] Exceções de mercado, papel ou tipo de entidade (o que vale em um lugar e não em outro).
- [ ] Falhas previsíveis: dado ausente, dado velho, arquivo ilegível, entidade não encontrada, sem permissão, timeout.

```
Regras que já conhecemos:
Exceções:
Se der errado, a pessoa deve ver / o sistema deve fazer:
```

> Padrão Carrier Allocation: regras em se/então com prioridade; pedido inteiro no mesmo carrier; se o serviço cair, devolve o carrier original.  
> Padrão AA: se não houver perfil, avisar que a recomendação *não* usou perfil — não inventar.

**Perguntas para o solution design**

- [ ] Estas regras vivem em código, em motor de regras, em prompt, ou em configuração por mercado?
- [ ] Quais erros precisam de código / mensagem estável para teste?

---



## 10. Hipóteses de tecnologia — o que imaginar, sem fechar

Obrigatório como *capacidades*. Proibido tratar como decisão final nesta fase.

Não escolha stack aqui. Nomeie o **tipo de problema técnico** para o solution design ter de onde partir.

Marque o que *parece* necessário:

- [ ] Interface web / app existente / assistente conversacional / API sem UI / relatório
- [ ] Identidade e papéis (login, RBAC, herdar permissão de outro produto)
- [ ] Persistência (histórico, auditoria, arquivos)
- [ ] Busca ou recuperação de documentos
- [ ] Processamento de mídia (áudio, vídeo, PDF)
- [ ] Extração ou geração assistida por modelo (com revisão humana)
- [ ] Integração com sistema interno já existente
- [ ] Integração com terceiro / carrier / vendor
- [ ] Job assíncrono, fila, ou processamento com status
- [ ] Exportação (CSV, markdown, PDF)
- [ ] Observabilidade / trilha de auditoria

**Hipóteses (opcional) — deixe explícito que são hipóteses**

```
Talvez precise de: python, fastapi, RAG, banco de dados relacional, página na web em react, infra de cloud para deploy
Provavelmente NÃO precise de (nesta versão): infra complexa, integração com outros sistemas
O que eu não sei ainda sobre tecnologia: como manejar de forma MVP banco e cloud
```

**Perguntas para o solution design**

- Dado o fluxo da seção 4, isto pede um serviço novo, uma tela nova, ou só um contrato em cima do que já existe?
- Se houver IA: o que é determinístico (lookup, regra, CRUD) e o que é generativo?
- Onde os segredos, arquivos e PII podem viver, em tese?
- Existe restrição de vendor, nuvem ou dado que já limita as opções?

---



## 11. Premissas, riscos e perguntas em aberto

Obrigatório ter a lista. Não é obrigatório ter mitigação.

- [ ] **Premissas** que, se forem falsas, derrubam a ideia (adoção, qualidade de dado, o time X entrega o endpoint, revisão humana é aceitável).
- [ ] **Riscos** de prazo, qualidade, compliance, dependência de outro time.
- [ ] **Perguntas em aberto** com dono e, se possível, data-alvo. “To be done” sem dono não alimenta solution design.


| Tipo     | Item | Dono | Até quando | Bloqueia o SD? |
| -------- | ---- | ---- | ---------- | -------------- |
| Premissa |      |      |            |                |
| Risco    |      |      |            |                |
| Pergunta |      |      |            |                |


---



## 12. Gate: isto já alimenta um solution design?

Não avance para desenhar solução como se o produto estivesse definido. Avance quando a *história* estiver visível e as *perguntas certas* estiverem escritas.

**Pode ir para solution design se:**

- [ ] Consigo contar o caminho feliz em voz alta, do gatilho ao resultado.
- [ ] Sei quem sofre a dor e o que muda no trabalho dela.
- [ ] Sei o que a primeira versão *não* faz.
- [ ] Nomeei as entidades e pelo menos as fontes *candidatas*.
- [ ] Listei os sistemas que provavelmente precisam se falar, mesmo sem contrato.
- [ ] Tenho uma lista de perguntas sobre conexão, integração e tecnologia — não um stack fechado.
- [ ] Há pelo menos um cenário concreto (real ou realista) para discutir.

**Ainda não é hora de solution design se:**

- [ ] O problema é “não ter a feature”.
- [ ] O fluxo manual está em branco.
- [ ] Não há exclusões de escopo.
- [ ] Não se sabe de onde viria o dado, nem como pergunta.
- [ ] Já se escolheu banco, cloud e modelo sem ter o fluxo.

**Handoff sugerido**


| Este checklist | Alimenta no BRD (`BRD_template.md`)                    | Alimenta no solution design                    |
| -------------- | ------------------------------------------------------ | ---------------------------------------------- |
| §§1–2          | 1. Use Case · 2. Example Inputs                        | Problem statement · atores · pontos de entrada |
| §3             | 3. Manual Process                                      | Regras, fontes, edge cases                     |
| §§4–5          | 4. Expected Output · 5. Requirements · Proposed design | Fluxo de dados alto nível · UX do resultado    |
| §6             | 5. Requirements · 6. Out of Scope                      | Limite da arquitetura da v1                    |
| §§7–8          | 7.2 Dependencies                                       | Data flow · dicionário · contratos · mapping   |
| §9             | 4.2 Validation · 7.1 Risks                             | Error scenarios · fallback                     |
| §10            | 7.2 Tools (ainda como hipótese)                        | Opções de tecnologia, não a escolha final      |
| §11            | 7.3 Open questions · Assumptions                       | Backlog de decisões técnicas                   |


Quando este checklist estiver “bom o bastante”, o próximo passo não é escolher a stack. É um solution design que responda: **como isto se conecta, o que integra com o quê, e quais tecnologias são candidatas** — com as perguntas daqui como índice.

---



## Controle do documento


| Versão | Data       | Autor            | Mudança                                                                                                                      |
| ------ | ---------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 0.1    | 2026-08-25 | Gabriel / Cursor | Versão inicial, derivada do template de BRD, BRDs de AA, Status Tracker, Carrier Allocation e da cadeia BRD → spec → mapping |


