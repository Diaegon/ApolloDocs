import type { Metadata } from "next";
import { Header } from "@/components/layout/header";
import { ProcuracaoForm } from "@/components/forms/procuracao-form";

export const metadata: Metadata = {
  title: "Procuração",
};

export default function ProcuracaoPage() {
  return (
    <>
      <Header title="Procuração" />
      <div className="p-6">
        <div className="mb-6">
          <p className="text-sm text-gray-500">
            Preencha os dados do cliente e do procurador para gerar a
            procuração junto à ENEL-CE.
          </p>
        </div>
        <ProcuracaoForm />
      </div>
    </>
  );
}
