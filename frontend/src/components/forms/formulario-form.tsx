"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  projetoFormularioEnelCeSchema,
  type ProjetoFormularioEnelCeFormData,
} from "@/lib/validations/formulario";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { FormField } from "@/components/ui/form-field";
import { useGenerateDoc } from "@/hooks/use-generate-doc";
import { PdfViewer } from "@/components/pdf-viewer";
import { ClipboardList } from "lucide-react";

const CLASSE_OPTIONS = [
  { value: "residencial", label: "Residencial" },
  { value: "comercial", label: "Comercial" },
  { value: "industrial", label: "Industrial" },
  { value: "rural", label: "Rural" },
];

const RAMAL_OPTIONS = [
  { value: "aereo", label: "Aéreo" },
  { value: "subterraneo", label: "Subterrâneo" },
];

export function FormularioForm() {
  const { generate, pdfUrl, filename, isLoading, error, reset } =
    useGenerateDoc({ docType: "formulario" });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProjetoFormularioEnelCeFormData>({
    resolver: zodResolver(projetoFormularioEnelCeSchema),
    defaultValues: {
      data_hoje: new Date().toISOString().split("T")[0],
    },
  });

  function onSubmit(data: ProjetoFormularioEnelCeFormData) {
    generate(data);
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
        {/* Dados da UC */}
        <fieldset className="form-section space-y-4">
          <legend>Dados da Unidade Consumidora</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              label="Número da UC"
              htmlFor="numero_uc"
              error={errors.numero_uc?.message}
              required
            >
              <Input
                id="numero_uc"
                placeholder="123456789"
                error={errors.numero_uc?.message}
                {...register("numero_uc")}
              />
            </FormField>

            <FormField
              label="Classe de Consumo"
              htmlFor="classe"
              error={errors.classe?.message}
              required
            >
              <Select
                id="classe"
                options={CLASSE_OPTIONS}
                placeholder="Selecione"
                error={errors.classe?.message}
                {...register("classe")}
              />
            </FormField>

            <FormField
              label="Ramal de Energia"
              htmlFor="ramal_energia"
              error={errors.ramal_energia?.message}
              required
            >
              <Select
                id="ramal_energia"
                options={RAMAL_OPTIONS}
                placeholder="Selecione"
                error={errors.ramal_energia?.message}
                {...register("ramal_energia")}
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

            <FormField
              label="Carga Instalada (kW)"
              htmlFor="carga_instalada_kw"
              error={errors.carga_instalada_kw?.message}
              required
            >
              <Input
                id="carga_instalada_kw"
                type="number"
                step="0.01"
                placeholder="5.5"
                error={errors.carga_instalada_kw?.message}
                {...register("carga_instalada_kw", { valueAsNumber: true })}
              />
            </FormField>

            <FormField
              label="Potência de Geração (kWp)"
              htmlFor="potencia_geracao"
              error={errors.potencia_geracao?.message}
              required
            >
              <Input
                id="potencia_geracao"
                type="number"
                step="0.01"
                placeholder="5.04"
                error={errors.potencia_geracao?.message}
                {...register("potencia_geracao", { valueAsNumber: true })}
              />
            </FormField>

            <FormField
              label="Data"
              htmlFor="data_hoje"
              error={errors.data_hoje?.message}
              required
            >
              <Input
                id="data_hoje"
                type="date"
                error={errors.data_hoje?.message}
                {...register("data_hoje")}
              />
            </FormField>
          </div>
        </fieldset>

        {/* Dados do Cliente */}
        <fieldset className="form-section space-y-4">
          <legend>Dados do Cliente</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              label="Nome Completo"
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
              label="CPF"
              htmlFor="cpf"
              error={errors.cpf?.message}
              required
            >
              <Input
                id="cpf"
                placeholder="000.000.000-00"
                error={errors.cpf?.message}
                {...register("cpf")}
              />
            </FormField>

            <FormField
              label="Telefone"
              htmlFor="telefone_cliente"
              error={errors.telefone_cliente?.message}
              required
            >
              <Input
                id="telefone_cliente"
                placeholder="(85) 99999-9999"
                error={errors.telefone_cliente?.message}
                {...register("telefone_cliente")}
              />
            </FormField>

            <FormField
              label="E-mail"
              htmlFor="email_cliente"
              error={errors.email_cliente?.message}
              required
            >
              <Input
                id="email_cliente"
                type="email"
                placeholder="cliente@email.com"
                error={errors.email_cliente?.message}
                {...register("email_cliente")}
              />
            </FormField>
          </div>
        </fieldset>

        {/* Endereço da Obra */}
        <fieldset className="form-section space-y-4">
          <legend>Endereço da Obra</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              label="Logradouro"
              htmlFor="endereco_obra.logradouro_obra"
              error={errors.endereco_obra?.logradouro_obra?.message}
              required
            >
              <Input
                id="endereco_obra.logradouro_obra"
                placeholder="Rua das Flores"
                error={errors.endereco_obra?.logradouro_obra?.message}
                {...register("endereco_obra.logradouro_obra")}
              />
            </FormField>

            <FormField
              label="Número"
              htmlFor="endereco_obra.numero_obra"
              error={errors.endereco_obra?.numero_obra?.message}
              required
            >
              <Input
                id="endereco_obra.numero_obra"
                placeholder="123"
                error={errors.endereco_obra?.numero_obra?.message}
                {...register("endereco_obra.numero_obra")}
              />
            </FormField>

            <FormField
              label="Complemento"
              htmlFor="endereco_obra.complemento_obra"
            >
              <Input
                id="endereco_obra.complemento_obra"
                placeholder="Apt 10"
                {...register("endereco_obra.complemento_obra")}
              />
            </FormField>

            <FormField
              label="CEP"
              htmlFor="endereco_obra.cep_obra"
              error={errors.endereco_obra?.cep_obra?.message}
              required
            >
              <Input
                id="endereco_obra.cep_obra"
                placeholder="60000-000"
                error={errors.endereco_obra?.cep_obra?.message}
                {...register("endereco_obra.cep_obra")}
              />
            </FormField>

            <FormField
              label="Bairro"
              htmlFor="endereco_obra.bairro_obra"
              error={errors.endereco_obra?.bairro_obra?.message}
              required
            >
              <Input
                id="endereco_obra.bairro_obra"
                placeholder="Centro"
                error={errors.endereco_obra?.bairro_obra?.message}
                {...register("endereco_obra.bairro_obra")}
              />
            </FormField>

            <FormField
              label="Cidade"
              htmlFor="endereco_obra.cidade_obra"
              error={errors.endereco_obra?.cidade_obra?.message}
              required
            >
              <Input
                id="endereco_obra.cidade_obra"
                placeholder="Fortaleza"
                error={errors.endereco_obra?.cidade_obra?.message}
                {...register("endereco_obra.cidade_obra")}
              />
            </FormField>

            <FormField
              label="Estado (UF)"
              htmlFor="endereco_obra.estado_obra"
              error={errors.endereco_obra?.estado_obra?.message}
              required
            >
              <Input
                id="endereco_obra.estado_obra"
                placeholder="CE"
                maxLength={2}
                className="uppercase w-24"
                error={errors.endereco_obra?.estado_obra?.message}
                {...register("endereco_obra.estado_obra")}
              />
            </FormField>
          </div>
        </fieldset>

        {/* Dados do Procurador */}
        <fieldset className="form-section space-y-4">
          <legend>Dados do Procurador</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              label="Nome do Procurador"
              htmlFor="nome_procurador"
              error={errors.nome_procurador?.message}
              required
            >
              <Input
                id="nome_procurador"
                placeholder="Maria Souza"
                error={errors.nome_procurador?.message}
                {...register("nome_procurador")}
              />
            </FormField>

            <FormField
              label="CPF do Procurador"
              htmlFor="cpf_procurador"
              error={errors.cpf_procurador?.message}
              required
            >
              <Input
                id="cpf_procurador"
                placeholder="000.000.000-00"
                error={errors.cpf_procurador?.message}
                {...register("cpf_procurador")}
              />
            </FormField>

            <FormField
              label="E-mail do Procurador"
              htmlFor="email_procurador"
              error={errors.email_procurador?.message}
              required
            >
              <Input
                id="email_procurador"
                type="email"
                placeholder="procurador@email.com"
                error={errors.email_procurador?.message}
                {...register("email_procurador")}
              />
            </FormField>

            <FormField
              label="Telefone do Procurador"
              htmlFor="telefone_procurador"
              error={errors.telefone_procurador?.message}
              required
            >
              <Input
                id="telefone_procurador"
                placeholder="(85) 99999-9999"
                error={errors.telefone_procurador?.message}
                {...register("telefone_procurador")}
              />
            </FormField>
          </div>
        </fieldset>

        {error && (
          <div
            className="rounded-md bg-red-50 p-4 text-sm text-red-700"
            role="alert"
          >
            {error}
          </div>
        )}

        <div className="flex gap-3">
          <Button
            type="submit"
            size="lg"
            isLoading={isLoading}
            className="gap-2"
          >
            <ClipboardList className="h-5 w-5" aria-hidden="true" />
            {isLoading ? "Gerando PDF…" : "Gerar PDF"}
          </Button>
          {pdfUrl && (
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={reset}
            >
              Nova geração
            </Button>
          )}
        </div>
      </form>

      {pdfUrl && (
        <PdfViewer pdfUrl={pdfUrl} filename={filename} onClose={reset} />
      )}
    </div>
  );
}
