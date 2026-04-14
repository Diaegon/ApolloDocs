import { apiFetch } from "./client";
import type {
  ProjetoMemorial,
  ProjetoProcuracao,
  ProjetoUnifilar,
  ProjetoFormularioEnelCe,
  ProjetoTodos,
  ProjetoMemorialV2,
  ProjetoUnifilarV2,
  InversorPublic,
  PlacaPublic,
} from "@/types/docs";

/**
 * Generate Memorial Descritivo PDF.
 * Returns the raw Response so the caller can stream or blob it.
 */
export async function generateMemorialDescritivo(
  data: ProjetoMemorial
): Promise<Response> {
  return apiFetch("/docs/memorialdescritivo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

/**
 * Generate Procuração PDF.
 */
export async function generateProcuracao(
  data: ProjetoProcuracao
): Promise<Response> {
  return apiFetch("/docs/procuracao", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

/**
 * Generate Diagrama Unifilar PDF.
 */
export async function generateDiagramaUnifilar(
  data: ProjetoUnifilar
): Promise<Response> {
  return apiFetch("/docs/diagramaunifilar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

/**
 * Generate Formulário ENEL-CE PDF.
 */
export async function generateFormularioEnel(
  data: ProjetoFormularioEnelCe
): Promise<Response> {
  return apiFetch("/docs/formularioenel", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

/**
 * Generate All Documents (ZIP).
 */
export async function generateTodosDocumentos(
  data: ProjetoTodos
): Promise<Response> {
  return apiFetch("/docs/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

// ─── Equipment catalog (v2) ──────────────────────────────────────────────────

export async function getInversores(): Promise<{ inversores: InversorPublic[] }> {
  const res = await apiFetch("/equipamentos/inversores/");
  if (!res.ok) throw new Error("Failed to fetch inversores");
  return res.json();
}

export async function getPlacas(): Promise<{ placas: PlacaPublic[] }> {
  const res = await apiFetch("/equipamentos/placas/");
  if (!res.ok) throw new Error("Failed to fetch placas");
  return res.json();
}

// ─── v2 document endpoints ───────────────────────────────────────────────────

export async function generateMemorialDescritivoV2(
  data: ProjetoMemorialV2
): Promise<Response> {
  return apiFetch("/docs/v2/memorialdescritivo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export async function generateDiagramaUnifilarV2(
  data: ProjetoUnifilarV2
): Promise<Response> {
  return apiFetch("/docs/v2/diagramaunifilar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}
