import { describe, it, expect } from "vitest";
import { projetoUnifilarSchema } from "@/lib/validations/unifilar";

const validSistema = {
  inversor: {
    marca_inversor: "Growatt",
    modelo_inversor: "MIN 6000TL-X",
    potencia_inversor: 6000,
    numero_fases: "monofasico" as const,
    tipo_de_inversor: "string" as const,
  },
  quantidade_inversor: 1,
  quantidade_total_placas_do_sistema: { quantidade_placas: 12 },
  placa: {
    marca_placa: "Canadian Solar",
    modelo_placa: "CS6R-420MS",
    potencia_placa: 420,
    tipo_celula: "Monocristalino",
    tensao_pico: 49.1,
    corrente_curtocircuito: 11.21,
    tensao_maxima_potencia: 41.3,
    corrente_maxima_potencia: 10.17,
  },
};

const validUnifilar = {
  nome_projetista: "Eng. Carlos Lima",
  cft_crea_projetista: "CREA-CE 12345",
  nome_cliente: "João da Silva",
  quantidade_sistemas_instalados: 1 as const,
  disjuntor_geral_amperes: 40,
  tensao_local: 220, // backend: int, not string
  endereco_obra: {
    logradouro_obra: "Rua das Flores",
    numero_obra: "123",
    cep_obra: "60000-000",
    bairro_obra: "Centro",
    cidade_obra: "Fortaleza",
    estado_obra: "CE",
  },
  sistema_instalado1: validSistema,
};

describe("projetoUnifilarSchema", () => {
  it("accepts valid unifilar data", () => {
    expect(projetoUnifilarSchema.safeParse(validUnifilar).success).toBe(true);
  });

  it("rejects missing nome_projetista", () => {
    const result = projetoUnifilarSchema.safeParse({
      ...validUnifilar,
      nome_projetista: "",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      const err = result.error.issues.find((i) =>
        i.path.includes("nome_projetista")
      );
      expect(err?.message).toContain("obrigatório");
    }
  });

  it("rejects missing cft_crea_projetista", () => {
    const result = projetoUnifilarSchema.safeParse({
      ...validUnifilar,
      cft_crea_projetista: "",
    });
    expect(result.success).toBe(false);
  });

  it("accepts 2 systems", () => {
    const result = projetoUnifilarSchema.safeParse({
      ...validUnifilar,
      quantidade_sistemas_instalados: 2,
      sistema_instalado2: validSistema,
    });
    expect(result.success).toBe(true);
  });

  it("accepts 3 systems", () => {
    const result = projetoUnifilarSchema.safeParse({
      ...validUnifilar,
      quantidade_sistemas_instalados: 3,
      sistema_instalado2: validSistema,
      sistema_instalado3: validSistema,
    });
    expect(result.success).toBe(true);
  });

  it("rejects invalid quantidade_sistemas_instalados", () => {
    const result = projetoUnifilarSchema.safeParse({
      ...validUnifilar,
      quantidade_sistemas_instalados: 5,
    });
    expect(result.success).toBe(false);
  });

  it("rejects negative disjuntor_geral_amperes", () => {
    const result = projetoUnifilarSchema.safeParse({
      ...validUnifilar,
      disjuntor_geral_amperes: -10,
    });
    expect(result.success).toBe(false);
  });
});
