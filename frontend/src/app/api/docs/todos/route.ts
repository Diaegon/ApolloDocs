import { NextRequest, NextResponse } from "next/server";
import { generateTodosDocumentos } from "@/lib/api/docs";
import type { ProjetoTodos } from "@/types/docs";

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json() as ProjetoTodos;
    const response = await generateTodosDocumentos(body);

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        { error: errorText || "Erro ao gerar Documentos" },
        { status: response.status }
      );
    }

    const fileBuffer = await response.arrayBuffer();

    return new NextResponse(fileBuffer, {
      status: 200,
      headers: {
        "Content-Type": "application/zip",
        "Content-Disposition":
          'attachment; filename="documentos.zip"',
      },
    });
  } catch (err) {
    console.error("Error generating todos:", err);
    return NextResponse.json(
      { error: "Erro interno ao gerar documentos" },
      { status: 500 }
    );
  }
}
