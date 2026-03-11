/**
 * Payload shape tests.
 *
 * These tests verify that the normalized payloads sent to each backend endpoint
 * match what FastAPI / Pydantic v2 expects — specifically:
 *   1. Required-nullable fields (typed `X | None` with no default) are present
 *      as `null` rather than being omitted.
 *   2. Numeric fields that the backend declares as `int` are numbers, not strings.
 *   3. Optional fields with backend defaults may be omitted without error.
 */

import { describe, it, expect } from "vitest";
import {
  normalizeMemorialPayload,
  normalizeProcuracaoPayload,
  normalizeUnifilarPayload,
} from "@/lib/payload/normalize";
import type { ProjetoMemorialFormData } from "@/lib/validations/memorial";
import type { ProjetoProcuracaoFormData } from "@/lib/validations/procuracao";
import type { ProjetoUnifilarFormData } from "@/lib/validations/unifilar";

// ─── Shared fixtures ──────────────────────────────────────────────────────────

const placaForm = {
  marca_placa: "Canadian Solar",
  modelo_placa: "CS6R-420MS",
  potencia_placa: 420,
  tipo_celula: "Monocristalino",
  tensao_pico: 49.1,
  corrente_curtocircuito: 11.21,
  tensao_maxima_potencia: 41.3,
  corrente_maxima_potencia: 10.17,
  // id_placa and eficiencia_placa intentionally absent (undefined from form)
};

const inversorForm = {
  marca_inversor: "Growatt",
  modelo_inversor: "MIN 6000TL-X",
  potencia_inversor: 6000,
  numero_fases: "monofasico" as const,
  tipo_de_inversor: "string" as const,
  // id_inversor intentionally absent (undefined from form)
};

const sistemaForm = {
  inversor: inversorForm,
  quantidade_inversor: 1,
  quantidade_total_placas_do_sistema: { quantidade_placas: 12 },
  placa: placaForm,
};

const enderecoObraForm = {
  logradouro_obra: "Rua das Flores",
  numero_obra: "123",
  cep_obra: "60000-000",
  bairro_obra: "Centro",
  cidade_obra: "Fortaleza",
  estado_obra: "CE",
};

// ─── Memorial Descritivo ─────────────────────────────────────────────────────

const memorialFormData: ProjetoMemorialFormData = {
  numero_unidade_consumidora: "123456789",
  carga_instalada_kw: 5.5,
  disjuntor_geral_amperes: 40,
  energia_media_mensal_kwh: 350,
  classe_consumo1: "residencial",
  tipo_fornecimento: "monofasico",
  ramal_energia: "aereo",
  data_projeto: "2026-01-15",
  quantidade_sistemas_instalados: 1,
  sistema_instalado1: sistemaForm,
  // id_projeto, cliente, endereco_obra left undefined (as when user doesn't fill them)
};

describe("normalizeMemorialPayload — required-nullable fields", () => {
  it("id_projeto is null (not undefined/omitted) when not filled", () => {
    const payload = normalizeMemorialPayload(memorialFormData);
    expect("id_projeto" in payload).toBe(true);
    expect(payload.id_projeto).toBeNull();
  });

  it("cliente is null (not undefined/omitted) when not filled", () => {
    const payload = normalizeMemorialPayload(memorialFormData);
    expect("cliente" in payload).toBe(true);
    expect(payload.cliente).toBeNull();
  });

  it("endereco_obra is null (not undefined/omitted) when not filled", () => {
    const payload = normalizeMemorialPayload(memorialFormData);
    expect("endereco_obra" in payload).toBe(true);
    expect(payload.endereco_obra).toBeNull();
  });

  it("sistema_instalado1.inversor.id_inversor is null when not filled", () => {
    const payload = normalizeMemorialPayload(memorialFormData);
    expect("id_inversor" in payload.sistema_instalado1.inversor).toBe(true);
    expect(payload.sistema_instalado1.inversor.id_inversor).toBeNull();
  });

  it("sistema_instalado1.placa.id_placa is null when not filled", () => {
    const payload = normalizeMemorialPayload(memorialFormData);
    expect("id_placa" in payload.sistema_instalado1.placa).toBe(true);
    expect(payload.sistema_instalado1.placa.id_placa).toBeNull();
  });

  it("sistema_instalado1.placa.eficiencia_placa is null when not filled", () => {
    const payload = normalizeMemorialPayload(memorialFormData);
    expect("eficiencia_placa" in payload.sistema_instalado1.placa).toBe(true);
    expect(payload.sistema_instalado1.placa.eficiencia_placa).toBeNull();
  });
});

