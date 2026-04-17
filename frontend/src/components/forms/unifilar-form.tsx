"use client";

import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQuery } from "@tanstack/react-query";
import {
  projetoUnifilarV2Schema,
  type ProjetoUnifilarV2FormData,
} from "@/lib/validations/unifilar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FormField } from "@/components/ui/form-field";
import { useGenerateDoc } from "@/hooks/use-generate-doc";
import { PdfViewer } from "@/components/pdf-viewer";
import { Zap, Plus } from "lucide-react";
import {
  InversorCascadeRow,
  PlacaCascadeRow,
} from "@/components/forms/shared/catalog-cascade-select";
import type { InversorPublic, PlacaPublic } from "@/types/docs";

export function UnifilarForm() {
  const { generate, pdfUrl, filename, isLoading, error, reset } =
    useGenerateDoc({ docType: "unifilar" });

  const { data: inversoresData } = useQuery<{ inversores: InversorPublic[] }>({
    queryKey: ["catalogo", "inversores"],
    queryFn: () =>
      fetch("/api/equipamentos/inversores", { credentials: "same-origin" }).then(
        (r) => r.json()
      ),
  });

  const { data: placasData } = useQuery<{ placas: PlacaPublic[] }>({
    queryKey: ["catalogo", "placas"],
    queryFn: () =>
      fetch("/api/equipamentos/placas", { credentials: "same-origin" }).then(
        (r) => r.json()
      ),
  });

  const inversores = inversoresData?.inversores ?? [];
  const placas = placasData?.placas ?? [];

  const {
    register,
    handleSubmit,
    control,
    setValue,
    formState: { errors },
  } = useForm<ProjetoUnifilarV2FormData>({
    resolver: zodResolver(projetoUnifilarV2Schema),
    defaultValues: {
      inversores: [{ id_inversor: 0, quantidade: 1 }],
      placas: [{ id_placa: 0, quantidade: 10 }],
    },
  });

  const {
    fields: inversorFields,
    append: appendInversor,
    remove: removeInversor,
  } = useFieldArray({ control, name: "inversores" });

  const {
    fields: placaFields,
    append: appendPlaca,
    remove: removePlaca,
  } = useFieldArray({ control, name: "placas" });

  function onSubmit(data: ProjetoUnifilarV2FormData) {
    generate(data);
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
        {/* Informações do Projetista */}
        <fieldset className="form-section space-y-4">
          <legend>Informações do Projetista</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              label="Nome do Projetista"
              htmlFor="nome_projetista"
              error={errors.nome_projetista?.message}
              required
            >
              <Input
                id="nome_projetista"
                placeholder="Eng. Carlos Lima"
                error={errors.nome_projetista?.message}
                {...register("nome_projetista")}
              />
            </FormField>

            <FormField
              label="CFT / CREA"
              htmlFor="cft_crea_projetista"
              error={errors.cft_crea_projetista?.message}
              required
            >
              <Input
                id="cft_crea_projetista"
                placeholder="CREA-CE 12345"
                error={errors.cft_crea_projetista?.message}
                {...register("cft_crea_projetista")}
              />
            </FormField>
          </div>
        </fieldset>

        {/* Informações do Cliente */}
        <fieldset className="form-section space-y-4">
          <legend>Informações do Cliente</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              label="Nome do Cliente"
              htmlFor="nome_cliente"
              error={errors.nome_cliente?.message}
              required
            >
              <Input
                id="nome_cliente"
                placeholder="João da Silva"
                error={errors.nome_cliente?.message}
                {...register("nome_cliente")}
              />
            </FormField>

            <FormField
              label="Disjuntor Geral (A)"
              htmlFor="disjuntor_geral_amperes"
              error={errors.disjuntor_geral_amperes?.message}
              required
            >
              <Input
                id="disjuntor_geral_amperes"
                type="number"
                placeholder="40"
                error={errors.disjuntor_geral_amperes?.message}
                {...register("disjuntor_geral_amperes", { valueAsNumber: true })}
              />
            </FormField>

            <FormField
              label="Tensão Local (V)"
              htmlFor="tensao_local"
              error={errors.tensao_local?.message}
              required
            >
              <Input
                id="tensao_local"
                type="number"
                placeholder="220"
                error={errors.tensao_local?.message}
                {...register("tensao_local", { valueAsNumber: true })}
              />
            </FormField>
          </div>
        </fieldset>

        {/* Endereço da Obra */}
        <fieldset className="form-section space-y-4">
          <legend>Endereço da Obra</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField label="Logradouro" htmlFor="endereco_obra.logradouro_obra" error={errors.endereco_obra?.logradouro_obra?.message} required>
              <Input id="endereco_obra.logradouro_obra" placeholder="Rua das Flores" error={errors.endereco_obra?.logradouro_obra?.message} {...register("endereco_obra.logradouro_obra")} />
            </FormField>
            <FormField label="Número" htmlFor="endereco_obra.numero_obra" error={errors.endereco_obra?.numero_obra?.message} required>
              <Input id="endereco_obra.numero_obra" placeholder="123" error={errors.endereco_obra?.numero_obra?.message} {...register("endereco_obra.numero_obra")} />
            </FormField>
            <FormField label="CEP" htmlFor="endereco_obra.cep_obra" error={errors.endereco_obra?.cep_obra?.message} required>
              <Input id="endereco_obra.cep_obra" placeholder="60000-000" error={errors.endereco_obra?.cep_obra?.message} {...register("endereco_obra.cep_obra")} />
            </FormField>
            <FormField label="Bairro" htmlFor="endereco_obra.bairro_obra" error={errors.endereco_obra?.bairro_obra?.message} required>
              <Input id="endereco_obra.bairro_obra" placeholder="Centro" error={errors.endereco_obra?.bairro_obra?.message} {...register("endereco_obra.bairro_obra")} />
            </FormField>
            <FormField label="Cidade" htmlFor="endereco_obra.cidade_obra" error={errors.endereco_obra?.cidade_obra?.message} required>
              <Input id="endereco_obra.cidade_obra" placeholder="Fortaleza" error={errors.endereco_obra?.cidade_obra?.message} {...register("endereco_obra.cidade_obra")} />
            </FormField>
            <FormField label="Estado (UF)" htmlFor="endereco_obra.estado_obra" error={errors.endereco_obra?.estado_obra?.message} required>
              <Input id="endereco_obra.estado_obra" placeholder="CE" maxLength={2} className="uppercase w-24" error={errors.endereco_obra?.estado_obra?.message} {...register("endereco_obra.estado_obra")} />
            </FormField>
          </div>
        </fieldset>

        {/* Inversores */}
        <fieldset className="form-section space-y-3">
          <legend>Inversores</legend>
          {inversorFields.map((field, i) => (
            <InversorCascadeRow
              key={field.id}
              inversores={inversores}
              index={i}
              register={register}
              setValue={setValue}
              errors={errors}
              onRemove={inversorFields.length > 1 ? () => removeInversor(i) : undefined}
            />
          ))}
          {inversorFields.length < 3 && (
            <button
              type="button"
              onClick={() => appendInversor({ id_inversor: 0, quantidade: 1 })}
              className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-primary-600 hover:bg-primary-50 transition-colors"
            >
              <Plus className="h-4 w-4" aria-hidden="true" />
              Adicionar inversor
            </button>
          )}
        </fieldset>

        {/* Módulos Fotovoltaicos */}
        <fieldset className="form-section space-y-3">
          <legend>Módulos Fotovoltaicos</legend>
          {placaFields.map((field, i) => (
            <PlacaCascadeRow
              key={field.id}
              placas={placas}
              index={i}
              register={register}
              setValue={setValue}
              errors={errors}
              onRemove={placaFields.length > 1 ? () => removePlaca(i) : undefined}
            />
          ))}
          {placaFields.length < 3 && (
            <button
              type="button"
              onClick={() => appendPlaca({ id_placa: 0, quantidade: 10 })}
              className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-primary-600 hover:bg-primary-50 transition-colors"
            >
              <Plus className="h-4 w-4" aria-hidden="true" />
              Adicionar módulo
            </button>
          )}

          {/* Equal-length error surfaced at placas array level by Zod .refine() */}
          {errors.placas?.root?.message && (
            <p className="text-sm text-red-600">{errors.placas.root.message}</p>
          )}
        </fieldset>

        {error && (
          <div className="rounded-md bg-red-50 p-4 text-sm text-red-700" role="alert">
            {error}
          </div>
        )}

        <div className="flex gap-3">
          <Button type="submit" size="lg" isLoading={isLoading} className="gap-2">
            <Zap className="h-5 w-5" aria-hidden="true" />
            {isLoading ? "Gerando PDF…" : "Gerar PDF"}
          </Button>
          {pdfUrl && (
            <Button type="button" variant="secondary" size="lg" onClick={reset}>
              Nova geração
            </Button>
          )}
        </div>
      </form>

      {pdfUrl && <PdfViewer pdfUrl={pdfUrl} filename={filename} onClose={reset} />}
    </div>
  );
}
