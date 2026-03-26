import { cookies } from "next/headers";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

/**
 * Server-side fetch: reads apollo_token from cookies and adds
 * Authorization header. Use only in Server Components, Route Handlers,
 * or Server Actions.
 */
export async function apiFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  const cookieStore = await cookies();
  const token = cookieStore.get("apollo_token")?.value;

  const headers: HeadersInit = {
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const url = `${BACKEND_URL}${path}`;

  return fetch(url, {
    ...options,
    headers,
  });
}

/**
 * Client-side fetch: calls the Next.js API proxy routes.
 * Never touches the backend URL or the token directly.
 */
export async function clientFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  return fetch(path, {
    ...options,
    credentials: "same-origin",
  });
}
