"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { registerSchema, type RegisterFormData } from "@/lib/validations/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FormField } from "@/components/ui/form-field";
import { Card, CardContent } from "@/components/ui/card";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function RegisterPage() {
  const router = useRouter();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  async function onSubmit(data: RegisterFormData) {
    setServerError(null);

    // Register directly to the backend (user creation doesn't require auth)
    const response = await fetch(`${BACKEND_URL}/users/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: data.username,
        email: data.email,
        password: data.password,
      }),
    });

    if (response.ok) {
      // Auto-login after registration
      const loginResponse = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: data.email, password: data.password }),
      });

      if (loginResponse.ok) {
        router.push("/dashboard");
        router.refresh();
      } else {
        router.push("/login");
      }
    } else {
      const body = await response.json().catch(() => ({})) as { detail?: string | { msg: string }[] };
      if (typeof body.detail === "string") {
        setServerError(body.detail);
      } else if (Array.isArray(body.detail)) {
        setServerError(body.detail.map((e) => e.msg).join(", "));
      } else {
        setServerError("Erro ao criar conta. Tente novamente.");
      }
    }
  }

  return (
    <Card>
      <CardContent className="pt-6">
        <h2 className="mb-6 text-xl font-semibold text-gray-900">
          Criar conta
        </h2>

        <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
          <FormField
            label="Nome de usuário"
            htmlFor="username"
            error={errors.username?.message}
            required
          >
            <Input
              id="username"
              type="text"
              autoComplete="username"
              placeholder="meu_usuario"
              error={errors.username?.message}
              {...register("username")}
            />
          </FormField>

          <FormField
            label="E-mail"
            htmlFor="email"
            error={errors.email?.message}
            required
          >
            <Input
              id="email"
              type="email"
              autoComplete="email"
              placeholder="seu@email.com"
              error={errors.email?.message}
              {...register("email")}
            />
          </FormField>

          <FormField
            label="Senha"
            htmlFor="password"
            error={errors.password?.message}
            required
          >
            <Input
              id="password"
              type="password"
              autoComplete="new-password"
              placeholder="••••••••"
              error={errors.password?.message}
              {...register("password")}
            />
          </FormField>

          <FormField
            label="Confirmar senha"
            htmlFor="confirmPassword"
            error={errors.confirmPassword?.message}
            required
          >
            <Input
              id="confirmPassword"
              type="password"
              autoComplete="new-password"
              placeholder="••••••••"
              error={errors.confirmPassword?.message}
              {...register("confirmPassword")}
            />
          </FormField>

          {serverError && (
            <div
              className="rounded-md bg-red-50 p-3 text-sm text-red-700"
              role="alert"
            >
              {serverError}
            </div>
          )}

          <Button
            type="submit"
            className="w-full"
            isLoading={isSubmitting}
          >
            Criar conta
          </Button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-500">
          Já tem uma conta?{" "}
          <Link
            href="/login"
            className="font-medium text-primary-600 hover:text-primary-700"
          >
            Entrar
          </Link>
        </p>
      </CardContent>
    </Card>
  );
}
