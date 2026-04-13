/**
 * Tests for the Todos page metadata.
 *
 * The root layout already defines title template: "%s | ApolloDocs".
 * Page-level metadata must supply only the short title segment — NOT the full
 * "Short Title | ApolloDocs" string, which would produce a double-suffix
 * "Short Title | ApolloDocs | ApolloDocs" in the browser tab.
 */

import { describe, it, expect, vi } from "vitest";

// Stub the form component so we can import the server page without rendering it
vi.mock("@/components/forms/todos-form", () => ({
  TodosForm: () => null,
}));
vi.mock("@/components/layout/header", () => ({
  Header: () => null,
}));

import { metadata } from "@/app/(dashboard)/dashboard/todos/page";

function resolveTitle(
  value: NonNullable<typeof metadata>["title"]
): string {
  if (typeof value === "string") return value;
  if (value && typeof value === "object" && "default" in value)
    return String(value.default);
  return String(value);
}

describe("TodosPage metadata — title", () => {
  it("title is defined", () => {
    expect(metadata.title).toBeDefined();
  });

  it("title is 'Todos os Documentos' (short form, no site suffix)", () => {
    const title = resolveTitle(metadata.title);
    expect(title).toBe("Todos os Documentos");
  });

  it("title does not include 'ApolloDocs' (template adds it)", () => {
    const title = resolveTitle(metadata.title);
    expect(title).not.toContain("ApolloDocs");
  });

  it("title does not include a pipe separator (template adds it)", () => {
    const title = resolveTitle(metadata.title);
    expect(title).not.toContain("|");
  });
});
