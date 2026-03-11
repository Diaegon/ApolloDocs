# ApolloDocs

Sistema SaaS para automação de documentação técnica em projetos de energia solar fotovoltaica, focado na área de concessão da **ENEL-CE (Ceará, Brasil)**.

O usuário preenche os dados do projeto uma única vez e o sistema gera automaticamente todos os documentos necessários para homologação na distribuidora.

---

## Documentos Gerados

| Documento | Engine | Endpoint |
|-----------|--------|----------|
| Memorial Descritivo | Jinja2 + WeasyPrint | `POST /docs/memorialdescritivo` |
| Procuração Particular | Jinja2 + WeasyPrint | `POST /docs/procuracao` |
| Diagrama Unifilar | PyMuPDF (template) | `POST /docs/diagramaunifilar` |
| Formulário ENEL-CE | PyMuPDF (template) | `POST /docs/formularioenel` |
| **Todos (ZIP)** | Todos os acima | `POST /docs/todos` |

---

## Arquitetura

```
HTTP Request
    │
    ▼
FastAPI Router (api/routers/)
    │
    ▼
Service Layer (api/services/)
    │   DocsService          → geração individual
    │   AllDocsService       → gera todos e retorna ZIP
    ▼
ProjectFactory (src/createproject.py)
    │   converte Pydantic schemas → objetos de domínio
    ▼
Domain Layer (src/domain/)
    │   creatememorialobject.py  → cálculos elétricos (memorial)
    │   creatediagramobject.py   → cálculos para diagrama unifilar
    │   texts/                   → geração de textos técnicos
    ▼
PDF Builders (src/buildingdocuments/)
    │   memorialdescritivo.py    → WeasyPrint
    │   procuracao.py            → WeasyPrint
    │   unifilar.py              → PyMuPDF
    │   formularioENEL.py        → PyMuPDF
    ▼
StreamingResponse (PDF) ou ZIP
```

---

## Estrutura do Projeto

```
ApolloDocs/
├── api/                          # FastAPI backend
│   ├── app.py                    # instância da aplicação
│   ├── database.py               # sessão SQLAlchemy
│   ├── security.py               # JWT auth (PyJWT + Argon2)
│   ├── settings.py               # variáveis de ambiente
│   ├── routers/
│   │   ├── auth.py               # POST /auth/token
│   │   ├── users.py              # CRUD de usuários
│   │   └── docs.py               # endpoints de geração de documentos
│   ├── schemas/
│   │   ├── projetos/
│   │   │   ├── memorial.py       # ProjetoMemorial
│   │   │   ├── procuracao.py     # ProjetoProcuracao
│   │   │   ├── unifilar.py       # ProjetoUnifilar
│   │   │   ├── formularioenelce.py  # ProjetoFormularioEnelCe
│   │   │   └── completo.py       # ProjetoTodos (payload unificado)
│   │   ├── cliente/              # Cliente, EnderecoObra, EnderecoCliente
│   │   ├── pessoas/              # Procurador, Projetista
│   │   ├── sistema/              # ConfiguracaoSistema, Inversor, Placa
│   │   └── common/enums.py       # classe_consumo, tensao_fase, ramal_de_energia
│   ├── services/
│   │   ├── docs_service.py       # DocsService (geração individual)
│   │   └── all_docs_service.py   # AllDocsService (gera todos → ZIP)
│   └── tests/
│       ├── conftest.py           # fixtures (SQLite in-memory, client, user, token)
│       ├── test_docs.py          # testes dos endpoints de documentos
│       ├── test_payloads.py      # payloads reutilizáveis nos testes
│       ├── test_retorno_memorial.py  # testes dos cálculos do memorial
│       ├── test_security.py
│       ├── test_app.py
│       └── test_db.py
│
├── src/                          # lógica de domínio e geração de PDFs
│   ├── config.py                 # constantes de engenharia (Ceará: HSP, resistividade Cu)
│   ├── createproject.py          # ProjectFactory: Pydantic → objetos de domínio
│   ├── domain/
│   │   ├── creatememorialobject.py   # cálculos elétricos para memorial
│   │   ├── creatediagramobject.py    # cálculos para diagrama unifilar
│   │   ├── utils/calculos.py         # funções de cálculo base
│   │   ├── texts/
│   │   │   ├── text_memorial.py      # textos técnicos do memorial
│   │   │   └── text_procuracao.py    # texto da procuração
│   │   └── components/tablesmemorial.py
│   ├── buildingdocuments/
│   │   ├── memorialdescritivo.py  # HTML → PDF (WeasyPrint)
│   │   ├── procuracao.py          # HTML → PDF (WeasyPrint)
│   │   ├── unifilar.py            # template PDF + PyMuPDF
│   │   └── formularioENEL.py      # template PDF + PyMuPDF
│   ├── schemas/
│   │   ├── modelreturnobject.py   # ProjetoCompleto (dataclass de domínio)
│   │   ├── constantes.py
│   │   └── models.py
│   └── templates/                 # templates HTML para WeasyPrint
│
├── frontend/                      # Next.js 15 SaaS frontend
│   ├── middleware.ts              # proteção de rotas /dashboard/*
│   └── src/
│       ├── app/
│       │   ├── api/auth/          # proxy de login/logout (define cookie httpOnly)
│       │   ├── api/docs/          # proxy de PDFs (lê cookie, repassa ao FastAPI)
│       │   ├── (auth)/            # páginas de login e registro
│       │   └── (dashboard)/       # páginas do sistema (memorial, procuracao, etc.)
│       ├── components/
│       │   ├── forms/             # memorial-form, procuracao-form, unifilar-form, formulario-form
│       │   ├── layout/            # header, sidebar
│       │   ├── pdf-viewer.tsx
│       │   └── ui/                # button, card, input, select, label, form-field
│       ├── hooks/use-generate-doc.ts
│       ├── lib/
│       │   ├── api/client.ts      # apiFetch (server) + clientFetch (client)
│       │   ├── payload/normalize.ts  # normalização de payloads (undefined → null)
│       │   └── validations/       # schemas Zod por formulário
│       ├── types/auth.ts, docs.ts
│       └── __tests__/             # Vitest + RTL (validações, forms, hooks, componentes)
│
├── support-files/                 # templates PDF para PyMuPDF (não versionado)
├── migrations/                    # Alembic migrations
├── docker-compose.yml             # PostgreSQL 16
├── pyproject.toml                 # Poetry + taskipy
└── .env.dev                       # variáveis de ambiente (desenvolvimento)
```

