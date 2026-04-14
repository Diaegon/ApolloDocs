import { z } from "zod";
import { enderecoObraSchema, configuracaoSistemaSchema } from "./memorial";

export const projetoUnifilarSchema = z.object({
  nome_projetista: z.string().min(1, "Nome do projetista é obrigatório"),
  cft_crea_projetista: z
    .string()
    .min(1, "CFT/CREA do projetista é obrigatório"),
  nome_cliente: z.string().min(1, "Nome do cliente é obrigatório"),
  quantidade_sistemas_instalados: z.union([
    z.literal(1),
    z.literal(2),
    z.literal(3),
  ]),
  disjuntor_geral_amperes: z
    .number({ invalid_type_error: "Disjuntor geral é obrigatório" })
    .positive("Disjuntor deve ser positivo"),
  // Backend: tensao_local: int — coerce string input to integer
  tensao_local: z.coerce
    .number({ invalid_type_error: "Tensão local é obrigatória" })
    .int("Tensão local deve ser um número inteiro")
    .positive("Tensão local deve ser positiva"),
  endereco_obra: enderecoObraSchema,
  sistema_instalado1: configuracaoSistemaSchema,
  sistema_instalado2: configuracaoSistemaSchema.optional(),
  sistema_instalado3: configuracaoSistemaSchema.optional(),
});

export type ProjetoUnifilarFormData = z.infer<typeof projetoUnifilarSchema>;

// ─── v2 schemas (catalog-driven, same flat shape as memorial v2) ─────────────
// Import and re-export from memorial so the two forms share the same ref schemas.
export { materialInversorRefSchema, materialPlacaRefSchema } from "./memorial";
import { materialInversorRefSchema, materialPlacaRefSchema } from "./memorial";

export const projetoUnifilarV2Schema = z
  .object({
    nome_projetista: z.string().min(1, "Nome do projetista é obrigatório"),
    cft_crea_projetista: z
      .string()
      .min(1, "CFT/CREA do projetista é obrigatório"),
    nome_cliente: z.string().min(1, "Nome do cliente é obrigatório"),
    disjuntor_geral_amperes: z
      .number({ invalid_type_error: "Disjuntor geral é obrigatório" })
      .positive("Disjuntor deve ser positivo"),
    tensao_local: z.coerce
      .number({ invalid_type_error: "Tensão local é obrigatória" })
      .int("Tensão local deve ser um número inteiro")
      .positive("Tensão local deve ser positiva"),
    endereco_obra: enderecoObraSchema,
    inversores: z
      .array(materialInversorRefSchema)
      .min(1, "Adicione ao menos um inversor")
      .max(3),
    placas: z
      .array(materialPlacaRefSchema)
      .min(1, "Adicione ao menos um módulo")
      .max(3),
  })
  .refine((d) => d.inversores.length === d.placas.length, {
    message: "A quantidade de inversores e módulos deve ser igual",
    path: ["placas"],
  });

export type ProjetoUnifilarV2FormData = z.infer<typeof projetoUnifilarV2Schema>;
