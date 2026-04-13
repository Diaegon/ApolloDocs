/**
 * Tests for the shared SistemaSection component.
 *
 * This component is used by both MemorialForm and TodosForm.
 * It must render all inversor and placa fields for a given system index,
 * and wire field names with the correct prefix (sistema_instalado1/2/3).
 *
 * We test it wrapped in a minimal useForm harness to provide register/errors.
 */

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { useForm } from "react-hook-form";
import { SistemaSection } from "@/components/forms/shared/sistema-section";
import type { ProjetoMemorialFormData } from "@/lib/validations/memorial";

function SistemaSectionHarness({ index }: { index: 1 | 2 | 3 }) {
  const { register, formState: { errors } } = useForm<ProjetoMemorialFormData>();
  return (
    <SistemaSection
      index={index}
      register={register as Parameters<typeof SistemaSection>[0]["register"]}
      errors={errors as Parameters<typeof SistemaSection>[0]["errors"]}
    />
  );
}

describe("SistemaSection — inversor fields", () => {
  it("renders inversor marca field (identified by placeholder)", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByPlaceholderText("Ex: Growatt")).toBeInTheDocument();
  });

  it("renders inversor modelo field (identified by placeholder)", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByPlaceholderText("Ex: MIN 6000TL-X")).toBeInTheDocument();
  });

  it("renders inversor potência field", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByLabelText(/potência.*kw/i)).toBeInTheDocument();
  });

  it("renders número de fases select", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByLabelText(/número de fases/i)).toBeInTheDocument();
  });

  it("renders tipo de inversor select", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByLabelText(/tipo de inversor/i)).toBeInTheDocument();
  });

  it("renders quantidade de inversores field", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByLabelText(/quantidade de inversores/i)).toBeInTheDocument();
  });
});

describe("SistemaSection — placa (módulo fotovoltaico) fields", () => {
  it("renders módulo fotovoltaico heading", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByText(/módulo fotovoltaico/i)).toBeInTheDocument();
  });

  it("renders potência (Wp) field", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByLabelText(/potência.*wp/i)).toBeInTheDocument();
  });

  it("renders tipo de célula field", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByLabelText(/tipo de célula/i)).toBeInTheDocument();
  });

  it("renders tensão de pico field", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByLabelText(/tensão de pico/i)).toBeInTheDocument();
  });

  it("renders corrente de curto-circuito field", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByLabelText(/curto-circuito/i)).toBeInTheDocument();
  });

  it("renders quantidade de placas field", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByLabelText(/quantidade de placas.*string 1/i)).toBeInTheDocument();
  });
});

describe("SistemaSection — system index title", () => {
  it("shows 'Sistema 1' for index 1", () => {
    render(<SistemaSectionHarness index={1} />);
    expect(screen.getByText("Sistema 1")).toBeInTheDocument();
  });

  it("shows 'Sistema 2' for index 2", () => {
    render(<SistemaSectionHarness index={2} />);
    expect(screen.getByText("Sistema 2")).toBeInTheDocument();
  });

  it("shows 'Sistema 3' for index 3", () => {
    render(<SistemaSectionHarness index={3} />);
    expect(screen.getByText("Sistema 3")).toBeInTheDocument();
  });
});

describe("SistemaSection — field name prefixing", () => {
  it("input ids are prefixed with sistema_instalado1 for index 1", () => {
    render(<SistemaSectionHarness index={1} />);
    // The marca inversor input should have the correct id
    const marcaInput = document.querySelector(
      "#sistema_instalado1\\.inversor\\.marca_inversor"
    );
    expect(marcaInput).toBeInTheDocument();
  });

  it("input ids are prefixed with sistema_instalado2 for index 2", () => {
    render(<SistemaSectionHarness index={2} />);
    const marcaInput = document.querySelector(
      "#sistema_instalado2\\.inversor\\.marca_inversor"
    );
    expect(marcaInput).toBeInTheDocument();
  });
});
