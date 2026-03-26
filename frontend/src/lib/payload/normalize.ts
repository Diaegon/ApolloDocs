/**
 * Payload normalization utilities.
 *
 * Pydantic v2 treats `field: X | None` with no default as a REQUIRED field —
 * the JSON key must be present even when the value is null. Zod's `.optional()`
 * omits undefined keys from serialization, which would cause 422 from FastAPI.
 *
 * These functions convert form data (where optional fields may be undefined)
 * into the exact payloads expected by each backend endpoint.
 */

import type { ProjetoMemorialFormData } from "@/lib/validations/memorial";
import type { ProjetoProcuracaoFormData } from "@/lib/validations/procuracao";
import type { ProjetoUnifilarFormData } from "@/lib/validations/unifilar";
import type {
  ProjetoMemorial,
  ProjetoProcuracao,
  ProjetoUnifilar,
} from "@/types/docs";

type SistemaFormData = ProjetoMemorialFormData["sistema_instalado1"];

/** Ensures id_inversor, id_placa and eficiencia_placa are null (not undefined). */
function normalizeSistema(s: SistemaFormData) {
  const result: any = {
    ...s,
    inversor: {
      ...s.inversor,
      id_inversor: s.inversor.id_inversor ?? null,
    },
    placa: {
      ...s.placa,
      id_placa: s.placa.id_placa ?? null,
      eficiencia_placa: s.placa.eficiencia_placa ?? null,
    },
  };

  if (s.placa2) {
    result.placa2 = {
      ...s.placa2,
      id_placa: s.placa2.id_placa ?? null,
      eficiencia_placa: s.placa2.eficiencia_placa ?? null,
    };
  }

  return result as any;
}

export function normalizeMemorialPayload(
  data: ProjetoMemorialFormData
): ProjetoMemorial {
  return {
    ...data,
    id_projeto: data.id_projeto ?? null,
    cliente: data.cliente ?? null,
    endereco_obra: data.endereco_obra ?? null,
    sistema_instalado1: normalizeSistema(data.sistema_instalado1),
    sistema_instalado2: data.sistema_instalado2
      ? normalizeSistema(data.sistema_instalado2)
      : undefined,
    sistema_instalado3: data.sistema_instalado3
      ? normalizeSistema(data.sistema_instalado3)
      : undefined,
  };
}

export function normalizeProcuracaoPayload(
  data: ProjetoProcuracaoFormData
): ProjetoProcuracao {
  return {
    ...data,
    id_projeto: data.id_projeto ?? null,
  };
}

export function normalizeUnifilarPayload(
  data: ProjetoUnifilarFormData
): ProjetoUnifilar {
  return {
    ...data,
    sistema_instalado1: normalizeSistema(data.sistema_instalado1),
    sistema_instalado2: data.sistema_instalado2
      ? normalizeSistema(data.sistema_instalado2)
      : undefined,
    sistema_instalado3: data.sistema_instalado3
      ? normalizeSistema(data.sistema_instalado3)
      : undefined,
  };
}

import type { ProjetoTodosFormData } from "@/lib/validations/todos";
import type { ProjetoTodos } from "@/types/docs";

export function normalizeTodosPayload(
  data: ProjetoTodosFormData
): ProjetoTodos {
  return {
    ...data,
    id_projeto: data.id_projeto ?? null,
    sistema_instalado1: normalizeSistema(data.sistema_instalado1),
    sistema_instalado2: data.sistema_instalado2
      ? normalizeSistema(data.sistema_instalado2)
      : undefined,
    sistema_instalado3: data.sistema_instalado3
      ? normalizeSistema(data.sistema_instalado3)
      : undefined,
  };
}
