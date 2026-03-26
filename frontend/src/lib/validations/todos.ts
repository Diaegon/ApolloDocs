import { z } from "zod";
import {
  clienteSchema,
  enderecoObraSchema,
  configuracaoSistemaSchema,
} from "./memorial";
import { enderecoClienteSchema, procuradorSchema } from "./procuracao";

export const projetoTodosSchema = z.object({
  id_projeto: z.number().optional(),
  nome_projetista: z.string().min(1, "Nome do projetista é obrigatório"),
  cft_crea_projetista: z.string().min(1, "CFT/CREA do projetista é obrigatório"),
  cliente: clienteSchema,
  endereco_cliente: enderecoClienteSchema,
  endereco_obra: enderecoObraSchema,
  procurador: procuradorSchema,
  numero_unidade_consumidora: z.string().min(1, "Número da UC é obrigatório"),
  carga_instalada_kw: z.number({ invalid_type_error: "Carga instalada é obrigatória" }).positive("Deve ser positiva"),
  disjuntor_geral_amperes: z.number({ invalid_type_error: "Disjuntor geral é obrigatório" }).positive("Deve ser positivo"),
  energia_media_mensal_kwh: z.number({ invalid_type_error: "Energia média é obrigatória" }).positive("Deve ser positiva"),
  classe_consumo: z.enum(["residencial", "comercial", "industrial", "rural"], { errorMap: () => ({ message: "Selecione a classe de consumo" }) }),
  tipo_fornecimento: z.enum(["monofasico", "bifasico", "trifasico"], { errorMap: () => ({ message: "Selecione o tipo de fornecimento" }) }),
  ramal_energia: z.enum(["aereo", "subterraneo"], { errorMap: () => ({ message: "Selecione o tipo de ramal" }) }),
  tensao_local: z.coerce.number({ invalid_type_error: "Tensão local é obrigatória" }).int("Deve ser número inteiro").positive("Deve ser positiva"),
  potencia_geracao: z.coerce.number({ invalid_type_error: "Potência de geração é obrigatória" }).positive("Deve ser positiva"),
  data_projeto: z.string().min(1, "Data do projeto é obrigatória"),
  quantidade_sistemas_instalados: z.union([z.literal(1), z.literal(2), z.literal(3)]),
  sistema_instalado1: configuracaoSistemaSchema,
  sistema_instalado2: configuracaoSistemaSchema.optional(),
  sistema_instalado3: configuracaoSistemaSchema.optional(),
});

export type ProjetoTodosFormData = z.infer<typeof projetoTodosSchema>;
