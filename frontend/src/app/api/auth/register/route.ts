import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json() as {
      username?: string;
      email?: string;
      password?: string;
    };
    const { username, email, password } = body;

    if (!username || !email || !password) {
      return NextResponse.json(
        { error: "Todos os campos são obrigatórios" },
        { status: 400 }
      );
    }

    const backendResponse = await fetch(`${BACKEND_URL}/users/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    if (!backendResponse.ok) {
      const errorData = await backendResponse
        .json()
        .catch(() => ({})) as Record<string, unknown>;
      const detail = errorData.detail;
      let errorMessage: string;
      if (typeof detail === "string") {
        errorMessage = detail;
      } else if (Array.isArray(detail)) {
        errorMessage = (detail as Array<{ msg: string }>)
          .map((e) => e.msg)
          .join(", ");
      } else {
        errorMessage = "Erro ao criar conta";
      }
      return NextResponse.json(
        { error: errorMessage },
        { status: backendResponse.status }
      );
    }

    return NextResponse.json({ success: true }, { status: 201 });
  } catch {
    return NextResponse.json(
      { error: "Erro interno do servidor" },
      { status: 500 }
    );
  }
}
