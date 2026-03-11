import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";
const IS_PRODUCTION = process.env.NODE_ENV === "production";

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json() as { email?: string; password?: string };
    const { email, password } = body;

    if (!email || !password) {
      return NextResponse.json(
        { error: "E-mail e senha são obrigatórios" },
        { status: 400 }
      );
    }

    // Forward to FastAPI as form-urlencoded
    const formData = new URLSearchParams();
    formData.set("username", email);
    formData.set("password", password);

    const backendResponse = await fetch(`${BACKEND_URL}/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData.toString(),
    });

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({})) as Record<string, unknown>;
      return NextResponse.json(
        { error: (errorData.detail as string) ?? "Credenciais inválidas" },
        { status: 401 }
      );
    }

    const tokenData = await backendResponse.json() as {
      access_token: string;
      token_type: string;
    };

    const response = NextResponse.json({ success: true });

    // Set httpOnly cookie — JWT never exposed to client JS
    response.cookies.set("apollo_token", tokenData.access_token, {
      httpOnly: true,
      secure: IS_PRODUCTION,
      sameSite: "strict",
      path: "/",
      // 8 hours
      maxAge: 60 * 60 * 8,
    });

    return response;
  } catch {
    return NextResponse.json(
      { error: "Erro interno do servidor" },
      { status: 500 }
    );
  }
}
