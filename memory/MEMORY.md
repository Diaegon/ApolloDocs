# ApolloDocs Project Memory

## Project Overview
FastAPI backend that generates PDFs for solar energy projects (ENEL-CE, Ceará, Brazil).
Documents: Memorial Descritivo, Procuração, Diagrama Unifilar, Formulário ENEL-CE.

## Structure
- Backend: `/` (Python/FastAPI/Poetry) — see CLAUDE.md for commands
- Frontend: `/frontend/` (Next.js 15, TypeScript) — **separate from backend**

## Frontend Stack
Next.js 15 App Router · TypeScript · Tailwind CSS · React Hook Form + Zod · TanStack Query v5 · Vitest

See details: [frontend.md](frontend.md)

## Backend Core Engine (`src`)
The `src/` directory functions as the central engine for solar calculations and pure domain logic (calculates math and builds PDFs via Jinja+WeasyPrint / PyMuPDF).
See details: [src_analysis.md](src_analysis.md)

## Key Bug Patterns Found

### Pydantic v2 nullable required fields
Fields typed `X | None` with **no default** are REQUIRED in Pydantic v2.
The frontend must always send them — even as `null` — or FastAPI returns 422.
Affected fields in `ProjetoMemorial`: `id_projeto`, `cliente`, `endereco_obra`,
`Inversor.id_inversor`, `Placa.id_placa`, `Placa.eficiencia_placa`.
Fix: normalize `undefined → null` in form `onSubmit` before calling `generate()`.

### TSX generic arrow functions
In `.tsx` files, `<T>(v: T) =>` is parsed as JSX.
Fix: always use trailing comma → `<T,>(v: T) =>`.

### Testing: mocking before render
Mocking `document.createElement` before `render()` breaks React's own DOM creation silently (body ends up empty).
Fix: call `render()` first, then set up the mock.

### Testing: TanStack Query v5 isPending
`isPending` is set asynchronously. Checking it immediately after `act(() => mutate())` will be `false`.
Fix: use `await waitFor(() => expect(...isPending).toBe(true))`.

## Infrastructure & Deployment
- **Dockerized Environment**: The application (Next.js frontend, FastAPI backend, PostgreSQL) is fully containerized via Docker Compose.
- **Nginx Reverse Proxy**: Centralizes incoming traffic and routes requests securely. Removes direct public port exposure for the API and frontend services. Database access is restricted to the backend API via internal Docker networking.
- **HTTPS Enforcement**: Best practices on Docker environment for production rely on HTTPS, with configurations optimized for a 443-only setup.

## Recent Architectural Changes
- **Docs Endpoints Refactored**: Document generation endpoints (`/docs`) no longer rely on `user_id` from headers, using the `current_user` auth token directly instead.
- **Database Expansion**: Implemented and populated new models for `clientes`, `procuradores`, `projetistas`, and `inversores`.
- **Testing Enhancements**: Extended frontend test coverage specifically for the document generation process ("Todos os Documentos" format).
