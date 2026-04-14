import { NextRequest, NextResponse } from "next/server";
import { generateDiagramaUnifilarV2 } from "@/lib/api/docs";
import type { ProjetoUnifilarV2 } from "@/types/docs";

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json() as ProjetoUnifilarV2;
    const pdfResponse = await generateDiagramaUnifilarV2(body);

    if (!pdfResponse.ok) {
      const errorText = await pdfResponse.text();
      return NextResponse.json(
        { error: errorText || "Erro ao gerar Diagrama Unifilar" },
        { status: pdfResponse.status }
      );
    }

    const pdfBuffer = await pdfResponse.arrayBuffer();

    return new NextResponse(pdfBuffer, {
      status: 200,
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": 'attachment; filename="diagrama_unifilar.pdf"',
      },
    });
  } catch (err) {
    console.error("Error generating unifilar:", err);
    return NextResponse.json(
      { error: "Erro interno ao gerar documento" },
      { status: 500 }
    );
  }
}
