import { z } from "zod";
import { enderecoObraSchema } from "./memorial";

const classeConsumoEnum = z.enum(
  ["residencial", "comercial", "industrial", "rural"],
  { errorMap: () => ({ message: "Selecione a classe de consumo" }) }
);

const ramalEnergiaEnum = z.enum(["aereo", "subterraneo"], {
  errorMap: () => ({ message: "Selecione o tipo de ramal" }),
});

export const projetoFormularioEnelCeSchema = z.object({
  numero_uc: z
    .string()
    .min(1, "Número da UC é obrigatório"),
  classe: classeConsumoEnum,
  ramal_energia: ramalEnergiaEnum,
  nome_cliente: z.string().min(1, "Nome do cliente é obrigatório"),
  cpf: z
    .string()
    .min(1, "CPF é obrigatório")
    .regex(/^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$/, "CPF inválido"),
  telefone_cliente: z.string().min(1, "Telefone é obrigatório"),
  email_cliente: z
    .string()
    .min(1, "E-mail é obrigatório")
    .email("E-mail inválido"),
  endereco_obra: enderecoObraSchema,
  // Backend: tensao_local: int — coerce string input to integer
  tensao_local: z.coerce
    .number({ invalid_type_error: "Tensão local é obrigatória" })
    .int("Tensão local deve ser um número inteiro")
    .positive("Tensão local deve ser positiva"),
  carga_instalada_kw: z
    .number({ invalid_type_error: "Carga instalada é obrigatória" })
    .positive("Carga instalada deve ser positiva"),
  potencia_geracao: z
    .number({ invalid_type_error: "Potência de geração é obrigatória" })
    .positive("Potência deve ser positiva"),
  nome_procurador: z.string().min(1, "Nome do procurador é obrigatório"),
  cpf_procurador: z
    .string()
    .min(1, "CPF do procurador é obrigatório")
    .regex(/^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$/, "CPF inválido"),
  email_procurador: z
    .string()
    .min(1, "E-mail do procurador é obrigatório")
    .email("E-mail inválido"),
  data_hoje: z.string().min(1, "Data é obrigatória"),
  telefone_procurador: z.string().min(1, "Telefone do procurador é obrigatório"),
});

export type ProjetoFormularioEnelCeFormData = z.infer<
  typeof projetoFormularioEnelCeSchema
>;
