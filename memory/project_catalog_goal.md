---
name: Material Catalog Lookup Goal
description: Goal to auto-populate inversor/placa specs from DB catalog by brand+model, removing manual spec entry
type: project
---

User wants to eliminate manual spec entry for inversores and placas in doc generation.
Instead of filling in potencia, tensao, corrente, etc. manually, the user will select brand+model and the system auto-fills from a catalog.

**Why:** Reduces data entry errors and speeds up project creation for solar installers.

**How to apply:** When designing catalog lookup, reference this goal to drive decisions.

## Current State (as of 2026-04-12)

### What already exists in the DB:
- `inversores` table: `marca_inversor`, `modelo_inversor`, `potencia_inversor`, `numero_fases`, `tipo_de_inversor`, `numero_mppt` — already the right structure for a catalog
- `placas` table: `marca_placa`, `modelo_placa`, `potencia_placa`, `tipo_celula`, `tensao_pico`, `corrente_curtocircuito`, `tensao_maxima_potencia`, `corrente_maxima_potencia`, `eficiencia_placa` — same
- Both are **global** (no `user_id`) — intended to be shared catalog entries
- `Projeto` already FK-links up to 3 inversores and 3 placas by ID

### What is MISSING:
1. **No CRUD router for inversores/placas DB catalog** — `api/routers/inversores.py` only lists INMETRO PDF files (filesystem), not DB records. There is no `api/routers/placas.py` at all.
2. **Doc generation does not look up by ID** — payload requires inline full spec objects (all technical fields) rather than pointing to an `id_inversor` or `id_placa` in the DB.
3. **No seeding / import flow** for populating the catalog from INMETRO PDFs or a CSV.

### The clean solution path:
1. Add `GET/POST /equipamentos/inversores` and `GET/POST /equipamentos/placas` CRUD endpoints to manage the catalog
2. Modify the `v2` doc generation endpoint to accept `{ id_inversor, quantidade }` + `{ id_placa, quantidade }` — service fetches full specs from DB before passing to domain layer
3. The `ProjetoMemorialV2` schema's `inversores: list[MaterialInversor]` already has `Inversor_v2` (marca+modelo+quantidade) — could extend or replace with `id`-based lookup

### Hint already in code:
`api/schemas/sistema/inversor.py` already defines `Inversor_v2`:
```python
class Inversor_v2(BaseModel):
    marca_inversor: str
    modelo_inversor: str
    quantidade: int
```
This signals the dev was already thinking about a lighter reference schema.
The most natural evolution: replace with `id_inversor + quantidade` and do the DB lookup in the service layer.
