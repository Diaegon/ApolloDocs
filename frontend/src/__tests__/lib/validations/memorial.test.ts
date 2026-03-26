import { describe, it, expect } from "vitest";
import {
  projetoMemorialSchema,
  clienteSchema,
  inversorSchema,
  placaSchema,
  configuracaoSistemaSchema,
} from "@/lib/validations/memorial";

const validPlaca = {
  marca_placa: "Canadian Solar",
  modelo_placa: "CS6R-420MS",
  potencia_placa: 420,
  tipo_celula: "Monocristalino",
  tensao_pico: 49.1,
  corrente_curtocircuito: 11.21,
  tensao_maxima_potencia: 41.3,
  corrente_maxima_potencia: 10.17,
};

const validInversor = {
  marca_inversor: "Growatt",
  modelo_inversor: "MIN 6000TL-X",
  potencia_inversor: 6000,
  numero_fases: "monofasico" as const,
  tipo_de_inversor: "string" as const,
};

const validSistema = {
  inversor: validInversor,
  quantidade_inversor: 1,
  quantidade_total_placas_do_sistema: { quantidade_placas: 12 },
  placa: validPlaca,
};

const validMemorial = {
  numero_unidade_consumidora: "123456789",
  carga_instalada_kw: 5.5,
  disjuntor_geral_amperes: 40,
  energia_media_mensal_kwh: 350,
  classe_consumo1: "residencial" as const,
  tipo_fornecimento: "monofasico" as const,
  ramal_energia: "aereo" as const,
  data_projeto: "2026-01-15",
  quantidade_sistemas_instalados: 1 as const,
  sistema_instalado1: validSistema,
};

describe("clienteSchema", () => {
  it("accepts valid client data", () => {
    const result = clienteSchema.safeParse({
      nome_cliente: "João da Silva",
      cpf: "123.456.789-00",
      data_nascimento: "1990-01-01",
      rg: "1234567",
      telefone_cliente: "(85) 99999-9999",
      email_cliente: "joao@email.com",
    });
    expect(result.success).toBe(true);
  });

  it("accepts CPF without formatting", () => {
    const result = clienteSchema.safeParse({
      nome_cliente: "João",
      cpf: "12345678900",
      data_nascimento: "1990-01-01",
      rg: "1234567",
      telefone_cliente: "(85) 99999-9999",
      email_cliente: "joao@email.com",
    });
    expect(result.success).toBe(true);
  });

  it("rejects invalid CPF format", () => {
    const result = clienteSchema.safeParse({
      nome_cliente: "João",
      cpf: "12345",
      data_nascimento: "1990-01-01",
      rg: "1234567",
      telefone_cliente: "(85) 99999-9999",
      email_cliente: "joao@email.com",
    });
    expect(result.success).toBe(false);
  });

  it("rejects invalid email", () => {
    const result = clienteSchema.safeParse({
      nome_cliente: "João",
      cpf: "123.456.789-00",
      data_nascimento: "1990-01-01",
      rg: "1234567",
      telefone_cliente: "(85) 99999-9999",
      email_cliente: "not-an-email",
    });
    expect(result.success).toBe(false);
  });
});

describe("inversorSchema", () => {
  it("accepts valid inversor", () => {
    expect(inversorSchema.safeParse(validInversor).success).toBe(true);
  });

  it("rejects zero potencia", () => {
    const result = inversorSchema.safeParse({
      ...validInversor,
      potencia_inversor: 0,
    });
    expect(result.success).toBe(false);
  });

  it("rejects invalid numero_fases", () => {
    const result = inversorSchema.safeParse({
      ...validInversor,
      numero_fases: "quadrifasico",
    });
    expect(result.success).toBe(false);
  });

  it("rejects invalid tipo_de_inversor", () => {
    const result = inversorSchema.safeParse({
      ...validInversor,
      tipo_de_inversor: "hibrido",
    });
    expect(result.success).toBe(false);
  });
});

describe("placaSchema", () => {
  it("accepts valid placa", () => {
    expect(placaSchema.safeParse(validPlaca).success).toBe(true);
  });

  it("rejects negative potencia", () => {
    const result = placaSchema.safeParse({
      ...validPlaca,
      potencia_placa: -100,
    });
    expect(result.success).toBe(false);
  });

  it("rejects missing marca_placa", () => {
    const result = placaSchema.safeParse({
      ...validPlaca,
      marca_placa: "",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toContain("obrigatória");
    }
  });
});

describe("configuracaoSistemaSchema", () => {
  it("accepts valid sistema configuration", () => {
    expect(configuracaoSistemaSchema.safeParse(validSistema).success).toBe(
      true
    );
  });

  it("rejects zero quantidade_inversor", () => {
    const result = configuracaoSistemaSchema.safeParse({
      ...validSistema,
      quantidade_inversor: 0,
    });
    expect(result.success).toBe(false);
  });
});

describe("projetoMemorialSchema", () => {
  it("accepts valid memorial data", () => {
    const result = projetoMemorialSchema.safeParse(validMemorial);
    expect(result.success).toBe(true);
  });

  it("rejects missing numero_unidade_consumidora", () => {
    const result = projetoMemorialSchema.safeParse({
      ...validMemorial,
      numero_unidade_consumidora: "",
    });
    expect(result.success).toBe(false);
  });

  it("rejects invalid classe_consumo1", () => {
    const result = projetoMemorialSchema.safeParse({
      ...validMemorial,
      classe_consumo1: "agricola",
    });
    expect(result.success).toBe(false);
  });

  it("rejects invalid ramal_energia", () => {
    const result = projetoMemorialSchema.safeParse({
      ...validMemorial,
      ramal_energia: "subterraneo_profundo",
    });
    expect(result.success).toBe(false);
  });

  it("accepts quantidade_sistemas_instalados of 1, 2, or 3", () => {
    for (const qty of [1, 2, 3] as const) {
      const result = projetoMemorialSchema.safeParse({
        ...validMemorial,
        quantidade_sistemas_instalados: qty,
      });
      expect(result.success).toBe(true);
    }
  });

  it("rejects quantidade_sistemas_instalados of 4", () => {
    const result = projetoMemorialSchema.safeParse({
      ...validMemorial,
      quantidade_sistemas_instalados: 4,
    });
    expect(result.success).toBe(false);
  });

  it("rejects negative carga_instalada_kw", () => {
    const result = projetoMemorialSchema.safeParse({
      ...validMemorial,
      carga_instalada_kw: -1,
    });
    expect(result.success).toBe(false);
  });
});
