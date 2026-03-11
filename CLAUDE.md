# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ApolloDocs automates generation of technical documentation for solar energy projects in Brazil (focused on ENEL-CE utility in Ceará). It generates PDFs for: Memorial Descritivo, Procuração, Diagrama Unifilar, and Formulário ENEL-CE.

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
```

**Layers:**

- `api/routers/` — HTTP endpoints (auth, users, docs)
- `api/services/docs_service.py` — Orchestrates document generation; decouples HTTP from logic
- `api/schemas/` — Pydantic request/response models (nested: `projetos/`, `cliente/`, `pessoas/`, `sistema/`, `common/`)
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
- JWT auth (PyJWT + Argon2 password hashing). All `/docs` endpoints require Bearer token.
- Tests use in-memory SQLite; fixtures in `api/tests/conftest.py`

## Setup Notes

- Python 3.12+, managed via Poetry
- `support-files/` (images, PDF templates for diagrams/forms) must be downloaded separately and placed in the repo root — not tracked by git
- Ruff line length: 79; linting rules: I, F, E, W, PL, PT, FAST; `migrations/` and `formularioENEL.py` are excluded
