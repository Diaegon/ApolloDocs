import { NextRequest, NextResponse } from "next/server";
import { generateProcuracao } from "@/lib/api/docs";
import type { ProjetoProcuracao } from "@/types/docs";

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json() as ProjetoProcuracao;
    const pdfResponse = await generateProcuracao(body);

    if (!pdfResponse.ok) {
      const errorText = await pdfResponse.text();
      return NextResponse.json(
        { error: errorText || "Erro ao gerar Procuração" },
        { status: pdfResponse.status }
      );
    }

    const pdfBuffer = await pdfResponse.arrayBuffer();

    return new NextResponse(pdfBuffer, {
      status: 200,
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": 'attachment; filename="procuracao.pdf"',
      },
    });
  } catch (err) {
    console.error("Error generating procuracao:", err);
    return NextResponse.json(
      { error: "Erro interno ao gerar documento" },
      { status: 500 }
    );
  }
}
