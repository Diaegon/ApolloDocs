"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  projetoMemorialSchema,
  type ProjetoMemorialFormData,
} from "@/lib/validations/memorial";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { FormField } from "@/components/ui/form-field";
import { useGenerateDoc } from "@/hooks/use-generate-doc";
import { PdfViewer } from "@/components/pdf-viewer";
import { normalizeMemorialPayload } from "@/lib/payload/normalize";
import { FileText } from "lucide-react";

const FASES_OPTIONS = [
  { value: "monofasico", label: "Monofásico" },
  { value: "bifasico", label: "Bifásico" },
  { value: "trifasico", label: "Trifásico" },
];

const TIPO_INVERSOR_OPTIONS = [
  { value: "string", label: "String" },
  { value: "micro", label: "Micro-inversor" },
];

const CLASSE_CONSUMO_OPTIONS = [
  { value: "residencial", label: "Residencial" },
  { value: "comercial", label: "Comercial" },
  { value: "industrial", label: "Industrial" },
  { value: "rural", label: "Rural" },
];

const RAMAL_OPTIONS = [
  { value: "aereo", label: "Aéreo" },
  { value: "subterraneo", label: "Subterrâneo" },
];

const QUANTIDADE_SISTEMAS_OPTIONS = [
  { value: "1", label: "1 sistema" },
  { value: "2", label: "2 sistemas" },
  { value: "3", label: "3 sistemas" },
];

