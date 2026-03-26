"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  FileText,
  ScrollText,
  Zap,
  ClipboardList,
  LayoutDashboard,
  Files,
} from "lucide-react";

const navItems = [
  {
    href: "/dashboard",
    label: "Painel",
    icon: LayoutDashboard,
  },
  {
    href: "/dashboard/memorial",
    label: "Memorial Descritivo",
    icon: FileText,
  },
  {
    href: "/dashboard/procuracao",
    label: "Procuração",
    icon: ScrollText,
  },
  {
    href: "/dashboard/unifilar",
    label: "Diagrama Unifilar",
    icon: Zap,
  },
  {
    href: "/dashboard/formulario",
    label: "Formulário ENEL-CE",
    icon: ClipboardList,
  },
  {
    href: "/dashboard/todos",
    label: "Todos os Documentos",
    icon: Files,
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-full w-64 flex-col border-r border-gray-200 bg-white">
      <div className="flex h-16 items-center border-b border-gray-200 px-6">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary-600">
            <Zap className="h-5 w-5 text-white" />
          </div>
          <span className="text-lg font-bold text-gray-900">ApolloDocs</span>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto p-4" aria-label="Navegação principal">
        <ul className="space-y-1" role="list">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive =
              item.href === "/dashboard"
                ? pathname === "/dashboard"
                : pathname.startsWith(item.href);

            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary-50 text-primary-700"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  )}
                  aria-current={isActive ? "page" : undefined}
                >
                  <Icon className="h-5 w-5 shrink-0" aria-hidden="true" />
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="border-t border-gray-200 p-4 text-xs text-gray-400">
        Solar ENEL-CE — Ceará, Brasil
      </div>
    </aside>
  );
}
