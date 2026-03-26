import { z } from "zod";
import { clienteSchema, enderecoObraSchema } from "./memorial";

export const enderecoClienteSchema = z.object({
  logradouro_cliente: z.string().min(1, "Logradouro é obrigatório"),
  numero_casa_cliente: z.string().min(1, "Número é obrigatório"),
  complemento_casa_cliente: z.string().optional(),
  cep_cliente: z
    .string()
    .min(1, "CEP é obrigatório")
    .regex(/^\d{5}-?\d{3}$/, "CEP inválido"),
  bairro_cliente: z.string().min(1, "Bairro é obrigatório"),
  cidade_cliente: z.string().min(1, "Cidade é obrigatória"),
  estado_cliente: z
    .string()
    .min(2, "Estado é obrigatório")
    .max(2, "Use a sigla do estado (ex: CE)"),
});

export const procuradorSchema = z.object({
  id_procurador: z.number().optional(),
  nome_procurador: z.string().min(1, "Nome do procurador é obrigatório"),
  cpf_procurador: z
    .string()
    .min(1, "CPF do procurador é obrigatório")
    .regex(/^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$/, "CPF inválido"),
  rg_procurador: z.string().min(1, "RG do procurador é obrigatório"),
  telefone_procurador: z.string().min(1, "Telefone do procurador é obrigatório"),
  email_procurador: z
    .string()
    .min(1, "E-mail do procurador é obrigatório")
    .email("E-mail inválido"),
  logradouro_procurador: z.string().min(1, "Logradouro é obrigatório"),
  numero_casa_procurador: z.string().min(1, "Número é obrigatório"),
  complemento_procurador: z.string().optional(),
  cep_procurador: z
    .string()
    .min(1, "CEP é obrigatório")
    .regex(/^\d{5}-?\d{3}$/, "CEP inválido"),
  bairro_procurador: z.string().min(1, "Bairro é obrigatório"),
  cidade_procurador: z.string().min(1, "Cidade é obrigatória"),
  estado_procurador: z
    .string()
    .min(2, "Estado é obrigatório")
    .max(2, "Use a sigla do estado (ex: CE)"),
});

export const projetoProcuracaoSchema = z.object({
  id_projeto: z.number().optional(),
  cliente: clienteSchema,
  endereco_cliente: enderecoClienteSchema,
  endereco_obra: enderecoObraSchema,
  procurador: procuradorSchema,
});

export type ProjetoProcuracaoFormData = z.infer<typeof projetoProcuracaoSchema>;
