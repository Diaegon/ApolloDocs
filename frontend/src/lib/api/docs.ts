import { apiFetch } from "./client";
import type {
  ProjetoMemorial,
  ProjetoProcuracao,
  ProjetoUnifilar,
  ProjetoFormularioEnelCe,
  ProjetoTodos,
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
