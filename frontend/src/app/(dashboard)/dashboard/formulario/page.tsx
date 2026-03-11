import type { Metadata } from "next";
import { Header } from "@/components/layout/header";
import { FormularioForm } from "@/components/forms/formulario-form";

export const metadata: Metadata = {
  title: "Formulário ENEL-CE",
};

export default function FormularioPage() {
  return (
    <>
      <Header title="Formulário ENEL-CE" />
      <div className="p-6">
        <div className="mb-6">
          <p className="text-sm text-gray-500">
            Preencha os dados para gerar o formulário oficial de solicitação de
            acesso de micro/minigeração da ENEL-CE.
          </p>
        </div>
        <FormularioForm />
      </div>
    </>
  );
}
