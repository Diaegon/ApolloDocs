"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  projetoTodosSchema,
  type ProjetoTodosFormData,
} from "@/lib/validations/todos";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { FormField } from "@/components/ui/form-field";
import { useGenerateDoc } from "@/hooks/use-generate-doc";
import { normalizeTodosPayload } from "@/lib/payload/normalize";
import { FileArchive, Sparkles } from "lucide-react";
import { SistemaSection } from "@/components/forms/shared/sistema-section";
import {
  FASES_OPTIONS,
  CLASSE_CONSUMO_OPTIONS,
  RAMAL_OPTIONS,
  QUANTIDADE_SISTEMAS_OPTIONS,
} from "@/components/forms/shared/form-options";

export function TodosForm() {
  const { generate, pdfUrl, filename, isLoading, error, reset } =
    useGenerateDoc({ docType: "todos" });

  const {
    register,
    handleSubmit,
    watch,
    reset: resetForm,
    formState: { errors },
  } = useForm<ProjetoTodosFormData>({
    resolver: zodResolver(projetoTodosSchema),
    defaultValues: {
      quantidade_sistemas_instalados: 1,
    },
  });

  const qtdSistemas = watch("quantidade_sistemas_instalados") ?? 1;

  function onSubmit(data: ProjetoTodosFormData) {
    generate(normalizeTodosPayload(data));
  }

  function fillDevData() {
    resetForm({
      nome_projetista: "Eng. Teste",
      cft_crea_projetista: "123456",
      numero_unidade_consumidora: "123456789",
      data_projeto: "2026-01-15",
      carga_instalada_kw: 5.5,
      disjuntor_geral_amperes: 40,
      energia_media_mensal_kwh: 350,
      tensao_local: 220,
      potencia_geracao: 5000,
      classe_consumo: "residencial",
      tipo_fornecimento: "monofasico",
      ramal_energia: "aereo",
      quantidade_sistemas_instalados: 1,
      cliente: {
        nome_cliente: "João Tester",
        cpf: "123.456.789-00",
        rg: "1234567",
        data_nascimento: "1990-01-01",
        telefone_cliente: "(85) 99999-9999",
        email_cliente: "joao@teste.com"
      },
      endereco_cliente: {
        logradouro_cliente: "Rua Teste",
        numero_casa_cliente: "123",
        cep_cliente: "60000-000",
        bairro_cliente: "Centro",
        cidade_cliente: "Fortaleza",
        estado_cliente: "CE"
      },
      endereco_obra: {
        logradouro_obra: "Rua Obra",
        numero_obra: "456",
        cep_obra: "60000-000",
        bairro_obra: "Aldeota",
        cidade_obra: "Fortaleza",
        estado_obra: "CE"
      },
      procurador: {
        nome_procurador: "Procurador Teste",
        cpf_procurador: "987.654.321-00",
        rg_procurador: "7654321",
        telefone_procurador: "(85) 88888-8888",
        email_procurador: "procurador@teste.com",
        logradouro_procurador: "Av Procurador",
        numero_casa_procurador: "789",
        cep_procurador: "60000-000",
        bairro_procurador: "Meireles",
        cidade_procurador: "Fortaleza",
        estado_procurador: "CE"
      },
      sistema_instalado1: {
        inversor: {
          marca_inversor: "Growatt",
          modelo_inversor: "MIN 6000TL-X",
          potencia_inversor: 6,
          numero_fases: "monofasico",
          tipo_de_inversor: "string",
        },
        quantidade_inversor: 1,
        placa: {
          marca_placa: "Canadian",
          modelo_placa: "CS6R",
          potencia_placa: 420,
          tipo_celula: "Mono",
          tensao_pico: 49.1,
          corrente_curtocircuito: 11.2,
          tensao_maxima_potencia: 41.3,
          corrente_maxima_potencia: 10.1,
        },
        quantidade_total_placas_do_sistema: {
          quantidade_placas: 12,
        },
      },
    } as ProjetoTodosFormData);
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
        {/* Informações Institucionais (Projetista) */}
        <fieldset className="form-section space-y-4">
          <legend>Dados do Projetista</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <FormField label="Nome do Projetista" htmlFor="nome_projetista" error={errors.nome_projetista?.message} required>
              <Input id="nome_projetista" placeholder="Nome Completo" {...register("nome_projetista")} />
            </FormField>
            <FormField label="CFT / CREA" htmlFor="cft_crea_projetista" error={errors.cft_crea_projetista?.message} required>
              <Input id="cft_crea_projetista" placeholder="Número do Registro" {...register("cft_crea_projetista")} />
            </FormField>
          </div>
        </fieldset>

        {/* Informações do Projeto */}
        <fieldset className="form-section space-y-4">
          <legend>Informações do Projeto</legend>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <FormField label="Número da UC" htmlFor="numero_unidade_consumidora" error={errors.numero_unidade_consumidora?.message} required>
              <Input id="numero_unidade_consumidora" {...register("numero_unidade_consumidora")} />
            </FormField>
            <FormField label="Data do Projeto" htmlFor="data_projeto" error={errors.data_projeto?.message} required>
              <Input type="date" {...register("data_projeto")} />
            </FormField>
            <FormField label="Carga Instalada (kW)" htmlFor="carga_instalada_kw" error={errors.carga_instalada_kw?.message} required>
              <Input type="number" step="0.01" {...register("carga_instalada_kw", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Disjuntor Geral (A)" htmlFor="disjuntor_geral_amperes" error={errors.disjuntor_geral_amperes?.message} required>
              <Input type="number" {...register("disjuntor_geral_amperes", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Energia Média Mensal (kWh)" htmlFor="energia_media_mensal_kwh" error={errors.energia_media_mensal_kwh?.message} required>
              <Input type="number" step="0.01" {...register("energia_media_mensal_kwh", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Tensão Local (V)" htmlFor="tensao_local" error={errors.tensao_local?.message} required>
              <Input type="number" {...register("tensao_local", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Potência de Geração" htmlFor="potencia_geracao" error={errors.potencia_geracao?.message} required>
              <Input type="number" {...register("potencia_geracao", { valueAsNumber: true })} />
            </FormField>
            <FormField label="Classe de Consumo" htmlFor="classe_consumo" error={errors.classe_consumo?.message} required>
              <Select options={[...CLASSE_CONSUMO_OPTIONS]} {...register("classe_consumo")} />
            </FormField>
            <FormField label="Tipo de Fornecimento" htmlFor="tipo_fornecimento" error={errors.tipo_fornecimento?.message} required>
              <Select options={[...FASES_OPTIONS]} {...register("tipo_fornecimento")} />
            </FormField>
            <FormField label="Ramal de Energia" htmlFor="ramal_energia" error={errors.ramal_energia?.message} required>
              <Select options={[...RAMAL_OPTIONS]} {...register("ramal_energia")} />
            </FormField>

            <div className="col-span-1 sm:col-span-3">
              <FormField label="Quantidade de Sistemas" htmlFor="quantidade_sistemas_instalados" error={errors.quantidade_sistemas_instalados?.message} required>
                <Select className="w-40" options={[...QUANTIDADE_SISTEMAS_OPTIONS]} {...register("quantidade_sistemas_instalados", { valueAsNumber: true })} />
              </FormField>
            </div>
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
              <Input id="cliente.cpf" {...register("cliente.cpf")} />
            </FormField>
            <FormField label="RG" htmlFor="cliente.rg" error={errors.cliente?.rg?.message} required>
              <Input id="cliente.rg" {...register("cliente.rg")} />
            </FormField>
            <FormField label="Data de Nascimento" htmlFor="cliente.data_nascimento" error={errors.cliente?.data_nascimento?.message} required>
              <Input type="date" {...register("cliente.data_nascimento")} />
            </FormField>
            <FormField label="Telefone" htmlFor="cliente.telefone_cliente" error={errors.cliente?.telefone_cliente?.message} required>
              <Input id="cliente.telefone_cliente" {...register("cliente.telefone_cliente")} />
            </FormField>
            <FormField label="E-mail" htmlFor="cliente.email_cliente" error={errors.cliente?.email_cliente?.message} required>
              <Input type="email" {...register("cliente.email_cliente")} />
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

        {/* Sistemas Instalados */}
        <SistemaSection index={1} register={register} errors={errors} />
        {qtdSistemas >= 2 && <SistemaSection index={2} register={register} errors={errors} />}
        {qtdSistemas >= 3 && <SistemaSection index={3} register={register} errors={errors} />}

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
          {!pdfUrl && (
            <Button type="button" variant="secondary" size="lg" onClick={fillDevData} className="gap-2 text-indigo-600 border-indigo-200 hover:bg-indigo-50">
              <Sparkles className="h-4 w-4" />
              Preencher Teste
            </Button>
          )}
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
