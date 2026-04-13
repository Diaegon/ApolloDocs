/**
 * Tests for Next.js security headers configuration.
 *
 * These headers are required for a SaaS handling PII (CPF, RG, address data):
 *  - X-Frame-Options: prevents clickjacking
 *  - X-Content-Type-Options: prevents MIME sniffing
 *  - Referrer-Policy: limits referrer leakage
 *  - Strict-Transport-Security: enforces HTTPS
 *  - Content-Security-Policy: limits resource origins
 *  - Permissions-Policy: restricts browser features
 *
 * The headers() function must apply to all routes (source: "/:path*").
 */

import { describe, it, expect } from "vitest";
import nextConfig from "../../next.config";

async function getAllHeaders() {
  if (typeof nextConfig.headers !== "function") {
    throw new Error("next.config must export a headers() function");
  }
  const configs = await nextConfig.headers();
  return configs.flatMap((c) => c.headers);
}

async function getHeader(key: string) {
  const all = await getAllHeaders();
  return all.find((h) => h.key === key);
}

describe("next.config — headers() is defined", () => {
  it("exports a headers() async function", () => {
    expect(typeof nextConfig.headers).toBe("function");
  });

  it("headers() resolves to a non-empty array", async () => {
    const configs = await (nextConfig.headers as () => Promise<unknown[]>)();
    expect(Array.isArray(configs)).toBe(true);
    expect(configs.length).toBeGreaterThan(0);
  });
});

describe("next.config — header coverage", () => {
  it("applies headers to all routes (source includes /:path*)", async () => {
    if (typeof nextConfig.headers !== "function") throw new Error();
    const configs = await nextConfig.headers();
    const globalRule = configs.find(
      (c) => c.source === "/:path*" || c.source === "(.*)"
    );
    expect(
      globalRule,
      'A header rule with source "/:path*" or "(.*)" must exist'
    ).toBeDefined();
  });

  it("sets X-Frame-Options to DENY", async () => {
    const header = await getHeader("X-Frame-Options");
    expect(header, "X-Frame-Options header must be configured").toBeDefined();
    expect(header?.value).toBe("DENY");
  });

  it("sets X-Content-Type-Options to nosniff", async () => {
    const header = await getHeader("X-Content-Type-Options");
    expect(header, "X-Content-Type-Options header must be configured").toBeDefined();
    expect(header?.value).toBe("nosniff");
  });

  it("sets Referrer-Policy", async () => {
    const header = await getHeader("Referrer-Policy");
    expect(header, "Referrer-Policy header must be configured").toBeDefined();
    expect(header?.value).toBeTruthy();
  });

  it("sets Strict-Transport-Security with max-age", async () => {
    const header = await getHeader("Strict-Transport-Security");
    expect(header, "Strict-Transport-Security header must be configured").toBeDefined();
    expect(header?.value).toMatch(/max-age=\d+/);
  });

  it("sets Content-Security-Policy", async () => {
    const header = await getHeader("Content-Security-Policy");
    expect(header, "Content-Security-Policy header must be configured").toBeDefined();
    expect(header?.value).toBeTruthy();
  });

  it("CSP includes default-src directive", async () => {
    const header = await getHeader("Content-Security-Policy");
    expect(header?.value).toContain("default-src");
  });

  it("CSP allows blob: in frame-src (required for PDF iframe viewer)", async () => {
    const header = await getHeader("Content-Security-Policy");
    expect(header?.value).toContain("blob:");
  });

  it("sets Permissions-Policy", async () => {
    const header = await getHeader("Permissions-Policy");
    expect(header, "Permissions-Policy header must be configured").toBeDefined();
    expect(header?.value).toBeTruthy();
  });
});
