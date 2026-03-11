"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Download, X } from "lucide-react";

interface PdfViewerProps {
  pdfUrl: string;
  filename?: string;
  onClose?: () => void;
}

export function PdfViewer({
  pdfUrl,
  filename = "documento.pdf",
  onClose,
}: PdfViewerProps) {
  // Clean up the object URL when the component unmounts or pdfUrl changes
  useEffect(() => {
    return () => {
      if (pdfUrl.startsWith("blob:")) {
        URL.revokeObjectURL(pdfUrl);
      }
    };
  }, [pdfUrl]);

  function handleDownload() {
    const link = document.createElement("a");
    link.href = pdfUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  return (
    <div className="flex flex-col gap-3 rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-gray-700">
          Documento gerado com sucesso
        </p>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleDownload}
            className="gap-1.5"
          >
            <Download className="h-4 w-4" aria-hidden="true" />
            Baixar PDF
          </Button>
          {onClose && (
            <button
              onClick={onClose}
              className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
              aria-label="Fechar visualizador"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      <iframe
        src={pdfUrl}
        className="h-[600px] w-full rounded border border-gray-200"
        title="Visualizador de PDF"
      />
    </div>
  );
}
