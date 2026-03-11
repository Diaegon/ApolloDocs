# Frontend Architecture

## Location
`/home/d1aegon/Documentos/code/ApolloDocs/frontend/`

## Commands
```bash
cd frontend
npm run dev       # http://localhost:3000
npm test          # vitest run (73 tests)
npm run build     # production build
```
Env: copy `.env.local.example` → `.env.local`, set `BACKEND_URL=http://localhost:8000`.

## Security Model
JWT stored in **httpOnly cookie** (`apollo_token`) — never exposed to client JS.

Flow:
1. Client POSTs `{email, password}` to `/api/auth/login` (Next.js route)
2. Route forwards to FastAPI `POST /token` as `application/x-www-form-urlencoded`
3. Sets `apollo_token` httpOnly + SameSite=strict cookie (8h)
4. `middleware.ts` guards all `/dashboard/*` — redirects to `/login` if no cookie
5. PDF proxy routes (`/api/docs/*`) read cookie server-side, add `Authorization: Bearer`
6. Client never sees the JWT or the backend URL

## File Map
```
src/
├── app/
│   ├── api/auth/login/route.ts     ← sets httpOnly JWT cookie
│   ├── api/auth/logout/route.ts    ← clears cookie
│   ├── api/docs/*/route.ts         ← PDF proxy (4 routes)
│   ├── (auth)/login/page.tsx
│   ├── (auth)/register/page.tsx
│   └── (dashboard)/dashboard/
│       ├── page.tsx                ← overview with 4 doc cards
│       ├── memorial/page.tsx
│       ├── procuracao/page.tsx
│       ├── unifilar/page.tsx
│       └── formulario/page.tsx
├── components/
│   ├── ui/                         ← Button, Input, Label, Select, Card, FormField
│   ├── layout/                     ← Sidebar, Header
│   ├── forms/                      ← one form component per document type
│   └── pdf-viewer.tsx              ← iframe + download, revokes blob URL on unmount
├── lib/
│   ├── api/client.ts               ← apiFetch (server-side) + clientFetch
│   ├── api/docs.ts                 ← server-side FastAPI calls
│   └── validations/                ← Zod schemas mirroring Pydantic models
├── hooks/use-generate-doc.ts       ← TanStack Query mutation → blob URL
├── types/docs.ts                   ← TypeScript types for all API schemas
└── __tests__/                      ← 73 tests (vitest + RTL)
```
## API Endpoints (Backend)
| Frontend route | Backend route | Method |
|---|---|---|
| `/api/auth/login` | `POST /token` | form-urlencoded |
| `/api/docs/memorial` | `POST /docs/memorialdescritivo` | JSON → PDF stream |
| `/api/docs/procuracao` | `POST /docs/procuracao` | JSON → PDF stream |
| `/api/docs/unifilar` | `POST /docs/diagramaunifilar` | JSON → PDF stream |
| `/api/docs/formulario` | `POST /docs/formularioenel` | JSON → PDF stream |

## Payload Normalization
All forms use `src/lib/payload/normalize.ts` (exported functions) before calling `generate()`.
This ensures Pydantic v2 required-nullable fields are always sent as `null` (not omitted).

| Form | Normalized fields |
|---|---|
| Memorial | `id_projeto`, `cliente`, `endereco_obra`, `id_inversor`, `id_placa`, `eficiencia_placa` |
| Procuracao | `id_projeto` |
| Unifilar | `id_inversor`, `id_placa`, `eficiencia_placa` per sistema |
| Formulario | no normalization needed (all fields have backend defaults) |

`tensao_local` is `int` in backend (not string). Zod uses `z.coerce.number().int()` in
unifilar and formulario schemas. Form inputs use `type="number"`.

Payload shape tests are in `src/__tests__/forms/payload.test.ts` (25 tests).

## .gitignore entries added
`frontend/node_modules/`, `frontend/.next/`, `frontend/.env.local`, `frontend/coverage/`, `frontend/.turbo/`
