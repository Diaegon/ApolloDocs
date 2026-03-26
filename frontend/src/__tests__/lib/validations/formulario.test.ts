import { describe, it, expect } from "vitest";
import { projetoFormularioEnelCeSchema } from "@/lib/validations/formulario";

const validFormulario = {
  numero_uc: "123456789",
  classe: "residencial" as const,
  ramal_energia: "aereo" as const,
  nome_cliente: "João da Silva",
  cpf: "123.456.789-00",
  telefone_cliente: "(85) 99999-9999",
  email_cliente: "joao@email.com",
  endereco_obra: {
    logradouro_obra: "Rua das Flores",
    numero_obra: "123",
    cep_obra: "60000-000",
    bairro_obra: "Centro",
    cidade_obra: "Fortaleza",
    estado_obra: "CE",
  },
  tensao_local: 220, // backend: int, not string
  carga_instalada_kw: 5.5,
  potencia_geracao: 5.04,
  nome_procurador: "Maria Souza",
  cpf_procurador: "987.654.321-00",
  email_procurador: "maria@email.com",
  data_hoje: "2026-03-10",
  telefone_procurador: "(85) 98888-8888",
};

describe("projetoFormularioEnelCeSchema", () => {
  it("accepts valid formulario data", () => {
    expect(projetoFormularioEnelCeSchema.safeParse(validFormulario).success).toBe(true);
  });

  it("rejects missing numero_uc", () => {
    const result = projetoFormularioEnelCeSchema.safeParse({
      ...validFormulario,
      numero_uc: "",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      const err = result.error.issues.find((i) =>
        i.path.includes("numero_uc")
      );
      expect(err?.message).toContain("obrigatório");
    }
  });

  it("rejects invalid classe", () => {
    const result = projetoFormularioEnelCeSchema.safeParse({
      ...validFormulario,
      classe: "agricola",
    });
    expect(result.success).toBe(false);
  });

  it("rejects invalid ramal_energia", () => {
    const result = projetoFormularioEnelCeSchema.safeParse({
      ...validFormulario,
      ramal_energia: "subterraneo_profundo",
    });
    expect(result.success).toBe(false);
  });

  it("rejects invalid client email", () => {
    const result = projetoFormularioEnelCeSchema.safeParse({
      ...validFormulario,
      email_cliente: "not-an-email",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues.some((i) => i.message === "E-mail inválido")).toBe(true);
    }
  });

  it("rejects invalid procurador email", () => {
    const result = projetoFormularioEnelCeSchema.safeParse({
      ...validFormulario,
      email_procurador: "invalid",
    });
    expect(result.success).toBe(false);
  });

  it("rejects negative potencia_geracao", () => {
    const result = projetoFormularioEnelCeSchema.safeParse({
      ...validFormulario,
      potencia_geracao: -1,
    });
    expect(result.success).toBe(false);
  });

  it("accepts all valid classe values", () => {
    for (const classe of ["residencial", "comercial", "industrial", "rural"] as const) {
      const result = projetoFormularioEnelCeSchema.safeParse({
        ...validFormulario,
        classe,
      });
      expect(result.success).toBe(true);
    }
  });

  it("accepts all valid ramal values", () => {
    for (const ramal of ["aereo", "subterraneo"] as const) {
      const result = projetoFormularioEnelCeSchema.safeParse({
        ...validFormulario,
        ramal_energia: ramal,
      });
      expect(result.success).toBe(true);
    }
  });
});
