import type { Metadata } from "next";
import { Header } from "@/components/layout/header";
import { UnifilarForm } from "@/components/forms/unifilar-form";

export const metadata: Metadata = {
  title: "Diagrama Unifilar",
};

export default function UnifilarPage() {
  return (
    <>
      <Header title="Diagrama Unifilar" />
      <div className="p-6">
        <div className="mb-6">
          <p className="text-sm text-gray-500">
            Preencha os dados do sistema para gerar o diagrama unifilar elétrico
            do sistema fotovoltaico.
          </p>
        </div>
        <UnifilarForm />
      </div>
    </>
  );
}
