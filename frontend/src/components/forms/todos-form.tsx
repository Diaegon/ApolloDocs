"use client";

import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQuery } from "@tanstack/react-query";
import {
  projetoTodosSchema,
  type ProjetoTodosFormData,
} from "@/lib/validations/todos";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { FormField } from "@/components/ui/form-field";
import { useGenerateDoc } from "@/hooks/use-generate-doc";
import { FileArchive, Plus } from "lucide-react";
import {
  InversorCascadeRow,
  PlacaCascadeRow,
} from "@/components/forms/shared/catalog-cascade-select";
import {
  FASES_OPTIONS,
  CLASSE_CONSUMO_OPTIONS,
  RAMAL_OPTIONS,
} from "@/components/forms/shared/form-options";
import type { InversorPublic, PlacaPublic } from "@/types/docs";

export function TodosForm() {
  const { generate, pdfUrl, filename, isLoading, error, reset } =
    useGenerateDoc({ docType: "todos" });

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
  } = useForm<ProjetoTodosFormData>({
    resolver: zodResolver(projetoTodosSchema),
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

  function onSubmit(data: ProjetoTodosFormData) {
    generate(data);
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
        {/* Dados do Projetista */}
        <fieldset className="form-section space-y-4">
          <legend>Dados do Projetista</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField label="Nome do Projetista" htmlFor="nome_projetista" error={errors.nome_projetista?.message} required>
              <Input id="nome_projetista" placeholder="Eng. Carlos Lima" error={errors.nome_projetista?.message} {...register("nome_projetista")} />
            </FormField>
            <FormField label="CFT / CREA" htmlFor="cft_crea_projetista" error={errors.cft_crea_projetista?.message} required>
              <Input id="cft_crea_projetista" placeholder="CREA-CE 12345" error={errors.cft_crea_projetista?.message} {...register("cft_crea_projetista")} />
            </FormField>
          </div>
        </fieldset>

        {/* Informações do Projeto */}
        <fieldset className="form-section space-y-4">
          <legend>Informações do Projeto</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <FormField label="Número da UC" htmlFor="numero_unidade_consumidora" error={errors.numero_unidade_consumidora?.message} required>
              <Input id="numero_unidade_consumidora" placeholder="123456789" error={errors.numero_unidade_consumidora?.message} {...register("numero_unidade_consumidora")} />
            </FormField>
            <FormField label="Data do Projeto" htmlFor="data_projeto" error={errors.data_projeto?.message} required>
              <Input id="data_projeto" type="date" error={errors.data_projeto?.message} {...register("data_projeto")} />
            </FormField>
            <FormField label="Carga Instalada (kW)" htmlFor="carga_instalada_kw" error={errors.carga_instalada_kw?.message} required>
              <Input id="carga_instalada_kw" type="number" step="0.01" placeholder="5.5" error={errors.carga_instalada_kw?.message} {...register("carga_instalada_kw", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Disjuntor Geral (A)" htmlFor="disjuntor_geral_amperes" error={errors.disjuntor_geral_amperes?.message} required>
              <Input id="disjuntor_geral_amperes" type="number" placeholder="40" error={errors.disjuntor_geral_amperes?.message} {...register("disjuntor_geral_amperes", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Energia Média Mensal (kWh)" htmlFor="energia_media_mensal_kwh" error={errors.energia_media_mensal_kwh?.message} required>
              <Input id="energia_media_mensal_kwh" type="number" step="0.01" placeholder="350" error={errors.energia_media_mensal_kwh?.message} {...register("energia_media_mensal_kwh", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Tensão Local (V)" htmlFor="tensao_local" error={errors.tensao_local?.message} required>
              <Input id="tensao_local" type="number" placeholder="220" error={errors.tensao_local?.message} {...register("tensao_local", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Potência de Geração (W)" htmlFor="potencia_geracao" error={errors.potencia_geracao?.message} required>
              <Input id="potencia_geracao" type="number" placeholder="5000" error={errors.potencia_geracao?.message} {...register("potencia_geracao", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Classe de Consumo" htmlFor="classe_consumo" error={errors.classe_consumo?.message} required>
              <Select id="classe_consumo" options={[...CLASSE_CONSUMO_OPTIONS]} placeholder="Selecione" error={errors.classe_consumo?.message} {...register("classe_consumo")} />
            </FormField>
            <FormField label="Tipo de Fornecimento" htmlFor="tipo_fornecimento" error={errors.tipo_fornecimento?.message} required>
              <Select id="tipo_fornecimento" options={[...FASES_OPTIONS]} placeholder="Selecione" error={errors.tipo_fornecimento?.message} {...register("tipo_fornecimento")} />
            </FormField>
            <FormField label="Ramal de Energia" htmlFor="ramal_energia" error={errors.ramal_energia?.message} required>
              <Select id="ramal_energia" options={[...RAMAL_OPTIONS]} placeholder="Selecione" error={errors.ramal_energia?.message} {...register("ramal_energia")} />
            </FormField>
          </div>
        </fieldset>

        {/* Dados do Cliente */}
        <fieldset className="form-section space-y-4">
          <legend>Dados do Cliente</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField label="Nome Completo" htmlFor="cliente.nome_cliente" error={errors.cliente?.nome_cliente?.message} required>
              <Input id="cliente.nome_cliente" {...register("cliente.nome_cliente")} />
            </FormField>
            <FormField label="CPF" htmlFor="cliente.cpf" error={errors.cliente?.cpf?.message} required>
              <Input id="cliente.cpf" placeholder="000.000.000-00" {...register("cliente.cpf")} />
            </FormField>
            <FormField label="RG" htmlFor="cliente.rg" error={errors.cliente?.rg?.message} required>
              <Input id="cliente.rg" {...register("cliente.rg")} />
            </FormField>
            <FormField label="Data de Nascimento" htmlFor="cliente.data_nascimento" error={errors.cliente?.data_nascimento?.message} required>
              <Input id="cliente.data_nascimento" type="date" {...register("cliente.data_nascimento")} />
            </FormField>
            <FormField label="Telefone" htmlFor="cliente.telefone_cliente" error={errors.cliente?.telefone_cliente?.message} required>
              <Input id="cliente.telefone_cliente" {...register("cliente.telefone_cliente")} />
            </FormField>
            <FormField label="E-mail" htmlFor="cliente.email_cliente" error={errors.cliente?.email_cliente?.message} required>
              <Input id="cliente.email_cliente" type="email" {...register("cliente.email_cliente")} />
            </FormField>
          </div>
          <h4 className="mt-4 mb-2 text-sm font-semibold text-gray-700">Endereço do Cliente</h4>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField label="Logradouro" htmlFor="endereco_cliente.logradouro_cliente" error={errors.endereco_cliente?.logradouro_cliente?.message} required>
              <Input {...register("endereco_cliente.logradouro_cliente")} />
            </FormField>
            <FormField label="Número" htmlFor="endereco_cliente.numero_casa_cliente" error={errors.endereco_cliente?.numero_casa_cliente?.message} required>
              <Input {...register("endereco_cliente.numero_casa_cliente")} />
            </FormField>
            <FormField label="Complemento" htmlFor="endereco_cliente.complemento_casa_cliente" error={errors.endereco_cliente?.complemento_casa_cliente?.message}>
              <Input {...register("endereco_cliente.complemento_casa_cliente")} />
            </FormField>
            <FormField label="CEP" htmlFor="endereco_cliente.cep_cliente" error={errors.endereco_cliente?.cep_cliente?.message} required>
              <Input {...register("endereco_cliente.cep_cliente")} />
            </FormField>
            <FormField label="Bairro" htmlFor="endereco_cliente.bairro_cliente" error={errors.endereco_cliente?.bairro_cliente?.message} required>
              <Input {...register("endereco_cliente.bairro_cliente")} />
            </FormField>
            <FormField label="Cidade" htmlFor="endereco_cliente.cidade_cliente" error={errors.endereco_cliente?.cidade_cliente?.message} required>
              <Input {...register("endereco_cliente.cidade_cliente")} />
            </FormField>
            <FormField label="Estado (UF)" htmlFor="endereco_cliente.estado_cliente" error={errors.endereco_cliente?.estado_cliente?.message} required>
              <Input maxLength={2} className="uppercase w-24" {...register("endereco_cliente.estado_cliente")} />
            </FormField>
          </div>
        </fieldset>

        {/* Endereço da Obra */}
        <fieldset className="form-section space-y-4">
          <legend>Endereço da Obra</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField label="Logradouro" htmlFor="endereco_obra.logradouro_obra" error={errors.endereco_obra?.logradouro_obra?.message} required>
              <Input {...register("endereco_obra.logradouro_obra")} />
            </FormField>
            <FormField label="Número" htmlFor="endereco_obra.numero_obra" error={errors.endereco_obra?.numero_obra?.message} required>
              <Input {...register("endereco_obra.numero_obra")} />
            </FormField>
            <FormField label="Complemento" htmlFor="endereco_obra.complemento_obra" error={errors.endereco_obra?.complemento_obra?.message}>
              <Input {...register("endereco_obra.complemento_obra")} />
            </FormField>
            <FormField label="CEP" htmlFor="endereco_obra.cep_obra" error={errors.endereco_obra?.cep_obra?.message} required>
              <Input {...register("endereco_obra.cep_obra")} />
            </FormField>
            <FormField label="Bairro" htmlFor="endereco_obra.bairro_obra" error={errors.endereco_obra?.bairro_obra?.message} required>
              <Input {...register("endereco_obra.bairro_obra")} />
            </FormField>
            <FormField label="Cidade" htmlFor="endereco_obra.cidade_obra" error={errors.endereco_obra?.cidade_obra?.message} required>
              <Input {...register("endereco_obra.cidade_obra")} />
            </FormField>
            <FormField label="Estado (UF)" htmlFor="endereco_obra.estado_obra" error={errors.endereco_obra?.estado_obra?.message} required>
              <Input maxLength={2} className="uppercase w-24" {...register("endereco_obra.estado_obra")} />
            </FormField>
          </div>
        </fieldset>

        {/* Dados do Procurador */}
        <fieldset className="form-section space-y-4">
          <legend>Dados do Procurador</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField label="Nome Completo" htmlFor="procurador.nome_procurador" error={errors.procurador?.nome_procurador?.message} required>
              <Input {...register("procurador.nome_procurador")} />
            </FormField>
            <FormField label="CPF" htmlFor="procurador.cpf_procurador" error={errors.procurador?.cpf_procurador?.message} required>
              <Input {...register("procurador.cpf_procurador")} />
            </FormField>
            <FormField label="RG" htmlFor="procurador.rg_procurador" error={errors.procurador?.rg_procurador?.message} required>
              <Input {...register("procurador.rg_procurador")} />
            </FormField>
            <FormField label="Telefone" htmlFor="procurador.telefone_procurador" error={errors.procurador?.telefone_procurador?.message} required>
              <Input {...register("procurador.telefone_procurador")} />
            </FormField>
            <FormField label="E-mail" htmlFor="procurador.email_procurador" error={errors.procurador?.email_procurador?.message} required>
              <Input type="email" {...register("procurador.email_procurador")} />
            </FormField>
          </div>
          <h4 className="mt-4 mb-2 text-sm font-semibold text-gray-700">Endereço do Procurador</h4>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField label="Logradouro" htmlFor="procurador.logradouro_procurador" error={errors.procurador?.logradouro_procurador?.message} required>
              <Input {...register("procurador.logradouro_procurador")} />
            </FormField>
            <FormField label="Número" htmlFor="procurador.numero_casa_procurador" error={errors.procurador?.numero_casa_procurador?.message} required>
              <Input {...register("procurador.numero_casa_procurador")} />
            </FormField>
            <FormField label="Complemento" htmlFor="procurador.complemento_procurador" error={errors.procurador?.complemento_procurador?.message}>
              <Input {...register("procurador.complemento_procurador")} />
            </FormField>
            <FormField label="CEP" htmlFor="procurador.cep_procurador" error={errors.procurador?.cep_procurador?.message} required>
              <Input {...register("procurador.cep_procurador")} />
            </FormField>
            <FormField label="Bairro" htmlFor="procurador.bairro_procurador" error={errors.procurador?.bairro_procurador?.message} required>
              <Input {...register("procurador.bairro_procurador")} />
            </FormField>
            <FormField label="Cidade" htmlFor="procurador.cidade_procurador" error={errors.procurador?.cidade_procurador?.message} required>
              <Input {...register("procurador.cidade_procurador")} />
            </FormField>
            <FormField label="Estado (UF)" htmlFor="procurador.estado_procurador" error={errors.procurador?.estado_procurador?.message} required>
              <Input maxLength={2} className="uppercase w-24" {...register("procurador.estado_procurador")} />
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
            <FileArchive className="h-5 w-5" aria-hidden="true" />
            {isLoading ? "Gerando ZIP…" : "Gerar ZIP de Documentos"}
          </Button>
          {pdfUrl && (
            <Button type="button" variant="secondary" size="lg" onClick={reset}>
              Nova geração
            </Button>
          )}
        </div>
      </form>

      {pdfUrl && (
        <div className="mt-8 rounded-md bg-green-50 p-6 flex flex-col items-center justify-center space-y-4 shadow-sm border border-green-200 animate-in fade-in slide-in-from-bottom-2">
          <FileArchive className="h-12 w-12 text-green-600" />
          <p className="text-gray-800 text-center font-medium">Os documentos foram gerados com sucesso e unificados num arquivo ZIP.</p>
          <a
            href={pdfUrl}
            download={filename}
            className="inline-flex items-center gap-2 rounded-md bg-green-600 px-6 py-3 font-semibold text-white shadow hover:bg-green-700 transition"
          >
            Baixar {filename}
          </a>
        </div>
      )}
    </div>
  );
}
