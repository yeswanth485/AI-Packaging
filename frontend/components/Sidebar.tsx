"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Landing" },
  { href: "/dashboard", label: "Dashboard" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-60 flex-col border-r border-slate-800 bg-slate-950/80 px-4 py-6">
      <div className="mb-8">
        <h1 className="text-lg font-semibold tracking-tight">
          AI Packaging
        </h1>
        <p className="mt-1 text-xs text-slate-400">Automation Platform</p>
      </div>
      <nav className="flex flex-1 flex-col gap-1 text-sm">
        {navItems.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`rounded-md px-3 py-2 transition-colors ${
                active
                  ? "bg-slate-800 text-slate-50"
                  : "text-slate-300 hover:bg-slate-900 hover:text-slate-50"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
        <div className="mt-auto pt-4 text-xs text-slate-500">
          <button
            className="w-full rounded-md border border-slate-800 px-3 py-2 text-left text-xs text-slate-300 hover:bg-slate-900"
            onClick={() => {
              if (typeof window !== "undefined") {
                localStorage.removeItem("token");
                window.location.href = "/login";
              }
            }}
          >
            Log out
          </button>
        </div>
      </nav>
    </aside>
  );
}