---

## Segurança (Frontend)

- JWT armazenado **exclusivamente** em cookie `httpOnly`, `SameSite=strict`, duração 8h
- Cookie definido via rota proxy Next.js `/api/auth/login` — nunca exposto ao JavaScript do cliente
- Rotas de PDF `/api/docs/*` leem o cookie no servidor, repassam o JSON ao FastAPI e fazem streaming da resposta — o cliente nunca vê a URL do backend nem o token
- `middleware.ts` protege `/dashboard/*` e redireciona usuários autenticados para fora das páginas de auth

---

## Pré-requisitos

- **Python 3.12+** com [Poetry](https://python-poetry.org/docs/#installation)
- **Node.js 20+** com npm
- **Docker** (para PostgreSQL)

---

## Instalação

### Backend

```bash
# 1. Instalar dependências Python
poetry install

# 2. Subir o banco de dados
task db-up

# 3. Rodar as migrations
task migrate-dev

# 4. Baixar arquivos de suporte (templates PyMuPDF)
# Faça o download da pasta support-files em:
# https://drive.google.com/drive/folders/1wS_3gRbTehiSYByUsZgDKmRfIrHZ1TSS
# e coloque na raiz do projeto.

# 5. Iniciar o servidor de desenvolvimento
task dev
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Comandos (`taskipy`)

```bash
task dev          # Servidor de desenvolvimento com auto-reload (carrega .env.dev)
task run          # Servidor de produção
task test         # Todos os testes com cobertura (roda lint antes)
task lint         # ruff check
task format       # ruff format
task db-up        # Iniciar PostgreSQL via docker compose
task db-down      # Parar PostgreSQL
task migrate-dev  # alembic upgrade head
```

Rodar um teste específico:
```bash
pytest api/tests/test_docs.py -s -vv
pytest api/tests/test_docs.py::test_generate_memorial_descritivo -s -vv
```

### Frontend
```bash
cd frontend
npm run dev       # Servidor Next.js (porta 3000)
npm run build     # Build de produção
npm test          # Vitest
npm run lint      # ESLint
```

---

## Endpoints da API

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/token` | Login (OAuth2 password flow) |
| POST | `/users/` | Criar usuário |

### Documentos (requer Bearer token)
| Método | Rota | Resposta | Payload |
|--------|------|----------|---------|
| POST | `/docs/memorialdescritivo` | PDF | `ProjetoMemorial` |
| POST | `/docs/procuracao` | PDF | `ProjetoProcuracao` |
| POST | `/docs/diagramaunifilar` | PDF | `ProjetoUnifilar` |
| POST | `/docs/formularioenel` | PDF | `ProjetoFormularioEnelCe` |
| POST | `/docs/todos` | ZIP (4 PDFs) | `ProjetoTodos` |

O endpoint `/docs/todos` recebe um único payload unificado (`ProjetoTodos`) e retorna um arquivo `.zip` com os quatro documentos:
- `memorial_descritivo.pdf`
- `procuracao.pdf`
- `diagrama_unifilar.pdf`
- `formulario_enel_ce.pdf`

---

## Banco de Dados

- **PostgreSQL 16** via Docker (credenciais em `docker-compose.yml` e `.env.dev`)
- **SQLAlchemy 2.0** ORM com migrações via Alembic (`migrations/`)
- Testes usam **SQLite in-memory** via fixtures em `api/tests/conftest.py`

---

## Observações Técnicas

- Os templates para PyMuPDF (`support-files/`) não são versionados — baixe separadamente pelo link acima
- `support-files/` deve ficar na raiz do projeto
- Constantes de engenharia específicas do Ceará (HSP, resistividade do cobre, etc.) estão em `src/config.py`
- Ruff: comprimento de linha 79; regras I, F, E, W, PL, PT, FAST; `migrations/` e `formularioENEL.py` excluídos do lint
