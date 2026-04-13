/**
 * Tests for Sidebar layout component.
 *
 * Contracts:
 *  - Renders a logout button ("Sair")
 *  - Clicking it POSTs to /api/auth/logout
 *  - On success redirects to /login via router.push
 *  - Existing navigation links are still present
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Sidebar } from "@/components/layout/sidebar";

const mockPush = vi.fn();
const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

vi.mock("next/navigation", () => ({
  usePathname: () => "/dashboard",
  useRouter: () => ({ push: mockPush }),
}));

describe("Sidebar — navigation", () => {
  beforeEach(() => {
    mockFetch.mockClear();
    mockPush.mockClear();
  });

  it("renders the app brand", () => {
    render(<Sidebar />);
    expect(screen.getByText("ApolloDocs")).toBeInTheDocument();
  });

  it("renders all main navigation links", () => {
    render(<Sidebar />);
    expect(screen.getByRole("link", { name: /painel/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /memorial descritivo/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /procuração/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /diagrama unifilar/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /formulário enel/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /todos os documentos/i })).toBeInTheDocument();
  });
});

describe("Sidebar — logout button", () => {
  beforeEach(() => {
    mockFetch.mockClear();
    mockPush.mockClear();
  });

  it("renders a logout button", () => {
    render(<Sidebar />);
    expect(screen.getByRole("button", { name: /sair/i })).toBeInTheDocument();
  });

  it("calls POST /api/auth/logout when the logout button is clicked", async () => {
    mockFetch.mockResolvedValueOnce({ ok: true });
    render(<Sidebar />);
    await userEvent.click(screen.getByRole("button", { name: /sair/i }));
    expect(mockFetch).toHaveBeenCalledWith(
      "/api/auth/logout",
      expect.objectContaining({ method: "POST" })
    );
  });

  it("redirects to /login after a successful logout", async () => {
    mockFetch.mockResolvedValueOnce({ ok: true });
    render(<Sidebar />);
    await userEvent.click(screen.getByRole("button", { name: /sair/i }));
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/login");
    });
  });

  it("still redirects to /login even if the logout request fails", async () => {
    mockFetch.mockResolvedValueOnce({ ok: false });
    render(<Sidebar />);
    await userEvent.click(screen.getByRole("button", { name: /sair/i }));
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/login");
    });
  });
});
