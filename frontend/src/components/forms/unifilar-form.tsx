"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  projetoUnifilarSchema,
  type ProjetoUnifilarFormData,
} from "@/lib/validations/unifilar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { FormField } from "@/components/ui/form-field";
import { useGenerateDoc } from "@/hooks/use-generate-doc";
import { PdfViewer } from "@/components/pdf-viewer";
import { normalizeUnifilarPayload } from "@/lib/payload/normalize";
import { Zap } from "lucide-react";

const QUANTIDADE_SISTEMAS_OPTIONS = [
  { value: "1", label: "1 sistema" },
  { value: "2", label: "2 sistemas" },
  { value: "3", label: "3 sistemas" },
];

const FASES_OPTIONS = [
  { value: "monofasico", label: "Monofásico" },
  { value: "bifasico", label: "Bifásico" },
  { value: "trifasico", label: "Trifásico" },
];

const TIPO_INVERSOR_OPTIONS = [
  { value: "string", label: "String" },
  { value: "micro", label: "Micro-inversor" },
];

export function UnifilarForm() {
  const { generate, pdfUrl, filename, isLoading, error, reset } =
    useGenerateDoc({ docType: "unifilar" });

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ProjetoUnifilarFormData>({
    resolver: zodResolver(projetoUnifilarSchema),
    defaultValues: {
      quantidade_sistemas_instalados: 1,
    },
  });

  const qtdSistemas = watch("quantidade_sistemas_instalados") ?? 1;

  function onSubmit(data: ProjetoUnifilarFormData) {
    generate(normalizeUnifilarPayload(data));
  }

  const sistemaPrefixes = (["sistema_instalado1", "sistema_instalado2", "sistema_instalado3"] as const).slice(0, qtdSistemas);

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
                {...register("disjuntor_geral_amperes", {
                  valueAsNumber: true,
                })}
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

        {/* Sistemas */}
        {sistemaPrefixes.map((prefix, i) => {
          const idx = i + 1;
          const sysErrors = errors[prefix];
          return (
            <fieldset key={prefix} className="form-section space-y-6">
              <legend>Sistema {idx}</legend>

              <div>
                <h4 className="mb-3 text-sm font-semibold text-gray-700">
                  Inversor
                </h4>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <FormField
                    label="Marca"
                    htmlFor={`${prefix}.inversor.marca_inversor`}
                    error={sysErrors?.inversor?.marca_inversor?.message}
                    required
                  >
                    <Input
                      id={`${prefix}.inversor.marca_inversor`}
                      placeholder="Growatt"
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
                      placeholder="MIN 6000TL-X"
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
                </div>
              </div>

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
                      placeholder="Canadian Solar"
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
                      placeholder="CS6R-420MS"
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
                      placeholder="Monocristalino"
                      error={sysErrors?.placa?.tipo_celula?.message}
                      {...register(`${prefix}.placa.tipo_celula`)}
                    />
                  </FormField>

                  <FormField
                    label="Voc (V)"
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
                    label="Isc (A)"
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
                      {...register(
                        `${prefix}.placa.corrente_curtocircuito`,
                        { valueAsNumber: true }
                      )}
                    />
                  </FormField>

                  <FormField
                    label="Vmpp (V)"
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
                      {...register(
                        `${prefix}.placa.tensao_maxima_potencia`,
                        { valueAsNumber: true }
                      )}
                    />
                  </FormField>

                  <FormField
                    label="Impp (A)"
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
                      {...register(
                        `${prefix}.placa.corrente_maxima_potencia`,
                        { valueAsNumber: true }
                      )}
                    />
                  </FormField>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <FormField
                  label="Quantidade de Placas"
                  htmlFor={`${prefix}.quantidade_total_placas_do_sistema.quantidade_placas`}
                  error={sysErrors?.quantidade_total_placas_do_sistema?.quantidade_placas?.message}
                  required
                >
                  <Input
                    id={`${prefix}.quantidade_total_placas_do_sistema.quantidade_placas`}
                    type="number"
                    placeholder="12"
                    error={sysErrors?.quantidade_total_placas_do_sistema?.quantidade_placas?.message}
                    {...register(
                      `${prefix}.quantidade_total_placas_do_sistema.quantidade_placas`,
                      { valueAsNumber: true }
                    )}
                  />
                </FormField>
              </div>
            </fieldset>
          );
        })}

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
            <Zap className="h-5 w-5" aria-hidden="true" />
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
