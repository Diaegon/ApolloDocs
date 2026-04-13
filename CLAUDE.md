# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ApolloDocs is a SaaS that automates generation of technical documentation for solar energy projects in Brazil (focused on ENEL-CE utility in Ceará). It generates PDFs for: Memorial Descritivo, Procuração, Diagrama Unifilar, and Formulário ENEL-CE, as well as managing persistent data for clients, projects, people, and equipment.

## Commands

All tasks use `taskipy` (`task <name>`):

```bash
task dev          # Start dev server with auto-reload (loads .env.dev)
task run          # Start production server
task test         # Run all tests with coverage (lint first)
task lint         # ruff check
task format       # ruff format (pre_format runs --fix first)
task db-up        # Start PostgreSQL via docker compose
task db-down      # Stop PostgreSQL
task migrate-dev  # alembic upgrade head
```

Run a single test file or function:
```bash
pytest api/tests/test_docs.py -s -vv
pytest api/tests/test_docs.py::test_generate_memorial_descritivo -s -vv
```

## Architecture

```
HTTP Request → FastAPI Router → DocsService → ProjectFactory → Domain (Calculations) → PDF Builder → StreamingResponse
                             ↘ CRUD Routers → SQLAlchemy ORM → PostgreSQL
```

**Layers:**

- `api/routers/` — HTTP endpoints:
  - `docs.py` — document generation endpoints
  - `auth.py`, `users.py` — authentication and user management
  - `clientes.py` — CRUD for clients + sub-endpoints for `enderecos_cliente` and `enderecos_obra`
  - `projetos.py` — CRUD for projects (links cliente, procurador, projetista, inversores, placas)
  - `procuradores.py` — CRUD for procuradores
  - `projetistas.py` — CRUD for projetistas
  - `inversores.py` — lists INMETRO-certified inverter PDFs from `INMETRO_INVERSORES/`
- `api/services/docs_service.py` — Orchestrates document generation; decouples HTTP from logic
- `api/services/all_docs_service.py` — Generates all four docs and returns a ZIP
- `api/schemas/` — Pydantic request/response models (nested: `projetos/`, `cliente/`, `pessoas/`, `sistema/`, `common/`)
- `api/schemas/models.py` — SQLAlchemy ORM models: `User`, `Cliente`, `Inversor`, `Placa`, `Procurador`, `Projetista`, `EnderecoCliente`, `EnderecoObra`, `Projeto`
- `src/createproject.py` — Factory: converts API Pydantic models → domain objects
- `src/domain/creatememorialobject.py` — Engineering calculations for memorial (extends `calculos.py`)
- `src/domain/creatediagramobject.py` — Diagram-specific calculations
- `src/domain/texts/` — Text generation for documents
- `src/buildingdocuments/` — PDF builders; memorial & procuração use Jinja2+WeasyPrint; diagrama & formulário use PyMuPDF on pre-existing templates
- `src/templates/` — HTML templates for WeasyPrint
- `src/config.py` — Engineering constants (site-specific values for Ceará, e.g. peak sun hours, copper resistivity)

**PDF generation approach:**
- `memorial` & `procuracao`: HTML template rendered via Jinja2, then converted to PDF with WeasyPrint
- `diagramaunifilar` & `formularioenel`: PyMuPDF fills fields in pre-built PDF templates from `support-files/`

## Database & Auth

- PostgreSQL 16 via Docker (credentials in `docker-compose.yml` and `.env.dev`)
- SQLAlchemy 2.0 ORM with Alembic migrations in `migrations/`
- JWT auth (PyJWT + Argon2 password hashing). All `/docs` and CRUD endpoints require Bearer token.
- All CRUD resources are user-scoped: queries always filter by `user_id = current_user.id`
- Tests use in-memory SQLite; fixtures in `api/tests/conftest.py`

## ORM Models

| Model | Table | Key Relations |
|-------|-------|---------------|
| `User` | `users` | owns all other resources |
| `Cliente` | `clientes` | has many `EnderecoCliente`, `EnderecoObra` |
| `EnderecoCliente` | `enderecocliente` | belongs to `Cliente` |
| `EnderecoObra` | `enderecoobra` | belongs to `Cliente`; has optional lat/lon |
| `Procurador` | `procuradores` | standalone, user-scoped |
| `Projetista` | `projetistas` | standalone, user-scoped |
| `Inversor` | `inversores` | global (no user_id); linked from `Projeto` |
| `Placa` | `placas` | global (no user_id); linked from `Projeto` |
| `Projeto` | `projetos` | links cliente + procurador (required) + projetista + up to 3 inversores + 3 placas |

## INMETRO Inverters

`INMETRO_INVERSORES/` (repo root) holds PDF certification files organized as `brand/model/*.pdf`.
Currently 12 brands (CANADIAN, DEYE, GROWATT, HOYMILES, HUAWEI, LIVOLTEK, PHB, RENO, SMA, SOLAR EDGE, …).

- `GET /inversores/list` — returns JSON tree of brands → models → PDF filenames (auth required)
- `GET /inversores/{brand}/{model}/{file}.pdf` — static file serving via FastAPI `StaticFiles` mount at `/inversores`

In Docker, `INMETRO_INVERSORES/` is bind-mounted read-only to `/app/INMETRO_INVERSORES`.

## Infrastructure

Full Docker Compose stack (production):
- `db` — PostgreSQL 16 Alpine (internal network only)
- `api` — FastAPI (internal + web networks); env vars via `.env`
- `frontend` — Next.js 15 (web network); build args for `NEXT_PUBLIC_*`
- `nginx` — Reverse proxy; ports 80 + 443; SSL certs at `nginx/ssl/`; config at `nginx/nginx.conf`

CORS origins configured via `CORS_ORIGINS` env var (comma-separated).

## Setup Notes

- Python 3.12+, managed via Poetry
- `support-files/` (images, PDF templates for diagrams/forms) must be downloaded separately and placed in the repo root — not tracked by git
- `INMETRO_INVERSORES/` must be present at repo root; not tracked by git
- Ruff line length: 79; linting rules: I, F, E, W, PL, PT, FAST; `migrations/` and `formularioENEL.py` are excluded
