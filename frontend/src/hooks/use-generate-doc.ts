"use client";

import { useState, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import type { DocType } from "@/types/docs";

interface UseGenerateDocOptions {
  docType: DocType;
  filename?: string;
}

interface GenerateDocState {
  pdfUrl: string | null;
  isLoading: boolean;
  error: string | null;
}

const DOC_ENDPOINTS: Record<DocType, string> = {
  memorial: "/api/docs/memorial",
  procuracao: "/api/docs/procuracao",
  unifilar: "/api/docs/unifilar",
  formulario: "/api/docs/formulario",
  todos: "/api/docs/todos",
};

const DOC_FILENAMES: Record<DocType, string> = {
  memorial: "memorial_descritivo.pdf",
  procuracao: "procuracao.pdf",
  unifilar: "diagrama_unifilar.pdf",
  formulario: "formulario_enel_ce.pdf",
  todos: "documentos.zip",
};

export function useGenerateDoc({ docType, filename }: UseGenerateDocOptions) {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  const resolvedFilename = filename ?? DOC_FILENAMES[docType];
  const endpoint = DOC_ENDPOINTS[docType];

  const mutation = useMutation({
    mutationFn: async (data: unknown): Promise<string> => {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({})) as Record<string, unknown>;
        throw new Error(
          (errorBody.error as string) ?? "Erro ao gerar documento"
        );
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      return url;
    },
    onSuccess: (url) => {
      // Revoke previous URL to avoid memory leaks
      if (pdfUrl) {
        URL.revokeObjectURL(pdfUrl);
      }
      setPdfUrl(url);
    },
  });

  const generate = useCallback(
    (data: unknown) => {
      mutation.mutate(data);
    },
    [mutation]
  );

  const reset = useCallback(() => {
    if (pdfUrl) {
      URL.revokeObjectURL(pdfUrl);
    }
    setPdfUrl(null);
    mutation.reset();
  }, [mutation, pdfUrl]);

  return {
    generate,
    pdfUrl,
    filename: resolvedFilename,
    isLoading: mutation.isPending,
    error: mutation.error?.message ?? null,
    reset,
  };
}
