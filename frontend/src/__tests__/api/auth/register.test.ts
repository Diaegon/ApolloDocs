/**
 * Tests for POST /api/auth/register route handler.
 *
 * The handler must:
 *  - Validate that username, email and password are present (400 otherwise)
 *  - Forward the request to the backend POST /users/ endpoint
 *  - Return { success: true } with status 201 on success
 *  - Propagate backend error messages correctly
 *  - Never expose the backend URL in its response body
 *  - Never set any auth cookie (registration is not authentication)
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { POST } from "@/app/api/auth/register/route";

const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

/** Helper to build a minimal NextRequest-like object for the handler. */
function makeRequest(body: Record<string, unknown>) {
  return new Request("http://localhost/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }) as Parameters<typeof POST>[0];
}

describe("POST /api/auth/register — input validation", () => {
  beforeEach(() => mockFetch.mockClear());

  it("returns 400 when username is missing", async () => {
    const response = await POST(
      makeRequest({ email: "test@test.com", password: "senha123" })
    );
    expect(response.status).toBe(400);
    const body = await response.json() as { error: string };
    expect(body.error).toBeTruthy();
    expect(mockFetch).not.toHaveBeenCalled();
  });

  it("returns 400 when email is missing", async () => {
    const response = await POST(
      makeRequest({ username: "usuario", password: "senha123" })
    );
    expect(response.status).toBe(400);
    expect(mockFetch).not.toHaveBeenCalled();
  });

  it("returns 400 when password is missing", async () => {
    const response = await POST(
      makeRequest({ username: "usuario", email: "test@test.com" })
    );
    expect(response.status).toBe(400);
    expect(mockFetch).not.toHaveBeenCalled();
  });

  it("returns 400 when all fields are empty strings", async () => {
    const response = await POST(
      makeRequest({ username: "", email: "", password: "" })
    );
    expect(response.status).toBe(400);
    expect(mockFetch).not.toHaveBeenCalled();
  });
});

describe("POST /api/auth/register — backend forwarding", () => {
  beforeEach(() => mockFetch.mockClear());

  it("calls backend /users/ with the correct payload", async () => {
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ id: 1, email: "test@test.com" }), {
        status: 201,
      })
    );

    await POST(
      makeRequest({
        username: "meu_usuario",
        email: "test@test.com",
        password: "senha123",
      })
    );

    expect(mockFetch).toHaveBeenCalledOnce();
    const [url, options] = mockFetch.mock.calls[0] as [string, RequestInit];
    expect(url).toMatch(/\/users\/$/);
    expect(options.method).toBe("POST");
    const sentBody = JSON.parse(options.body as string) as Record<string, unknown>;
    expect(sentBody.username).toBe("meu_usuario");
    expect(sentBody.email).toBe("test@test.com");
    expect(sentBody.password).toBe("senha123");
  });

  it("returns 201 and { success: true } on successful registration", async () => {
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ id: 1 }), { status: 201 })
    );

    const response = await POST(
      makeRequest({
        username: "meu_usuario",
        email: "test@test.com",
        password: "senha123",
      })
    );

    expect(response.status).toBe(201);
    const body = await response.json() as { success: boolean };
    expect(body.success).toBe(true);
  });

  it("propagates string error from backend detail field", async () => {
    mockFetch.mockResolvedValueOnce(
      new Response(
        JSON.stringify({ detail: "E-mail já cadastrado" }),
        { status: 422 }
      )
    );

    const response = await POST(
      makeRequest({
        username: "meu_usuario",
        email: "used@test.com",
        password: "senha123",
      })
    );

    expect(response.status).toBe(422);
    const body = await response.json() as { error: string };
    expect(body.error).toBe("E-mail já cadastrado");
  });

  it("propagates array of validation errors from backend detail field", async () => {
    const detail = [
      { msg: "value is not a valid email" },
      { msg: "username too short" },
    ];
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ detail }), { status: 422 })
    );

    const response = await POST(
      makeRequest({
        username: "ab",
        email: "bad-email",
        password: "senha123",
      })
    );

    expect(response.status).toBe(422);
    const body = await response.json() as { error: string };
    expect(body.error).toContain("value is not a valid email");
    expect(body.error).toContain("username too short");
  });

  it("returns 500 when backend call throws", async () => {
    mockFetch.mockRejectedValueOnce(new Error("network failure"));

    const response = await POST(
      makeRequest({
        username: "meu_usuario",
        email: "test@test.com",
        password: "senha123",
      })
    );

    expect(response.status).toBe(500);
  });
});

describe("POST /api/auth/register — security constraints", () => {
  beforeEach(() => mockFetch.mockClear());

  it("response body does not contain the backend URL", async () => {
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ id: 1 }), { status: 201 })
    );

    const response = await POST(
      makeRequest({
        username: "meu_usuario",
        email: "test@test.com",
        password: "senha123",
      })
    );

    const text = await response.text();
    expect(text).not.toContain("localhost:8000");
    expect(text).not.toContain("BACKEND_URL");
  });

  it("does not set any cookie on the response", async () => {
    mockFetch.mockResolvedValueOnce(
      new Response(JSON.stringify({ id: 1 }), { status: 201 })
    );

    const response = await POST(
      makeRequest({
        username: "meu_usuario",
        email: "test@test.com",
        password: "senha123",
      })
    );

    // Registration must not authenticate — no cookie should be set
    expect(response.headers.get("set-cookie")).toBeNull();
  });
});
