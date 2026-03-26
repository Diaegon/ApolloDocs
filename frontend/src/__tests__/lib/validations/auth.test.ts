import { describe, it, expect } from "vitest";
import { loginSchema, registerSchema } from "@/lib/validations/auth";

describe("loginSchema", () => {
  it("accepts valid credentials", () => {
    const result = loginSchema.safeParse({
      email: "user@example.com",
      password: "senha123",
    });
    expect(result.success).toBe(true);
  });

  it("rejects missing email", () => {
    const result = loginSchema.safeParse({ email: "", password: "senha123" });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe("E-mail é obrigatório");
    }
  });

  it("rejects invalid email format", () => {
    const result = loginSchema.safeParse({
      email: "not-an-email",
      password: "senha123",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe("E-mail inválido");
    }
  });

  it("rejects missing password", () => {
    const result = loginSchema.safeParse({
      email: "user@example.com",
      password: "",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe("Senha é obrigatória");
    }
  });

  it("rejects password shorter than 6 characters", () => {
    const result = loginSchema.safeParse({
      email: "user@example.com",
      password: "12345",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toContain("6 caracteres");
    }
  });
});

describe("registerSchema", () => {
  const validData = {
    username: "meu_usuario",
    email: "user@example.com",
    password: "senha123",
    confirmPassword: "senha123",
  };

  it("accepts valid registration data", () => {
    const result = registerSchema.safeParse(validData);
    expect(result.success).toBe(true);
  });

  it("rejects username shorter than 3 characters", () => {
    const result = registerSchema.safeParse({ ...validData, username: "ab" });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toContain("3 caracteres");
    }
  });

  it("rejects username with special characters", () => {
    const result = registerSchema.safeParse({
      ...validData,
      username: "user@name",
    });
    expect(result.success).toBe(false);
  });

  it("rejects when passwords do not match", () => {
    const result = registerSchema.safeParse({
      ...validData,
      confirmPassword: "different",
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      const confirmError = result.error.issues.find(
        (i) => i.path[0] === "confirmPassword"
      );
      expect(confirmError?.message).toBe("As senhas não coincidem");
    }
  });

  it("rejects empty email", () => {
    const result = registerSchema.safeParse({ ...validData, email: "" });
    expect(result.success).toBe(false);
  });
});
