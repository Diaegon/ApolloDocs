import { describe, it, expect } from "vitest";
import {
  projetoProcuracaoSchema,
  enderecoClienteSchema,
  procuradorSchema,
} from "@/lib/validations/procuracao";

const validEndereco = {
  logradouro_cliente: "Rua das Flores",
  numero_casa_cliente: "123",
  cep_cliente: "60000-000",
  bairro_cliente: "Centro",
  cidade_cliente: "Fortaleza",
  estado_cliente: "CE",
};

const validProcurador = {
  nome_procurador: "Maria Souza",
  cpf_procurador: "987.654.321-00",
  rg_procurador: "9876543",
  telefone_procurador: "(85) 98888-8888",
  email_procurador: "maria@email.com",
  logradouro_procurador: "Av. Beira Mar",
  numero_casa_procurador: "456",
  cep_procurador: "60165-121",
  bairro_procurador: "Meireles",
  cidade_procurador: "Fortaleza",
  estado_procurador: "CE",
};

const validCliente = {
  nome_cliente: "João da Silva",
  cpf: "123.456.789-00",
  data_nascimento: "1990-01-01",
  rg: "1234567",
  telefone_cliente: "(85) 99999-9999",
  email_cliente: "joao@email.com",
};

const validEnderecoObra = {
  logradouro_obra: "Rua das Palmeiras",
  numero_obra: "789",
  cep_obra: "60000-001",
  bairro_obra: "Aldeota",
  cidade_obra: "Fortaleza",
  estado_obra: "CE",
};

describe("enderecoClienteSchema", () => {
  it("accepts valid address", () => {
    expect(enderecoClienteSchema.safeParse(validEndereco).success).toBe(true);
  });

  it("accepts address with optional complemento", () => {
    const result = enderecoClienteSchema.safeParse({
      ...validEndereco,
      complemento_casa_cliente: "Apt 10",
    });
    expect(result.success).toBe(true);
  });

  it("rejects invalid CEP", () => {
    const result = enderecoClienteSchema.safeParse({
      ...validEndereco,
      cep_cliente: "1234",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toContain("CEP inválido");
    }
  });

  it("rejects missing cidade", () => {
    const result = enderecoClienteSchema.safeParse({
      ...validEndereco,
      cidade_cliente: "",
    });
    expect(result.success).toBe(false);
  });
});

describe("procuradorSchema", () => {
  it("accepts valid procurador", () => {
    expect(procuradorSchema.safeParse(validProcurador).success).toBe(true);
  });

  it("rejects invalid email", () => {
    const result = procuradorSchema.safeParse({
      ...validProcurador,
      email_procurador: "not-email",
    });
    expect(result.success).toBe(false);
  });

  it("rejects missing nome_procurador", () => {
    const result = procuradorSchema.safeParse({
      ...validProcurador,
      nome_procurador: "",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toContain("obrigatório");
    }
  });
});

describe("projetoProcuracaoSchema", () => {
  const validProcuracao = {
    cliente: validCliente,
    endereco_cliente: validEndereco,
    endereco_obra: validEnderecoObra,
    procurador: validProcurador,
  };

  it("accepts valid procuracao data", () => {
    expect(projetoProcuracaoSchema.safeParse(validProcuracao).success).toBe(
      true
    );
  });

  it("accepts optional id_projeto", () => {
    const result = projetoProcuracaoSchema.safeParse({
      ...validProcuracao,
      id_projeto: 42,
    });
    expect(result.success).toBe(true);
  });

  it("rejects missing cliente", () => {
    const { cliente, ...rest } = validProcuracao;
    const result = projetoProcuracaoSchema.safeParse(rest);
    expect(result.success).toBe(false);
  });

  it("rejects missing procurador", () => {
    const { procurador, ...rest } = validProcuracao;
    const result = projetoProcuracaoSchema.safeParse(rest);
    expect(result.success).toBe(false);
  });
});
