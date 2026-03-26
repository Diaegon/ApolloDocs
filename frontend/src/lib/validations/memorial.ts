import { z } from "zod";

const numeroFasesEnum = z.enum(["monofasico", "bifasico", "trifasico"], {
  errorMap: () => ({ message: "Selecione o número de fases" }),
});

const tipoInversorEnum = z.enum(["string", "micro"], {
  errorMap: () => ({ message: "Selecione o tipo de inversor" }),
});

const classeConsumoEnum = z.enum(
  ["residencial", "comercial", "industrial", "rural"],
  { errorMap: () => ({ message: "Selecione a classe de consumo" }) }
);

const tipoFornecimentoEnum = z.enum(["monofasico", "bifasico", "trifasico"], {
  errorMap: () => ({ message: "Selecione o tipo de fornecimento" }),
});

const ramalEnergiaEnum = z.enum(["aereo", "subterraneo"], {
  errorMap: () => ({ message: "Selecione o tipo de ramal" }),
});

export const clienteSchema = z.object({
  id_cliente: z.number().optional(),
  nome_cliente: z.string().min(1, "Nome do cliente é obrigatório"),
  cpf: z
    .string()
    .min(1, "CPF é obrigatório")
    .regex(/^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$/, "CPF inválido"),
  data_nascimento: z.string().min(1, "Data de nascimento é obrigatória"),
  razao_social: z.string().optional(),
  nome_fantasia: z.string().optional(),
  cnpj: z.string().optional(),
  rg: z.string().min(1, "RG é obrigatório"),
  telefone_cliente: z.string().min(1, "Telefone é obrigatório"),
  email_cliente: z
    .string()
    .min(1, "E-mail é obrigatório")
    .email("E-mail inválido"),
});

export const enderecoObraSchema = z.object({
  logradouro_obra: z.string().min(1, "Logradouro é obrigatório"),
  numero_obra: z.string().min(1, "Número é obrigatório"),
  complemento_obra: z.string().optional(),
  cep_obra: z
    .string()
    .min(1, "CEP é obrigatório")
    .regex(/^\d{5}-?\d{3}$/, "CEP inválido"),
  bairro_obra: z.string().min(1, "Bairro é obrigatório"),
  cidade_obra: z.string().min(1, "Cidade é obrigatória"),
  estado_obra: z
    .string()
    .min(2, "Estado é obrigatório")
    .max(2, "Use a sigla do estado (ex: CE)"),
  // Backend: str | None — must be string if provided
  latitude_obra: z.string().optional(),
  longitude_obra: z.string().optional(),
});

export const inversorSchema = z.object({
  id_inversor: z.number().optional(),
  marca_inversor: z.string().min(1, "Marca do inversor é obrigatória"),
  modelo_inversor: z.string().min(1, "Modelo do inversor é obrigatório"),
  potencia_inversor: z
    .number({ invalid_type_error: "Potência do inversor é obrigatória" })
    .positive("Potência deve ser positiva"),
  numero_fases: numeroFasesEnum,
  tipo_de_inversor: tipoInversorEnum,
  numero_mppt: z.number().optional(),
});

export const placaSchema = z.object({
  id_placa: z.number().optional(),
  marca_placa: z.string().min(1, "Marca da placa é obrigatória"),
  modelo_placa: z.string().min(1, "Modelo da placa é obrigatório"),
  potencia_placa: z
    .number({ invalid_type_error: "Potência da placa é obrigatória" })
    .positive("Potência deve ser positiva"),
  tipo_celula: z.string().min(1, "Tipo de célula é obrigatório"),
  tensao_pico: z
    .number({ invalid_type_error: "Tensão de pico é obrigatória" })
    .positive("Tensão deve ser positiva"),
  corrente_curtocircuito: z
    .number({ invalid_type_error: "Corrente de curto-circuito é obrigatória" })
    .positive("Corrente deve ser positiva"),
  tensao_maxima_potencia: z
    .number({ invalid_type_error: "Tensão de máxima potência é obrigatória" })
    .positive("Tensão deve ser positiva"),
  corrente_maxima_potencia: z
    .number({ invalid_type_error: "Corrente de máxima potência é obrigatória" })
    .positive("Corrente deve ser positiva"),
  eficiencia_placa: z.number().optional(),
});

export const quantidadePlacasSchema = z.object({
  quantidade_placas: z
    .number({ invalid_type_error: "Quantidade de placas é obrigatória" })
    .int("Deve ser um número inteiro")
    .positive("Deve ser positivo"),
  quantidade_placas2: z.number().optional(),
});

export const configuracaoSistemaSchema = z.object({
  inversor: inversorSchema,
  quantidade_inversor: z
    .number({ invalid_type_error: "Quantidade de inversores é obrigatória" })
    .int("Deve ser um número inteiro")
    .positive("Deve ser positivo"),
  quantidade_total_placas_do_sistema: quantidadePlacasSchema,
  placa: placaSchema,
  placa2: placaSchema.optional(),
});

export const projetoMemorialSchema = z.object({
  id_projeto: z.number().optional(),
  cliente: clienteSchema.optional(),
  endereco_obra: enderecoObraSchema.optional(),
  numero_unidade_consumidora: z
    .string()
    .min(1, "Número da unidade consumidora é obrigatório"),
  carga_instalada_kw: z
    .number({ invalid_type_error: "Carga instalada é obrigatória" })
    .positive("Carga instalada deve ser positiva"),
  disjuntor_geral_amperes: z
    .number({ invalid_type_error: "Disjuntor geral é obrigatório" })
    .positive("Disjuntor deve ser positivo"),
  energia_media_mensal_kwh: z
    .number({ invalid_type_error: "Energia média mensal é obrigatória" })
    .positive("Energia média deve ser positiva"),
  classe_consumo1: classeConsumoEnum,
  tipo_fornecimento: tipoFornecimentoEnum,
  ramal_energia: ramalEnergiaEnum,
  data_projeto: z.string().min(1, "Data do projeto é obrigatória"),
  quantidade_sistemas_instalados: z.union([
    z.literal(1),
    z.literal(2),
    z.literal(3),
  ]),
  sistema_instalado1: configuracaoSistemaSchema,
  sistema_instalado2: configuracaoSistemaSchema.optional(),
  sistema_instalado3: configuracaoSistemaSchema.optional(),
});

export type ProjetoMemorialFormData = z.infer<typeof projetoMemorialSchema>;