function SistemaSection({
  index,
  register,
  errors,
}: {
  index: 1 | 2 | 3;
  register: ReturnType<typeof useForm<ProjetoMemorialFormData>>["register"];
  errors: ReturnType<typeof useForm<ProjetoMemorialFormData>>["formState"]["errors"];
}) {
  const prefix = `sistema_instalado${index}` as
    | "sistema_instalado1"
    | "sistema_instalado2"
    | "sistema_instalado3";
  const sysErrors = errors[prefix];

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
            label="Potência (W)"
            htmlFor={`${prefix}.inversor.potencia_inversor`}
            error={sysErrors?.inversor?.potencia_inversor?.message}
            required
          >
            <Input
              id={`${prefix}.inversor.potencia_inversor`}
              type="number"
              step="0.01"
              placeholder="6000"
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
              options={FASES_OPTIONS}
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
              options={TIPO_INVERSOR_OPTIONS}
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

export function MemorialForm() {
  const { generate, pdfUrl, filename, isLoading, error, reset } =
    useGenerateDoc({ docType: "memorial" });

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ProjetoMemorialFormData>({
    resolver: zodResolver(projetoMemorialSchema),
    defaultValues: {
      quantidade_sistemas_instalados: 1,
    },
  });

  const qtdSistemas = watch("quantidade_sistemas_instalados") ?? 1;

  function onSubmit(data: ProjetoMemorialFormData) {
    generate(normalizeMemorialPayload(data));
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
        {/* Informações do Projeto */}
        <fieldset className="form-section space-y-4">
          <legend>Informações do Projeto</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField
              label="Número da UC"
              htmlFor="numero_unidade_consumidora"
              error={errors.numero_unidade_consumidora?.message}
              required
            >
              <Input
                id="numero_unidade_consumidora"
                placeholder="123456789"
                error={errors.numero_unidade_consumidora?.message}
                {...register("numero_unidade_consumidora")}
              />
            </FormField>

            <FormField
              label="Data do Projeto"
              htmlFor="data_projeto"
              error={errors.data_projeto?.message}
              required
            >
              <Input
                id="data_projeto"
                type="date"
                error={errors.data_projeto?.message}
                {...register("data_projeto")}
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
                {...register("disjuntor_geral_amperes", {
                  valueAsNumber: true,
                })}
              />
            </FormField>

            <FormField
              label="Energia Média Mensal (kWh)"
              htmlFor="energia_media_mensal_kwh"
              error={errors.energia_media_mensal_kwh?.message}
              required
            >
              <Input
                id="energia_media_mensal_kwh"
                type="number"
                step="0.01"
                placeholder="350"
                error={errors.energia_media_mensal_kwh?.message}
                {...register("energia_media_mensal_kwh", {
                  valueAsNumber: true,
                })}
              />
            </FormField>

            <FormField
              label="Classe de Consumo"
              htmlFor="classe_consumo1"
              error={errors.classe_consumo1?.message}
              required
            >
              <Select
                id="classe_consumo1"
                options={CLASSE_CONSUMO_OPTIONS}
                placeholder="Selecione"
                error={errors.classe_consumo1?.message}
                {...register("classe_consumo1")}
              />
            </FormField>

            <FormField
              label="Tipo de Fornecimento"
              htmlFor="tipo_fornecimento"
              error={errors.tipo_fornecimento?.message}
              required
            >
              <Select
                id="tipo_fornecimento"
                options={FASES_OPTIONS}
                placeholder="Selecione"
                error={errors.tipo_fornecimento?.message}
                {...register("tipo_fornecimento")}
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
              label="Quantidade de Sistemas"
              htmlFor="quantidade_sistemas_instalados"
              error={errors.quantidade_sistemas_instalados?.message}
              required
            >
              <Select
                id="quantidade_sistemas_instalados"
                options={QUANTIDADE_SISTEMAS_OPTIONS}
                error={errors.quantidade_sistemas_instalados?.message}
                {...register("quantidade_sistemas_instalados", {
                  valueAsNumber: true,
                })}
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
              htmlFor="cliente.nome_cliente"
              error={errors.cliente?.nome_cliente?.message}
            >
              <Input
                id="cliente.nome_cliente"
                placeholder="João da Silva"
                {...register("cliente.nome_cliente")}
              />
            </FormField>

            <FormField
              label="CPF"
              htmlFor="cliente.cpf"
              error={errors.cliente?.cpf?.message}
            >
              <Input
                id="cliente.cpf"
                placeholder="000.000.000-00"
                {...register("cliente.cpf")}
              />
            </FormField>

            <FormField
              label="RG"
              htmlFor="cliente.rg"
              error={errors.cliente?.rg?.message}
            >
              <Input
                id="cliente.rg"
                placeholder="0000000"
                {...register("cliente.rg")}
              />
            </FormField>

            <FormField
              label="Data de Nascimento"
              htmlFor="cliente.data_nascimento"
              error={errors.cliente?.data_nascimento?.message}
            >
              <Input
                id="cliente.data_nascimento"
                type="date"
                {...register("cliente.data_nascimento")}
              />
            </FormField>

            <FormField
              label="Telefone"
              htmlFor="cliente.telefone_cliente"
              error={errors.cliente?.telefone_cliente?.message}
            >
              <Input
                id="cliente.telefone_cliente"
                placeholder="(85) 99999-9999"
                {...register("cliente.telefone_cliente")}
              />
            </FormField>

            <FormField
              label="E-mail"
              htmlFor="cliente.email_cliente"
              error={errors.cliente?.email_cliente?.message}
            >
              <Input
                id="cliente.email_cliente"
                type="email"
                placeholder="cliente@email.com"
                {...register("cliente.email_cliente")}
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
            >
              <Input
                id="endereco_obra.logradouro_obra"
                placeholder="Rua das Flores"
                {...register("endereco_obra.logradouro_obra")}
              />
            </FormField>

            <FormField
              label="Número"
              htmlFor="endereco_obra.numero_obra"
              error={errors.endereco_obra?.numero_obra?.message}
            >
              <Input
                id="endereco_obra.numero_obra"
                placeholder="123"
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
            >
              <Input
                id="endereco_obra.cep_obra"
                placeholder="60000-000"
                {...register("endereco_obra.cep_obra")}
              />
            </FormField>

            <FormField
              label="Bairro"
              htmlFor="endereco_obra.bairro_obra"
              error={errors.endereco_obra?.bairro_obra?.message}
            >
              <Input
                id="endereco_obra.bairro_obra"
                placeholder="Centro"
                {...register("endereco_obra.bairro_obra")}
              />
            </FormField>

            <FormField
              label="Cidade"
              htmlFor="endereco_obra.cidade_obra"
              error={errors.endereco_obra?.cidade_obra?.message}
            >
              <Input
                id="endereco_obra.cidade_obra"
                placeholder="Fortaleza"
                {...register("endereco_obra.cidade_obra")}
              />
            </FormField>

            <FormField
              label="Estado (UF)"
              htmlFor="endereco_obra.estado_obra"
              error={errors.endereco_obra?.estado_obra?.message}
            >
              <Input
                id="endereco_obra.estado_obra"
                placeholder="CE"
                maxLength={2}
                className="uppercase w-24"
                {...register("endereco_obra.estado_obra")}
              />
            </FormField>
          </div>
        </fieldset>

        {/* Sistemas Instalados */}
        <SistemaSection
          index={1}
          register={register}
          errors={errors}
        />
        {qtdSistemas >= 2 && (
          <SistemaSection
            index={2}
            register={register}
            errors={errors}
          />
        )}
        {qtdSistemas >= 3 && (
          <SistemaSection
            index={3}
            register={register}
            errors={errors}
          />
        )}

        {error && (
          <div className="rounded-md bg-red-50 p-4 text-sm text-red-700" role="alert">
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
            <FileText className="h-5 w-5" aria-hidden="true" />
            {isLoading ? "Gerando PDF…" : "Gerar PDF"}
          </Button>
          {pdfUrl && (
            <Button type="button" variant="secondary" size="lg" onClick={reset}>
              Nova geração
            </Button>
          )}
        </div>
      </form>

      {pdfUrl && (
        <PdfViewer
          pdfUrl={pdfUrl}
          filename={filename}
          onClose={reset}
        />
      )}
    </div>
  );
}
