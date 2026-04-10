import type { Metadata } from "next";
import { Header } from "@/components/layout/header";
import { apiFetch } from "@/lib/api/client";
import { InversoresClient, InversorBrand } from "./client";

export const metadata: Metadata = {
  title: "Certificados de Inversores",
};

export default async function InversoresPage() {
  let data: InversorBrand[] | null = null;
  let error = false;

  try {
    const res = await apiFetch("/inversores/list");
    if (!res.ok) {
      throw new Error("Failed to fetch inverses");
    }
    data = await res.json();
  } catch (err) {
    console.error("Fetch inversores failed", err);
    error = true;
  }

  return (
    <>
      <Header title="Certificados de Inversores" />
      <div className="p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900">
            Biblioteca de Inversores
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Selecione a marca e o modelo para baixar o certificado INMETRO do inversor.
          </p>
        </div>

        {error && (
          <div className="text-red-600 p-4 bg-red-50 rounded-lg border border-red-100">
            Erro ao carregar a biblioteca de inversores.
          </div>
        )}

        {!error && data && <InversoresClient data={data} />}
      </div>
    </>
  );
}
