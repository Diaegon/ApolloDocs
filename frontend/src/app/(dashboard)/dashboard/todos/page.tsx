import type { Metadata } from "next";
import { Header } from "@/components/layout/header";
import { TodosForm } from "@/components/forms/todos-form";

export const metadata: Metadata = {
  title: "Todos os Documentos",
  description: "Gerar todos os documentos do projeto solar (ZIP).",
};

export default function TodosPage() {
  return (
    <>
      <Header title="Todos os Documentos" />
      <div className="p-6">
        <div className="mb-6">
          <p className="text-sm text-gray-500">
            Preencha os dados abaixo para gerar o Memorial Descritivo, Procuração, Formulário ENEL-CE e Diagrama Unifilar num único arquivo ZIP.
          </p>
        </div>
        <TodosForm />
      </div>
    </>
  );
}