describe("normalizeMemorialPayload — value preservation", () => {
  it("preserves id_projeto when provided", () => {
    const payload = normalizeMemorialPayload({ ...memorialFormData, id_projeto: 42 });
    expect(payload.id_projeto).toBe(42);
  });

  it("preserves cliente object when provided", () => {
    const cliente = {
      nome_cliente: "João da Silva",
      cpf: "123.456.789-00",
      data_nascimento: "1990-01-01",
      rg: "1234567",
      telefone_cliente: "(85) 99999-9999",
      email_cliente: "joao@email.com",
    };
    const payload = normalizeMemorialPayload({ ...memorialFormData, cliente });
    expect(payload.cliente).toEqual(cliente);
  });

  it("preserves id_inversor when provided", () => {
    const data: ProjetoMemorialFormData = {
      ...memorialFormData,
      sistema_instalado1: {
        ...sistemaForm,
        inversor: { ...inversorForm, id_inversor: 7 },
      },
    };
    const payload = normalizeMemorialPayload(data);
    expect(payload.sistema_instalado1.inversor.id_inversor).toBe(7);
  });

  it("preserves core project fields unchanged", () => {
    const payload = normalizeMemorialPayload(memorialFormData);
    expect(payload.numero_unidade_consumidora).toBe("123456789");
    expect(payload.carga_instalada_kw).toBe(5.5);
    expect(payload.classe_consumo1).toBe("residencial");
    expect(payload.tipo_fornecimento).toBe("monofasico");
    expect(payload.ramal_energia).toBe("aereo");
  });
});

describe("normalizeMemorialPayload — multiple systems", () => {
  it("normalizes id fields in sistema_instalado2 when present", () => {
    const data: ProjetoMemorialFormData = {
      ...memorialFormData,
      quantidade_sistemas_instalados: 2,
      sistema_instalado2: sistemaForm,
    };
    const payload = normalizeMemorialPayload(data);
    expect(payload.sistema_instalado2).toBeDefined();
    expect(payload.sistema_instalado2!.inversor.id_inversor).toBeNull();
    expect(payload.sistema_instalado2!.placa.id_placa).toBeNull();
    expect(payload.sistema_instalado2!.placa.eficiencia_placa).toBeNull();
  });

  it("sistema_instalado2 is undefined (not null) when not provided", () => {
    // Backend has sistema_instalado2: ConfiguracaoSistema | None = None (with default)
    // so omitting it is fine — different from required-nullable fields.
    const payload = normalizeMemorialPayload(memorialFormData);
    expect(payload.sistema_instalado2).toBeUndefined();
  });
});

// ─── Procuração ───────────────────────────────────────────────────────────────

const procuracaoFormData: ProjetoProcuracaoFormData = {
  cliente: {
    nome_cliente: "João da Silva",
    cpf: "123.456.789-00",
    data_nascimento: "1990-01-01",
    rg: "1234567",
    telefone_cliente: "(85) 99999-9999",
    email_cliente: "joao@email.com",
  },
  endereco_cliente: {
    logradouro_cliente: "Rua das Flores",
    numero_casa_cliente: "123",
    cep_cliente: "60000-000",
    bairro_cliente: "Centro",
    cidade_cliente: "Fortaleza",
    estado_cliente: "CE",
  },
  endereco_obra: enderecoObraForm,
  procurador: {
    nome_procurador: "Maria Souza",
    cpf_procurador: "987.654.321-00",
    rg_procurador: "7654321",
    telefone_procurador: "(85) 88888-8888",
    email_procurador: "maria@email.com",
    logradouro_procurador: "Av. Principal",
    numero_casa_procurador: "789",
    cep_procurador: "60002-000",
    bairro_procurador: "Meireles",
    cidade_procurador: "Fortaleza",
    estado_procurador: "CE",
  },
  // id_projeto intentionally absent
};

describe("normalizeProcuracaoPayload — required-nullable fields", () => {
  it("id_projeto is null (not omitted) when not filled", () => {
    const payload = normalizeProcuracaoPayload(procuracaoFormData);
    expect("id_projeto" in payload).toBe(true);
    expect(payload.id_projeto).toBeNull();
  });

  it("preserves id_projeto when provided", () => {
    const payload = normalizeProcuracaoPayload({ ...procuracaoFormData, id_projeto: 99 });
    expect(payload.id_projeto).toBe(99);
  });
});

