import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, act, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createElement } from "react";
import { useGenerateDoc } from "@/hooks/use-generate-doc";

// Mock fetch globally
const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

// Mock URL methods
const mockCreateObjectURL = vi.fn(() => "blob:generated-url");
const mockRevokeObjectURL = vi.fn();
Object.defineProperty(globalThis, "URL", {
  value: {
    createObjectURL: mockCreateObjectURL,
    revokeObjectURL: mockRevokeObjectURL,
  },
  writable: true,
});

function makeWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      mutations: { retry: false },
      queries: { retry: false },
    },
  });
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return createElement(QueryClientProvider, { client: queryClient }, children);
  };
}

describe("useGenerateDoc", () => {
  beforeEach(() => {
    mockFetch.mockClear();
    mockCreateObjectURL.mockClear();
    mockRevokeObjectURL.mockClear();
  });

  it("initializes with null pdfUrl and no error", () => {
    const { result } = renderHook(
      () => useGenerateDoc({ docType: "memorial" }),
      { wrapper: makeWrapper() }
    );

    expect(result.current.pdfUrl).toBeNull();
    expect(result.current.error).toBeNull();
    expect(result.current.isLoading).toBe(false);
  });

  it("returns pdfUrl after successful generation", async () => {
    const mockBlob = new Blob(["PDF content"], { type: "application/pdf" });
    mockFetch.mockResolvedValueOnce({
      ok: true,
      blob: () => Promise.resolve(mockBlob),
    });

    const { result } = renderHook(
      () => useGenerateDoc({ docType: "memorial" }),
      { wrapper: makeWrapper() }
    );

    act(() => {
      result.current.generate({ test: "data" });
    });

    await waitFor(() => {
      expect(result.current.pdfUrl).toBe("blob:generated-url");
    });

    expect(mockCreateObjectURL).toHaveBeenCalledWith(mockBlob);
    expect(result.current.error).toBeNull();
  });

  it("sets error message on failed generation", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({ error: "Token inválido" }),
    });

    const { result } = renderHook(
      () => useGenerateDoc({ docType: "procuracao" }),
      { wrapper: makeWrapper() }
    );

    act(() => {
      result.current.generate({ test: "data" });
    });

    await waitFor(() => {
      expect(result.current.error).toBe("Token inválido");
    });

    expect(result.current.pdfUrl).toBeNull();
  });

  it("uses default error message when response has no error field", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({}),
    });

    const { result } = renderHook(
      () => useGenerateDoc({ docType: "unifilar" }),
      { wrapper: makeWrapper() }
    );

    act(() => {
      result.current.generate({});
    });

    await waitFor(() => {
      expect(result.current.error).toBe("Erro ao gerar documento");
    });
  });

  it("resets state and revokes URL when reset is called", async () => {
    const mockBlob = new Blob(["PDF"], { type: "application/pdf" });
    mockFetch.mockResolvedValueOnce({
      ok: true,
      blob: () => Promise.resolve(mockBlob),
    });

    const { result } = renderHook(
      () => useGenerateDoc({ docType: "formulario" }),
      { wrapper: makeWrapper() }
    );

    act(() => {
      result.current.generate({});
    });

    await waitFor(() => {
      expect(result.current.pdfUrl).toBe("blob:generated-url");
    });

    act(() => {
      result.current.reset();
    });

    expect(result.current.pdfUrl).toBeNull();
    expect(result.current.error).toBeNull();
    expect(mockRevokeObjectURL).toHaveBeenCalledWith("blob:generated-url");
  });

  it("posts to correct endpoint for each doc type", async () => {
    const endpoints: Record<string, string> = {
      memorial: "/api/docs/memorial",
      procuracao: "/api/docs/procuracao",
      unifilar: "/api/docs/unifilar",
      formulario: "/api/docs/formulario",
    };

    for (const [docType, expectedEndpoint] of Object.entries(endpoints)) {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        blob: () => Promise.resolve(new Blob(["PDF"])),
      });

      const { result } = renderHook(
        () => useGenerateDoc({ docType: docType as "memorial" | "procuracao" | "unifilar" | "formulario" }),
        { wrapper: makeWrapper() }
      );

      act(() => {
        result.current.generate({ data: "test" });
      });

      await waitFor(() => {
        expect(result.current.pdfUrl).toBeTruthy();
      });

      expect(mockFetch).toHaveBeenCalledWith(
        expectedEndpoint,
        expect.objectContaining({ method: "POST" })
      );

      mockFetch.mockClear();
      mockCreateObjectURL.mockClear();
    }
  });

  it("sets isLoading to true while generating", async () => {
    // Never-resolving promise keeps mutation in pending state indefinitely
    const fetchPromise = new Promise(() => {});
    mockFetch.mockReturnValueOnce(fetchPromise);

    const { result } = renderHook(
      () => useGenerateDoc({ docType: "memorial" }),
      { wrapper: makeWrapper() }
    );

    act(() => {
      result.current.generate({});
    });

    // TanStack Query v5 sets isPending asynchronously — wait for it
    await waitFor(() => {
      expect(result.current.isLoading).toBe(true);
    });
  });
});
