/**
 * Tests for the register page component.
 *
 * Key behavioral contract:
 *  - The registration request MUST be sent to the Next.js proxy route
 *    (/api/auth/register), NOT directly to the backend URL.
 *  - The backend URL must never appear in client-side fetch calls.
 *  - After successful registration the component triggers an auto-login
 *    via /api/auth/login (also a proxy route).
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import RegisterPage from "@/app/(auth)/register/page";

// Mock Next.js router
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    refresh: vi.fn(),
  }),
}));

const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

const validFormData = {
  username: "meu_usuario",
  email: "test@example.com",
  password: "senha123",
  confirmPassword: "senha123",
};

async function fillAndSubmitForm(overrides: Partial<typeof validFormData> = {}) {
  const data = { ...validFormData, ...overrides };
  if (data.username)
    await userEvent.type(screen.getByLabelText(/nome de usuário/i), data.username);
  if (data.email)
    await userEvent.type(screen.getByLabelText(/e-mail/i), data.email);
  const passwords = screen.getAllByLabelText(/senha/i);
  if (data.password) await userEvent.type(passwords[0], data.password);
  if (data.confirmPassword) await userEvent.type(passwords[1], data.confirmPassword);
  await userEvent.click(screen.getByRole("button", { name: /criar conta/i }));
}

describe("RegisterPage — proxy route usage", () => {
  beforeEach(() => {
    mockFetch.mockClear();
    vi.clearAllMocks();
  });

  it("submits registration to /api/auth/register, not to backend URL directly", async () => {
    // Register succeeds
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true }), { status: 201 })
    );
    // Auto-login succeeds
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true }), { status: 200 })
    );

    render(<RegisterPage />);
    await fillAndSubmitForm();

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalled();
    });

    const allCalls = mockFetch.mock.calls as [string, RequestInit][];
    const registerCall = allCalls.find(([url]) =>
      url === "/api/auth/register"
    );
    expect(
      registerCall,
      "Registration must go through /api/auth/register proxy, not directly to the backend"
    ).toBeDefined();
  });

  it("never calls the backend URL directly during registration", async () => {
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true }), { status: 201 })
    );
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true }), { status: 200 })
    );

    render(<RegisterPage />);
    await fillAndSubmitForm();

    await waitFor(() => expect(mockFetch).toHaveBeenCalled());

    const allCalls = mockFetch.mock.calls as [string, RequestInit][];
    const directBackendCall = allCalls.find(([url]) =>
      String(url).includes("localhost:8000") ||
      String(url).includes("BACKEND_URL") ||
      String(url).includes("/users/")
    );
    expect(
      directBackendCall,
      "Client component must not call backend directly"
    ).toBeUndefined();
  });

  it("sends correct JSON payload to /api/auth/register", async () => {
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true }), { status: 201 })
    );
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true }), { status: 200 })
    );

    render(<RegisterPage />);
    await fillAndSubmitForm();

    await waitFor(() => expect(mockFetch).toHaveBeenCalled());

    const allCalls = mockFetch.mock.calls as [string, RequestInit][];
    const registerCall = allCalls.find(([url]) => url === "/api/auth/register");
    expect(registerCall).toBeDefined();
    const body = JSON.parse(registerCall![1].body as string) as Record<string, unknown>;
    expect(body.username).toBe("meu_usuario");
    expect(body.email).toBe("test@example.com");
    expect(body.password).toBe("senha123");
  });

  it("shows server error message when registration fails", async () => {
    mockFetch.mockResolvedValueOnce(
      new Response(
        JSON.stringify({ error: "E-mail já cadastrado" }),
        { status: 422 }
      )
    );

    render(<RegisterPage />);
    await fillAndSubmitForm();

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("E-mail já cadastrado");
    });
  });

  it("auto-logs in via /api/auth/login after successful registration", async () => {
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true }), { status: 201 })
    );
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ success: true }), { status: 200 })
    );

    render(<RegisterPage />);
    await fillAndSubmitForm();

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledTimes(2);
    });

    const allCalls = mockFetch.mock.calls as [string, RequestInit][];
    const loginCall = allCalls.find(([url]) => url === "/api/auth/login");
    expect(loginCall).toBeDefined();
  });
});
