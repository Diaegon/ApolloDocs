"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  projetoProcuracaoSchema,
  type ProjetoProcuracaoFormData,
} from "@/lib/validations/procuracao";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FormField } from "@/components/ui/form-field";
import { useGenerateDoc } from "@/hooks/use-generate-doc";
import { PdfViewer } from "@/components/pdf-viewer";
import { normalizeProcuracaoPayload } from "@/lib/payload/normalize";
import { ScrollText } from "lucide-react";

export function ProcuracaoForm() {
  const { generate, pdfUrl, filename, isLoading, error, reset } =
    useGenerateDoc({ docType: "procuracao" });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProjetoProcuracaoFormData>({
    resolver: zodResolver(projetoProcuracaoSchema),
  });

  function onSubmit(data: ProjetoProcuracaoFormData) {
    generate(normalizeProcuracaoPayload(data));
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
        {/* Dados do Cliente */}
        <fieldset className="form-section space-y-4">
          <legend>Dados do Cliente</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              label="Nome Completo"
              htmlFor="cliente.nome_cliente"
              error={errors.cliente?.nome_cliente?.message}
              required
            >
              <Input
                id="cliente.nome_cliente"
                placeholder="João da Silva"
                error={errors.cliente?.nome_cliente?.message}
                {...register("cliente.nome_cliente")}
              />
            </FormField>

            <FormField
              label="CPF"
              htmlFor="cliente.cpf"
              error={errors.cliente?.cpf?.message}
              required
            >
              <Input
                id="cliente.cpf"
                placeholder="000.000.000-00"
                error={errors.cliente?.cpf?.message}
                {...register("cliente.cpf")}
              />
            </FormField>

            <FormField
              label="RG"
              htmlFor="cliente.rg"
              error={errors.cliente?.rg?.message}
              required
            >
              <Input
                id="cliente.rg"
                placeholder="0000000"
                error={errors.cliente?.rg?.message}
                {...register("cliente.rg")}
              />
            </FormField>

            <FormField
              label="Data de Nascimento"
              htmlFor="cliente.data_nascimento"
              error={errors.cliente?.data_nascimento?.message}
              required
            >
              <Input
                id="cliente.data_nascimento"
                type="date"
                error={errors.cliente?.data_nascimento?.message}
                {...register("cliente.data_nascimento")}
              />
            </FormField>

            <FormField
              label="Telefone"
              htmlFor="cliente.telefone_cliente"
              error={errors.cliente?.telefone_cliente?.message}
              required
            >
              <Input
                id="cliente.telefone_cliente"
                placeholder="(85) 99999-9999"
                error={errors.cliente?.telefone_cliente?.message}
                {...register("cliente.telefone_cliente")}
              />
            </FormField>

            <FormField
              label="E-mail"
              htmlFor="cliente.email_cliente"
              error={errors.cliente?.email_cliente?.message}
              required
            >
              <Input
                id="cliente.email_cliente"
                type="email"
                placeholder="cliente@email.com"
                error={errors.cliente?.email_cliente?.message}
                {...register("cliente.email_cliente")}
              />
            </FormField>
          </div>
        </fieldset>

        {/* Endereço do Cliente */}
        <fieldset className="form-section space-y-4">
          <legend>Endereço do Cliente</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              label="Logradouro"
              htmlFor="endereco_cliente.logradouro_cliente"
              error={errors.endereco_cliente?.logradouro_cliente?.message}
              required
            >
              <Input
                id="endereco_cliente.logradouro_cliente"
                placeholder="Rua das Flores"
                error={errors.endereco_cliente?.logradouro_cliente?.message}
                {...register("endereco_cliente.logradouro_cliente")}
              />
            </FormField>

            <FormField
              label="Número"
              htmlFor="endereco_cliente.numero_casa_cliente"
              error={errors.endereco_cliente?.numero_casa_cliente?.message}
              required
            >
              <Input
                id="endereco_cliente.numero_casa_cliente"
                placeholder="123"
                error={errors.endereco_cliente?.numero_casa_cliente?.message}
                {...register("endereco_cliente.numero_casa_cliente")}
              />
            </FormField>

            <FormField
              label="Complemento"
              htmlFor="endereco_cliente.complemento_casa_cliente"
              error={errors.endereco_cliente?.complemento_casa_cliente?.message}
            >
              <Input
                id="endereco_cliente.complemento_casa_cliente"
                placeholder="Apt 10"
                {...register("endereco_cliente.complemento_casa_cliente")}
              />
            </FormField>

            <FormField
              label="CEP"
              htmlFor="endereco_cliente.cep_cliente"
              error={errors.endereco_cliente?.cep_cliente?.message}
              required
            >
              <Input
                id="endereco_cliente.cep_cliente"
                placeholder="60000-000"
                error={errors.endereco_cliente?.cep_cliente?.message}
                {...register("endereco_cliente.cep_cliente")}
              />
            </FormField>

            <FormField
              label="Bairro"
              htmlFor="endereco_cliente.bairro_cliente"
              error={errors.endereco_cliente?.bairro_cliente?.message}
              required
            >
              <Input
                id="endereco_cliente.bairro_cliente"
                placeholder="Centro"
                error={errors.endereco_cliente?.bairro_cliente?.message}
                {...register("endereco_cliente.bairro_cliente")}
              />
            </FormField>

            <FormField
              label="Cidade"
              htmlFor="endereco_cliente.cidade_cliente"
              error={errors.endereco_cliente?.cidade_cliente?.message}
              required
            >
              <Input
                id="endereco_cliente.cidade_cliente"
                placeholder="Fortaleza"
                error={errors.endereco_cliente?.cidade_cliente?.message}
                {...register("endereco_cliente.cidade_cliente")}
              />
            </FormField>

            <FormField
              label="Estado (UF)"
              htmlFor="endereco_cliente.estado_cliente"
              error={errors.endereco_cliente?.estado_cliente?.message}
              required
            >
              <Input
                id="endereco_cliente.estado_cliente"
                placeholder="CE"
                maxLength={2}
                className="uppercase w-24"
                error={errors.endereco_cliente?.estado_cliente?.message}
                {...register("endereco_cliente.estado_cliente")}
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
              error={errors.endereco_obra?.complemento_obra?.message}
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
              label="Nome Completo"
              htmlFor="procurador.nome_procurador"
              error={errors.procurador?.nome_procurador?.message}
              required
            >
              <Input
                id="procurador.nome_procurador"
                placeholder="Maria Souza"
                error={errors.procurador?.nome_procurador?.message}
                {...register("procurador.nome_procurador")}
              />
            </FormField>

            <FormField
              label="CPF"
              htmlFor="procurador.cpf_procurador"
              error={errors.procurador?.cpf_procurador?.message}
              required
            >
              <Input
                id="procurador.cpf_procurador"
                placeholder="000.000.000-00"
                error={errors.procurador?.cpf_procurador?.message}
                {...register("procurador.cpf_procurador")}
              />
            </FormField>

            <FormField
              label="RG"
              htmlFor="procurador.rg_procurador"
              error={errors.procurador?.rg_procurador?.message}
              required
            >
              <Input
                id="procurador.rg_procurador"
                placeholder="0000000"
                error={errors.procurador?.rg_procurador?.message}
                {...register("procurador.rg_procurador")}
              />
            </FormField>

            <FormField
              label="Telefone"
              htmlFor="procurador.telefone_procurador"
              error={errors.procurador?.telefone_procurador?.message}
              required
            >
              <Input
                id="procurador.telefone_procurador"
                placeholder="(85) 99999-9999"
                error={errors.procurador?.telefone_procurador?.message}
                {...register("procurador.telefone_procurador")}
              />
            </FormField>

            <FormField
              label="E-mail"
              htmlFor="procurador.email_procurador"
              error={errors.procurador?.email_procurador?.message}
              required
            >
              <Input
                id="procurador.email_procurador"
                type="email"
                placeholder="procurador@email.com"
                error={errors.procurador?.email_procurador?.message}
                {...register("procurador.email_procurador")}
              />
            </FormField>

            <FormField
              label="Logradouro"
              htmlFor="procurador.logradouro_procurador"
              error={errors.procurador?.logradouro_procurador?.message}
              required
            >
              <Input
                id="procurador.logradouro_procurador"
                placeholder="Rua das Flores"
                error={errors.procurador?.logradouro_procurador?.message}
                {...register("procurador.logradouro_procurador")}
              />
            </FormField>

            <FormField
              label="Número"
              htmlFor="procurador.numero_casa_procurador"
              error={errors.procurador?.numero_casa_procurador?.message}
              required
            >
              <Input
                id="procurador.numero_casa_procurador"
                placeholder="456"
                error={errors.procurador?.numero_casa_procurador?.message}
                {...register("procurador.numero_casa_procurador")}
              />
            </FormField>

            <FormField
              label="CEP"
              htmlFor="procurador.cep_procurador"
              error={errors.procurador?.cep_procurador?.message}
              required
            >
              <Input
                id="procurador.cep_procurador"
                placeholder="60000-000"
                error={errors.procurador?.cep_procurador?.message}
                {...register("procurador.cep_procurador")}
              />
            </FormField>

            <FormField
              label="Bairro"
              htmlFor="procurador.bairro_procurador"
              error={errors.procurador?.bairro_procurador?.message}
              required
            >
              <Input
                id="procurador.bairro_procurador"
                placeholder="Centro"
                error={errors.procurador?.bairro_procurador?.message}
                {...register("procurador.bairro_procurador")}
              />
            </FormField>

            <FormField
              label="Cidade"
              htmlFor="procurador.cidade_procurador"
              error={errors.procurador?.cidade_procurador?.message}
              required
            >
              <Input
                id="procurador.cidade_procurador"
                placeholder="Fortaleza"
                error={errors.procurador?.cidade_procurador?.message}
                {...register("procurador.cidade_procurador")}
              />
            </FormField>

            <FormField
              label="Estado (UF)"
              htmlFor="procurador.estado_procurador"
              error={errors.procurador?.estado_procurador?.message}
              required
            >
              <Input
                id="procurador.estado_procurador"
                placeholder="CE"
                maxLength={2}
                className="uppercase w-24"
                error={errors.procurador?.estado_procurador?.message}
                {...register("procurador.estado_procurador")}
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
            <ScrollText className="h-5 w-5" aria-hidden="true" />
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
