import { z } from "zod";

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, "E-mail é obrigatório")
    .email("E-mail inválido"),
  password: z
    .string()
    .min(1, "Senha é obrigatória")
    .min(6, "Senha deve ter pelo menos 6 caracteres"),
});

export const registerSchema = z
  .object({
    username: z
      .string()
      .min(1, "Nome de usuário é obrigatório")
      .min(3, "Nome de usuário deve ter pelo menos 3 caracteres")
      .max(50, "Nome de usuário deve ter no máximo 50 caracteres")
      .regex(
        /^[a-zA-Z0-9_]+$/,
        "Nome de usuário deve conter apenas letras, números e _"
      ),
    email: z
      .string()
      .min(1, "E-mail é obrigatório")
      .email("E-mail inválido"),
    password: z
      .string()
      .min(1, "Senha é obrigatória")
      .min(6, "Senha deve ter pelo menos 6 caracteres"),
    confirmPassword: z
      .string()
      .min(1, "Confirmação de senha é obrigatória"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "As senhas não coincidem",
    path: ["confirmPassword"],
  });

export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;
