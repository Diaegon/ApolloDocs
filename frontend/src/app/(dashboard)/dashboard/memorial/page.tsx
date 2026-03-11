import type { Metadata } from "next";
import { Header } from "@/components/layout/header";
import { MemorialForm } from "@/components/forms/memorial-form";

export const metadata: Metadata = {
  title: "Memorial Descritivo",
};

export default function MemorialPage() {
  return (
    <>
      <Header title="Memorial Descritivo" />
      <div className="p-6">
        <div className="mb-6">
          <p className="text-sm text-gray-500">
            Preencha os dados do projeto para gerar o memorial descritivo
            técnico do sistema fotovoltaico.
          </p>
        </div>
        <MemorialForm />
      </div>
    </>
  );
}
