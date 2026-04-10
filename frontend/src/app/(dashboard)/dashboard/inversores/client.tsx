"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, FileText, Download } from "lucide-react";
import Link from "next/link";

export interface InversorModel {
  name: string;
  files: string[];
}

export interface InversorBrand {
  brand: string;
  models: InversorModel[];
}

interface InversoresClientProps {
  data: InversorBrand[];
}

export function InversoresClient({ data }: InversoresClientProps) {
  const [expandedBrands, setExpandedBrands] = useState<Record<string, boolean>>({});

  const toggleBrand = (brand: string) => {
    setExpandedBrands((prev) => ({ ...prev, [brand]: !prev[brand] }));
  };

  return (
    <div className="space-y-4">
      {data.map((brandInfo) => (
        <div key={brandInfo.brand} className="border rounded-lg bg-white overflow-hidden shadow-sm">
          <button
            onClick={() => toggleBrand(brandInfo.brand)}
            className="w-full flex justify-between items-center p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
          >
            <span className="font-semibold text-gray-900">
              {brandInfo.brand} ({brandInfo.models.length} modelos)
            </span>
            {expandedBrands[brandInfo.brand] ? (
              <ChevronUp className="w-5 h-5 text-gray-500" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-500" />
            )}
          </button>
          
          {expandedBrands[brandInfo.brand] && (
            <div className="p-4 border-t divide-y divide-gray-100">
              {brandInfo.models.map((model) => (
                <div key={model.name} className="py-4 first:pt-0 last:pb-0">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">{model.name}</h4>
                  <ul className="space-y-2">
                    {model.files.map((file) => (
                      <li key={file} className="flex items-center justify-between bg-gray-50 p-3 rounded-md">
                        <div className="flex items-center space-x-3 truncate">
                          <FileText className="w-4 h-4 text-blue-500 flex-shrink-0" />
                          <span className="text-sm text-gray-600 truncate">{file}</span>
                        </div>
                        <Link
                          href={
                            (typeof window !== "undefined" && window.location.hostname !== "localhost" 
                              ? "/backend" 
                              : "http://localhost:8000") + `/inversores/${brandInfo.brand}/${model.name}/${file}`
                          }
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-md transition-colors"
                        >
                          <Download className="w-4 h-4 mr-1.5" />
                          Baixar
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
              {brandInfo.models.length === 0 && (
                <p className="text-sm text-gray-500 text-center py-4">Nenhum certificado encontrado para esta marca.</p>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
