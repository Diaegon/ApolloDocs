import { NextRequest, NextResponse } from "next/server";
import { generateMemorialDescritivo } from "@/lib/api/docs";
import type { ProjetoMemorial } from "@/types/docs";

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json() as ProjetoMemorial;
    const pdfResponse = await generateMemorialDescritivo(body);

    if (!pdfResponse.ok) {
      const errorText = await pdfResponse.text();
      return NextResponse.json(
        { error: errorText || "Erro ao gerar Memorial Descritivo" },
        { status: pdfResponse.status }
      );
    }

    const pdfBuffer = await pdfResponse.arrayBuffer();

    return new NextResponse(pdfBuffer, {
      status: 200,
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition":
          'attachment; filename="memorial_descritivo.pdf"',
      },
    });
  } catch (err) {
    console.error("Error generating memorial:", err);
    return NextResponse.json(
      { error: "Erro interno ao gerar documento" },
      { status: 500 }
    );
  }
}
