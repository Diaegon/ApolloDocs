import type { Metadata } from "next";
import Link from "next/link";
import { Header } from "@/components/layout/header";
import { FileText, ScrollText, Zap, ClipboardList, ArrowRight } from "lucide-react";

export const metadata: Metadata = {
  title: "Painel",
};

const documents = [
  {
    href: "/dashboard/memorial",
    title: "Memorial Descritivo",
    description:
      "Gere o memorial descritivo técnico do sistema fotovoltaico com cálculos de dimensionamento.",
    icon: FileText,
    color: "text-blue-600",
    bg: "bg-blue-50",
    border: "border-blue-100",
  },
  {
    href: "/dashboard/procuracao",
    title: "Procuração",
    description:
      "Gere a procuração para o representante do cliente junto à ENEL-CE.",
    icon: ScrollText,
    color: "text-green-600",
    bg: "bg-green-50",
    border: "border-green-100",
  },
  {
    href: "/dashboard/unifilar",
    title: "Diagrama Unifilar",
    description:
      "Gere o diagrama unifilar elétrico do sistema de geração fotovoltaica.",
    icon: Zap,
    color: "text-yellow-600",
    bg: "bg-yellow-50",
    border: "border-yellow-100",
  },
  {
    href: "/dashboard/formulario",
    title: "Formulário ENEL-CE",
    description:
      "Preencha e gere o formulário oficial de solicitação de acesso micro/minigeração ENEL-CE.",
    icon: ClipboardList,
    color: "text-primary-600",
    bg: "bg-primary-50",
    border: "border-primary-100",
  },
];

export default function DashboardPage() {
  return (
    <>
      <Header title="Painel" />
      <div className="p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900">
            Documentos disponíveis
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Selecione o tipo de documento que deseja gerar.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {documents.map((doc) => {
            const Icon = doc.icon;
            return (
              <Link
                key={doc.href}
                href={doc.href}
                className={`group flex flex-col gap-4 rounded-lg border p-6 transition-shadow hover:shadow-md ${doc.border} bg-white`}
              >
                <div className="flex items-start gap-4">
                  <div
                    className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-lg ${doc.bg}`}
                  >
                    <Icon
                      className={`h-6 w-6 ${doc.color}`}
                      aria-hidden="true"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900">{doc.title}</h3>
                    <p className="mt-1 text-sm text-gray-500 leading-relaxed">
                      {doc.description}
                    </p>
                  </div>
                </div>
                <div
                  className={`flex items-center gap-1 text-sm font-medium ${doc.color} group-hover:gap-2 transition-all`}
                >
                  Gerar documento
                  <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </>
  );
}
