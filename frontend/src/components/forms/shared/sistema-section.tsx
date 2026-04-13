"use client";

import type { UseFormRegister, FieldErrors } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { FormField } from "@/components/ui/form-field";
import {
  FASES_OPTIONS,
  TIPO_INVERSOR_OPTIONS,
} from "@/components/forms/shared/form-options";
import type { configuracaoSistemaSchema } from "@/lib/validations/memorial";
import type { z } from "zod";

type ConfiguracaoSistema = z.infer<typeof configuracaoSistemaSchema>;

/** Minimal structural type covering the sistema_instalado* fields shared
 *  by ProjetoMemorialFormData and ProjetoTodosFormData. */
export interface FormWithSistemas {
  sistema_instalado1: ConfiguracaoSistema;
  sistema_instalado2?: ConfiguracaoSistema;
  sistema_instalado3?: ConfiguracaoSistema;
}

export interface SistemaSectionProps {
  index: 1 | 2 | 3;
  // UseFormRegister<any>/FieldErrors<any> are intentional: this component is
  // shared across memorial and todos schemas. eslint-config-next does not enable
  // @typescript-eslint/no-explicit-any so no suppress comment is needed here.
  register: UseFormRegister<any>;
  errors: FieldErrors<any>;
}

export function SistemaSection({ index, register, errors }: SistemaSectionProps) {
  const prefix = `sistema_instalado${index}` as
    | "sistema_instalado1"
    | "sistema_instalado2"
    | "sistema_instalado3";

  // Cast errors to FormWithSistemas to get typed field access; the `any` from
  // the prop type makes this safe at runtime — Zod ensures the actual shape.
  const sysErrors = (errors as FieldErrors<FormWithSistemas>)[prefix] as FieldErrors<FormWithSistemas>[typeof prefix];

  return (
    <fieldset className="form-section space-y-6">
      <legend>Sistema {index}</legend>

      {/* Inversor */}
      <div>
        <h4 className="mb-3 text-sm font-semibold text-gray-700">Inversor</h4>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <FormField
            label="Marca"
            htmlFor={`${prefix}.inversor.marca_inversor`}
            error={sysErrors?.inversor?.marca_inversor?.message}
            required
          >
            <Input
              id={`${prefix}.inversor.marca_inversor`}
              placeholder="Ex: Growatt"
              error={sysErrors?.inversor?.marca_inversor?.message}
              {...register(`${prefix}.inversor.marca_inversor`)}
            />
          </FormField>

          <FormField
            label="Modelo"
            htmlFor={`${prefix}.inversor.modelo_inversor`}
            error={sysErrors?.inversor?.modelo_inversor?.message}
            required
          >
            <Input
              id={`${prefix}.inversor.modelo_inversor`}
              placeholder="Ex: MIN 6000TL-X"
              error={sysErrors?.inversor?.modelo_inversor?.message}
              {...register(`${prefix}.inversor.modelo_inversor`)}
            />
          </FormField>

          <FormField
            label="Potência (kW)"
            htmlFor={`${prefix}.inversor.potencia_inversor`}
            error={sysErrors?.inversor?.potencia_inversor?.message}
            required
          >
            <Input
              id={`${prefix}.inversor.potencia_inversor`}
              type="number"
              step="0.01"
              placeholder="6"
              error={sysErrors?.inversor?.potencia_inversor?.message}
              {...register(`${prefix}.inversor.potencia_inversor`, {
                valueAsNumber: true,
              })}
            />
          </FormField>

          <FormField
            label="Número de Fases"
            htmlFor={`${prefix}.inversor.numero_fases`}
            error={sysErrors?.inversor?.numero_fases?.message}
            required
          >
            <Select
              id={`${prefix}.inversor.numero_fases`}
              options={[...FASES_OPTIONS]}
              placeholder="Selecione"
              error={sysErrors?.inversor?.numero_fases?.message}
              {...register(`${prefix}.inversor.numero_fases`)}
            />
          </FormField>

          <FormField
            label="Tipo de Inversor"
            htmlFor={`${prefix}.inversor.tipo_de_inversor`}
            error={sysErrors?.inversor?.tipo_de_inversor?.message}
            required
          >
            <Select
              id={`${prefix}.inversor.tipo_de_inversor`}
              options={[...TIPO_INVERSOR_OPTIONS]}
              placeholder="Selecione"
              error={sysErrors?.inversor?.tipo_de_inversor?.message}
              {...register(`${prefix}.inversor.tipo_de_inversor`)}
            />
          </FormField>

          <FormField
            label="Número de MPPTs"
            htmlFor={`${prefix}.inversor.numero_mppt`}
            error={sysErrors?.inversor?.numero_mppt?.message}
          >
            <Input
              id={`${prefix}.inversor.numero_mppt`}
              type="number"
              placeholder="2"
              error={sysErrors?.inversor?.numero_mppt?.message}
              {...register(`${prefix}.inversor.numero_mppt`, {
                valueAsNumber: true,
              })}
            />
          </FormField>
        </div>
      </div>

      {/* Quantidade de inversores */}
      <FormField
        label="Quantidade de Inversores"
        htmlFor={`${prefix}.quantidade_inversor`}
        error={sysErrors?.quantidade_inversor?.message}
        required
      >
        <Input
          id={`${prefix}.quantidade_inversor`}
          type="number"
          placeholder="1"
          className="w-40"
          error={sysErrors?.quantidade_inversor?.message}
          {...register(`${prefix}.quantidade_inversor`, {
            valueAsNumber: true,
          })}
        />
      </FormField>

      {/* Módulos / Placa */}
      <div>
        <h4 className="mb-3 text-sm font-semibold text-gray-700">
          Módulo Fotovoltaico
        </h4>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <FormField
            label="Marca"
            htmlFor={`${prefix}.placa.marca_placa`}
            error={sysErrors?.placa?.marca_placa?.message}
            required
          >
            <Input
              id={`${prefix}.placa.marca_placa`}
              placeholder="Ex: Canadian Solar"
              error={sysErrors?.placa?.marca_placa?.message}
              {...register(`${prefix}.placa.marca_placa`)}
            />
          </FormField>

          <FormField
            label="Modelo"
            htmlFor={`${prefix}.placa.modelo_placa`}
            error={sysErrors?.placa?.modelo_placa?.message}
            required
          >
            <Input
              id={`${prefix}.placa.modelo_placa`}
              placeholder="Ex: CS6R-420MS"
              error={sysErrors?.placa?.modelo_placa?.message}
              {...register(`${prefix}.placa.modelo_placa`)}
            />
          </FormField>

          <FormField
            label="Potência (Wp)"
            htmlFor={`${prefix}.placa.potencia_placa`}
            error={sysErrors?.placa?.potencia_placa?.message}
            required
          >
            <Input
              id={`${prefix}.placa.potencia_placa`}
              type="number"
              step="0.01"
              placeholder="420"
              error={sysErrors?.placa?.potencia_placa?.message}
              {...register(`${prefix}.placa.potencia_placa`, {
                valueAsNumber: true,
              })}
            />
          </FormField>

          <FormField
            label="Tipo de Célula"
            htmlFor={`${prefix}.placa.tipo_celula`}
            error={sysErrors?.placa?.tipo_celula?.message}
            required
          >
            <Input
              id={`${prefix}.placa.tipo_celula`}
              placeholder="Ex: Monocristalino"
              error={sysErrors?.placa?.tipo_celula?.message}
              {...register(`${prefix}.placa.tipo_celula`)}
            />
          </FormField>

          <FormField
            label="Tensão de Pico Voc (V)"
            htmlFor={`${prefix}.placa.tensao_pico`}
            error={sysErrors?.placa?.tensao_pico?.message}
            required
          >
            <Input
              id={`${prefix}.placa.tensao_pico`}
              type="number"
              step="0.01"
              placeholder="49.1"
              error={sysErrors?.placa?.tensao_pico?.message}
              {...register(`${prefix}.placa.tensao_pico`, {
                valueAsNumber: true,
              })}
            />
          </FormField>

          <FormField
            label="Corrente de Curto-circuito Isc (A)"
            htmlFor={`${prefix}.placa.corrente_curtocircuito`}
            error={sysErrors?.placa?.corrente_curtocircuito?.message}
            required
          >
            <Input
              id={`${prefix}.placa.corrente_curtocircuito`}
              type="number"
              step="0.01"
              placeholder="11.21"
              error={sysErrors?.placa?.corrente_curtocircuito?.message}
              {...register(`${prefix}.placa.corrente_curtocircuito`, {
                valueAsNumber: true,
              })}
            />
          </FormField>

          <FormField
            label="Tensão Máx. Potência Vmpp (V)"
            htmlFor={`${prefix}.placa.tensao_maxima_potencia`}
            error={sysErrors?.placa?.tensao_maxima_potencia?.message}
            required
          >
            <Input
              id={`${prefix}.placa.tensao_maxima_potencia`}
              type="number"
              step="0.01"
              placeholder="41.3"
              error={sysErrors?.placa?.tensao_maxima_potencia?.message}
              {...register(`${prefix}.placa.tensao_maxima_potencia`, {
                valueAsNumber: true,
              })}
            />
          </FormField>

          <FormField
            label="Corrente Máx. Potência Impp (A)"
            htmlFor={`${prefix}.placa.corrente_maxima_potencia`}
            error={sysErrors?.placa?.corrente_maxima_potencia?.message}
            required
          >
            <Input
              id={`${prefix}.placa.corrente_maxima_potencia`}
              type="number"
              step="0.01"
              placeholder="10.17"
              error={sysErrors?.placa?.corrente_maxima_potencia?.message}
              {...register(`${prefix}.placa.corrente_maxima_potencia`, {
                valueAsNumber: true,
              })}
            />
          </FormField>

          <FormField
            label="Eficiência (%)"
            htmlFor={`${prefix}.placa.eficiencia_placa`}
            error={sysErrors?.placa?.eficiencia_placa?.message}
          >
            <Input
              id={`${prefix}.placa.eficiencia_placa`}
              type="number"
              step="0.01"
              placeholder="21.4"
              error={sysErrors?.placa?.eficiencia_placa?.message}
              {...register(`${prefix}.placa.eficiencia_placa`, {
                valueAsNumber: true,
              })}
            />
          </FormField>
        </div>
      </div>

      {/* Quantidade de placas */}
      <div className="grid grid-cols-2 gap-4">
        <FormField
          label="Quantidade de Placas (string 1)"
          htmlFor={`${prefix}.quantidade_total_placas_do_sistema.quantidade_placas`}
          error={
            sysErrors?.quantidade_total_placas_do_sistema?.quantidade_placas
              ?.message
          }
          required
        >
          <Input
            id={`${prefix}.quantidade_total_placas_do_sistema.quantidade_placas`}
            type="number"
            placeholder="12"
            error={
              sysErrors?.quantidade_total_placas_do_sistema?.quantidade_placas
                ?.message
            }
            {...register(
              `${prefix}.quantidade_total_placas_do_sistema.quantidade_placas`,
              { valueAsNumber: true }
            )}
          />
        </FormField>

        <FormField
          label="Quantidade de Placas (string 2)"
          htmlFor={`${prefix}.quantidade_total_placas_do_sistema.quantidade_placas2`}
          error={
            sysErrors?.quantidade_total_placas_do_sistema?.quantidade_placas2
              ?.message
          }
        >
          <Input
            id={`${prefix}.quantidade_total_placas_do_sistema.quantidade_placas2`}
            type="number"
            placeholder="0"
            error={
              sysErrors?.quantidade_total_placas_do_sistema?.quantidade_placas2
                ?.message
            }
            {...register(
              `${prefix}.quantidade_total_placas_do_sistema.quantidade_placas2`,
              { valueAsNumber: true }
            )}
          />
        </FormField>
      </div>
    </fieldset>
  );
}
