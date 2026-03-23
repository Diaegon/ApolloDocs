import { vi, describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { TodosForm } from "@/components/forms/todos-form";
import { useGenerateDoc } from "@/hooks/use-generate-doc";

vi.mock("@/hooks/use-generate-doc", () => ({
  useGenerateDoc: vi.fn(),
}));

describe("TodosForm UI for Zip Archive", () => {
  it("renders the default form state successfully", () => {
    vi.mocked(useGenerateDoc).mockReturnValue({
      generate: vi.fn(),
      reset: vi.fn(),
      pdfUrl: null,
      filename: "documentos.zip",
      isLoading: false,
      error: null,
    });

    render(<TodosForm />);
    expect(screen.getByRole("button", { name: /Gerar ZIP de Documentos/i })).toBeInTheDocument();
  });

  it("renders success state and zip download button when pdfUrl is provided", () => {
    vi.mocked(useGenerateDoc).mockReturnValue({
      generate: vi.fn(),
      reset: vi.fn(),
      pdfUrl: "blob:test-zip-url",
      filename: "documentos.zip",
      isLoading: false,
      error: null,
    });

    render(<TodosForm />);

    // Assert that the success message appears
    expect(screen.getByText(/Os documentos foram gerados com sucesso e unificados num arquivo ZIP/i)).toBeInTheDocument();

    // Assert that the download link points to the ZIP
    const downloadLink = screen.getByRole("link", { name: /Baixar documentos.zip/i });
    expect(downloadLink).toBeInTheDocument();
    expect(downloadLink).toHaveAttribute("href", "blob:test-zip-url");
    expect(downloadLink).toHaveAttribute("download", "documentos.zip");
  });
  
  it("renders error message when generation fails", () => {
    vi.mocked(useGenerateDoc).mockReturnValue({
      generate: vi.fn(),
      reset: vi.fn(),
      pdfUrl: null,
      filename: "documentos.zip",
      isLoading: false,
      error: "Falha na validação do servidor",
    });

    render(<TodosForm />);

    const alertMsg = screen.getByRole("alert");
    expect(alertMsg).toHaveTextContent("Falha na validação do servidor");
  });
});