describe("normalizeProcuracaoPayload — value preservation", () => {
  it("preserves all client fields", () => {
    const payload = normalizeProcuracaoPayload(procuracaoFormData);
    expect(payload.cliente.nome_cliente).toBe("João da Silva");
    expect(payload.cliente.cpf).toBe("123.456.789-00");
  });

  it("preserves all procurador fields", () => {
    const payload = normalizeProcuracaoPayload(procuracaoFormData);
    expect(payload.procurador.nome_procurador).toBe("Maria Souza");
    expect(payload.procurador.cpf_procurador).toBe("987.654.321-00");
  });

  it("preserves endereco_obra", () => {
    const payload = normalizeProcuracaoPayload(procuracaoFormData);
    expect(payload.endereco_obra.logradouro_obra).toBe("Rua das Flores");
    expect(payload.endereco_obra.cidade_obra).toBe("Fortaleza");
  });
});

// ─── Diagrama Unifilar ────────────────────────────────────────────────────────

const unifilarFormData: ProjetoUnifilarFormData = {
  nome_projetista: "Eng. Carlos Lima",
  cft_crea_projetista: "CREA-CE 12345",
  nome_cliente: "João da Silva",
  quantidade_sistemas_instalados: 1,
  disjuntor_geral_amperes: 40,
  tensao_local: 220, // number after z.coerce — backend expects int
  endereco_obra: enderecoObraForm,
  sistema_instalado1: sistemaForm,
};

describe("normalizeUnifilarPayload — required-nullable fields", () => {
  it("sistema_instalado1.inversor.id_inversor is null when not filled", () => {
    const payload = normalizeUnifilarPayload(unifilarFormData);
    expect("id_inversor" in payload.sistema_instalado1.inversor).toBe(true);
    expect(payload.sistema_instalado1.inversor.id_inversor).toBeNull();
  });

  it("sistema_instalado1.placa.id_placa is null when not filled", () => {
    const payload = normalizeUnifilarPayload(unifilarFormData);
    expect("id_placa" in payload.sistema_instalado1.placa).toBe(true);
    expect(payload.sistema_instalado1.placa.id_placa).toBeNull();
  });

  it("sistema_instalado1.placa.eficiencia_placa is null when not filled", () => {
    const payload = normalizeUnifilarPayload(unifilarFormData);
    expect("eficiencia_placa" in payload.sistema_instalado1.placa).toBe(true);
    expect(payload.sistema_instalado1.placa.eficiencia_placa).toBeNull();
  });
});

describe("normalizeUnifilarPayload — type correctness", () => {
  it("tensao_local is a number (backend: int), not a string", () => {
    const payload = normalizeUnifilarPayload(unifilarFormData);
    expect(typeof payload.tensao_local).toBe("number");
    expect(payload.tensao_local).toBe(220);
  });

  it("disjuntor_geral_amperes is a number", () => {
    const payload = normalizeUnifilarPayload(unifilarFormData);
    expect(typeof payload.disjuntor_geral_amperes).toBe("number");
  });
});

describe("normalizeUnifilarPayload — value preservation and optional systems", () => {
  it("preserves projetista and client fields", () => {
    const payload = normalizeUnifilarPayload(unifilarFormData);
    expect(payload.nome_projetista).toBe("Eng. Carlos Lima");
    expect(payload.nome_cliente).toBe("João da Silva");
  });

  it("sistema_instalado2 is undefined when not provided", () => {
    const payload = normalizeUnifilarPayload(unifilarFormData);
    expect(payload.sistema_instalado2).toBeUndefined();
  });

  it("normalizes sistema_instalado2 when present", () => {
    const data: ProjetoUnifilarFormData = {
      ...unifilarFormData,
      quantidade_sistemas_instalados: 2,
      sistema_instalado2: sistemaForm,
    };
    const payload = normalizeUnifilarPayload(data);
    expect(payload.sistema_instalado2).toBeDefined();
    expect(payload.sistema_instalado2!.inversor.id_inversor).toBeNull();
    expect(payload.sistema_instalado2!.placa.id_placa).toBeNull();
  });
});
