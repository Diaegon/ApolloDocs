"use client";

import { useState } from "react";
import type {
  UseFormRegister,
  UseFormSetValue,
  FieldErrors,
} from "react-hook-form";
import { Select } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { FormField } from "@/components/ui/form-field";
import { Trash2 } from "lucide-react";
import type { InversorPublic, PlacaPublic } from "@/types/docs";

// ─── Inversor row ─────────────────────────────────────────────────────────────
// Renders: [Marca select] [Modelo select] [Qtd input] [Trash?]
// Brand is local state; model is registered to react-hook-form.
// Changing brand remounts the model select (via key) and resets the form value.

interface InversorRowProps {
  inversores: InversorPublic[];
  index: number;
  register: UseFormRegister<any>;
  setValue: UseFormSetValue<any>;
  errors?: FieldErrors<any>;
  onRemove?: () => void;
}

export function InversorCascadeRow({
  inversores,
  index,
  register,
  setValue,
  errors,
  onRemove,
}: InversorRowProps) {
  const [brand, setBrand] = useState("");

  const brands = Array.from(
    new Set(inversores.map((inv) => inv.marca_inversor))
  ).sort();

  const brandOptions = brands.map((b) => ({ value: b, label: b }));

  const modelOptions = inversores
    .filter((inv) => inv.marca_inversor === brand)
    .map((inv) => {
      const kw = (inv.potencia_inversor / 1000).toFixed(1).replace(".0", "");
      return {
        value: String(inv.id_inversor),
        label: `${inv.modelo_inversor} — ${kw} kW`,
      };
    });

  const isLoading = inversores.length === 0;
  const idField = `inversores.${index}.id_inversor`;
  const qtdField = `inversores.${index}.quantidade`;
  const rowErrors = (errors?.inversores as any)?.[index];

  function handleBrandChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setBrand(e.target.value);
    setValue(idField, 0);
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-[1fr_1fr_auto_auto] items-end">
      <FormField label={`Marca ${index + 1}`} htmlFor={`brand-inv-${index}`}>
        <Select
          id={`brand-inv-${index}`}
          options={brandOptions}
          placeholder={isLoading ? "Carregando…" : "Selecione a marca"}
          disabled={isLoading}
          value={brand}
          onChange={handleBrandChange}
        />
      </FormField>

      <FormField
        label="Modelo"
        htmlFor={idField}
        error={rowErrors?.id_inversor?.message}
        required
      >
        {/* key=brand forces remount when brand changes, clearing the DOM selection */}
        <Select
          key={brand}
          id={idField}
          options={modelOptions}
          placeholder={brand ? "Selecione o modelo" : "← marca primeiro"}
          error={rowErrors?.id_inversor?.message}
          disabled={!brand || modelOptions.length === 0}
          {...register(idField)}
        />
      </FormField>

      <FormField
        label="Qtd."
        htmlFor={qtdField}
        error={rowErrors?.quantidade?.message}
        required
      >
        <Input
          id={qtdField}
          type="number"
          min={1}
          className="w-24"
          error={rowErrors?.quantidade?.message}
          {...register(qtdField)}
        />
      </FormField>

      {onRemove && (
        <button
          type="button"
          onClick={onRemove}
          className="mb-0.5 flex items-center gap-1 rounded-md px-2 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
          aria-label={`Remover inversor ${index + 1}`}
        >
          <Trash2 className="h-4 w-4" aria-hidden="true" />
        </button>
      )}
    </div>
  );
}

// ─── Placa row ────────────────────────────────────────────────────────────────
// Same pattern for solar panels.

interface PlacaRowProps {
  placas: PlacaPublic[];
  index: number;
  register: UseFormRegister<any>;
  setValue: UseFormSetValue<any>;
  errors?: FieldErrors<any>;
  onRemove?: () => void;
}

export function PlacaCascadeRow({
  placas,
  index,
  register,
  setValue,
  errors,
  onRemove,
}: PlacaRowProps) {
  const [brand, setBrand] = useState("");

  const brands = Array.from(
    new Set(placas.map((p) => p.marca_placa))
  ).sort();

  const brandOptions = brands.map((b) => ({ value: b, label: b }));

  const modelOptions = placas
    .filter((p) => p.marca_placa === brand)
    .map((p) => ({
      value: String(p.id_placa),
      label: `${p.modelo_placa} — ${p.potencia_placa} Wp`,
    }));

  const isLoading = placas.length === 0;
  const idField = `placas.${index}.id_placa`;
  const qtdField = `placas.${index}.quantidade`;
  const rowErrors = (errors?.placas as any)?.[index];

  function handleBrandChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setBrand(e.target.value);
    setValue(idField, 0);
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-[1fr_1fr_auto_auto] items-end">
      <FormField label={`Marca ${index + 1}`} htmlFor={`brand-placa-${index}`}>
        <Select
          id={`brand-placa-${index}`}
          options={brandOptions}
          placeholder={isLoading ? "Carregando…" : "Selecione a marca"}
          disabled={isLoading}
          value={brand}
          onChange={handleBrandChange}
        />
      </FormField>

      <FormField
        label="Modelo"
        htmlFor={idField}
        error={rowErrors?.id_placa?.message}
        required
      >
        {/* key=brand forces remount when brand changes, clearing the DOM selection */}
        <Select
          key={brand}
          id={idField}
          options={modelOptions}
          placeholder={brand ? "Selecione o modelo" : "← marca primeiro"}
          error={rowErrors?.id_placa?.message}
          disabled={!brand || modelOptions.length === 0}
          {...register(idField)}
        />
      </FormField>

      <FormField
        label="Qtd."
        htmlFor={qtdField}
        error={rowErrors?.quantidade?.message}
        required
      >
        <Input
          id={qtdField}
          type="number"
          min={1}
          className="w-24"
          error={rowErrors?.quantidade?.message}
          {...register(qtdField)}
        />
      </FormField>

      {onRemove && (
        <button
          type="button"
          onClick={onRemove}
          className="mb-0.5 flex items-center gap-1 rounded-md px-2 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
          aria-label={`Remover módulo ${index + 1}`}
        >
          <Trash2 className="h-4 w-4" aria-hidden="true" />
        </button>
      )}
    </div>
  );
}
