import { NextRequest, NextResponse } from "next/server";
import { generateFormularioEnel } from "@/lib/api/docs";
import type { ProjetoFormularioEnelCe } from "@/types/docs";

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json() as ProjetoFormularioEnelCe;
    const pdfResponse = await generateFormularioEnel(body);

    if (!pdfResponse.ok) {
      const errorText = await pdfResponse.text();
      return NextResponse.json(
        { error: errorText || "Erro ao gerar Formulário ENEL-CE" },
        { status: pdfResponse.status }
      );
    }

    const pdfBuffer = await pdfResponse.arrayBuffer();

    return new NextResponse(pdfBuffer, {
      status: 200,
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": 'attachment; filename="formulario_enel_ce.pdf"',
      },
    });
  } catch (err) {
    console.error("Error generating formulario:", err);
    return NextResponse.json(
      { error: "Erro interno ao gerar documento" },
      { status: 500 }
    );
  }
}
