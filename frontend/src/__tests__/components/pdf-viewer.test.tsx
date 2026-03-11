import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { PdfViewer } from "@/components/pdf-viewer";

// Mock URL.revokeObjectURL
const mockRevokeObjectURL = vi.fn();
const mockCreateObjectURL = vi.fn(() => "blob:mock-url");

Object.defineProperty(globalThis, "URL", {
  value: {
    ...globalThis.URL,
    revokeObjectURL: mockRevokeObjectURL,
    createObjectURL: mockCreateObjectURL,
  },
  writable: true,
});

describe("PdfViewer", () => {
  beforeEach(() => {
    mockRevokeObjectURL.mockClear();
  });

  it("renders the iframe with the provided pdfUrl", () => {
    render(<PdfViewer pdfUrl="blob:test-url" />);
    const iframe = screen.getByTitle("Visualizador de PDF");
    expect(iframe).toBeInTheDocument();
    expect(iframe).toHaveAttribute("src", "blob:test-url");
  });

  it("renders the download button", () => {
    render(<PdfViewer pdfUrl="blob:test-url" />);
    expect(screen.getByText("Baixar PDF")).toBeInTheDocument();
  });

  it("renders success message", () => {
    render(<PdfViewer pdfUrl="blob:test-url" />);
    expect(
      screen.getByText("Documento gerado com sucesso")
    ).toBeInTheDocument();
  });

  it("renders close button when onClose is provided", () => {
    const onClose = vi.fn();
    render(<PdfViewer pdfUrl="blob:test-url" onClose={onClose} />);
    expect(screen.getByLabelText("Fechar visualizador")).toBeInTheDocument();
  });

  it("does not render close button when onClose is not provided", () => {
    render(<PdfViewer pdfUrl="blob:test-url" />);
    expect(
      screen.queryByLabelText("Fechar visualizador")
    ).not.toBeInTheDocument();
  });

  it("calls onClose when close button is clicked", () => {
    const onClose = vi.fn();
    render(<PdfViewer pdfUrl="blob:test-url" onClose={onClose} />);
    fireEvent.click(screen.getByLabelText("Fechar visualizador"));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("revokes blob URL on unmount", () => {
    const { unmount } = render(<PdfViewer pdfUrl="blob:test-url-to-revoke" />);
    unmount();
    expect(mockRevokeObjectURL).toHaveBeenCalledWith("blob:test-url-to-revoke");
  });

  it("does not revoke non-blob URLs on unmount", () => {
    const { unmount } = render(
      <PdfViewer pdfUrl="https://example.com/doc.pdf" />
    );
    unmount();
    expect(mockRevokeObjectURL).not.toHaveBeenCalled();
  });

  it("triggers download with correct filename", () => {
    // Render first — mocking createElement before render breaks React's DOM creation
    render(
      <PdfViewer pdfUrl="blob:test-url" filename="meu_documento.pdf" />
    );

    const appendChildSpy = vi.spyOn(document.body, "appendChild").mockImplementation((el) => el);
    const removeChildSpy = vi.spyOn(document.body, "removeChild").mockImplementation((el) => el);
    const clickSpy = vi.fn();

    const originalCreateElement = document.createElement.bind(document);
    vi.spyOn(document, "createElement").mockImplementation((tag: string) => {
      if (tag === "a") {
        const el = originalCreateElement("a");
        el.click = clickSpy;
        return el;
      }
      return originalCreateElement(tag);
    });

    fireEvent.click(screen.getByText("Baixar PDF"));

    expect(clickSpy).toHaveBeenCalled();
    expect(appendChildSpy).toHaveBeenCalled();
    expect(removeChildSpy).toHaveBeenCalled();

    appendChildSpy.mockRestore();
    removeChildSpy.mockRestore();
    vi.spyOn(document, "createElement").mockRestore();
  });
});
