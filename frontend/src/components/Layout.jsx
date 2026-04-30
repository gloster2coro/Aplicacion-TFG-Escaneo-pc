import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  Gauge, Cpu, HardDrives, Robot, ShieldCheck, FileText, Lightning, Clock
} from "@phosphor-icons/react";
import { toast } from "sonner";
import { createRestorePoint, getDocsPdfUrl } from "../lib/api";

const navItems = [
  { to: "/", label: "Dashboard", icon: Gauge, testid: "nav-dashboard" },
  { to: "/optimize", label: "Optimización", icon: Lightning, testid: "nav-optimize" },
  { to: "/drivers", label: "Drivers", icon: HardDrives, testid: "nav-drivers" },
  { to: "/ai", label: "Asistente IA", icon: Robot, testid: "nav-ai" },
  { to: "/scheduler", label: "Scheduler", icon: Clock, testid: "nav-scheduler" },
  { to: "/restore", label: "Restauración", icon: ShieldCheck, testid: "nav-restore" },
];

export default function Layout({ children }) {
  const navigate = useNavigate();

  const handleRestorePoint = async () => {
    try {
      toast.loading("Creando punto de restauración...", { id: "rp" });
      const res = await createRestorePoint(
        `Optidriver manual - ${new Date().toLocaleString('es-ES')}`
      );
      toast.success(
        res.simulated
          ? "Punto de restauración creado (simulado - funciona real en Windows admin)"
          : "Punto de restauración creado con éxito",
        { id: "rp" }
      );
    } catch (e) {
      toast.error("Error al crear punto de restauración", { id: "rp" });
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-white flex flex-col">
      {/* Top nav */}
      <header className="sticky top-0 z-50 bg-black/80 backdrop-blur-md border-b border-zinc-800">
        <div className="px-6 py-4 flex items-center justify-between">
          <div
            className="flex items-center gap-3 cursor-pointer"
            onClick={() => navigate("/")}
            data-testid="header-logo"
          >
            <div className="w-10 h-10 border border-[#007AFF] flex items-center justify-center bg-[#007AFF]/10">
              <Cpu size={22} weight="bold" className="text-[#007AFF]" />
            </div>
            <div>
              <div className="font-heading text-2xl font-black uppercase tracking-tighter leading-none">
                OPTI<span className="text-[#007AFF]">DRIVER</span>
              </div>
              <div className="text-[10px] text-zinc-500 uppercase tracking-[0.3em] font-mono">
                Performance Control Center
              </div>
            </div>
          </div>

          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                data-testid={item.testid}
                className={({ isActive }) =>
                  `px-4 py-2 font-heading uppercase tracking-widest text-sm font-bold border transition-colors ${
                    isActive
                      ? "border-[#007AFF] text-[#007AFF] bg-[#007AFF]/10"
                      : "border-transparent text-zinc-400 hover:text-white hover:border-zinc-700"
                  }`
                }
              >
                <span className="flex items-center gap-2">
                  <item.icon size={16} weight="bold" />
                  {item.label}
                </span>
              </NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <a
              href={getDocsPdfUrl()}
              target="_blank"
              rel="noopener noreferrer"
              data-testid="btn-download-pdf"
              className="hidden md:flex items-center gap-2 px-3 py-2 border border-zinc-700 hover:border-zinc-500 text-zinc-300 hover:text-white font-heading uppercase text-xs tracking-widest font-bold transition-colors"
            >
              <FileText size={14} weight="bold" /> PDF
            </a>
            <button
              onClick={handleRestorePoint}
              data-testid="btn-create-restore-point"
              className="btn-tactical text-xs flex items-center gap-2"
            >
              <ShieldCheck size={16} weight="bold" />
              <span className="hidden sm:inline">Restore Point</span>
            </button>
          </div>
        </div>

        {/* Mobile nav */}
        <nav className="lg:hidden flex items-center gap-1 px-4 pb-3 overflow-x-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              data-testid={`mobile-${item.testid}`}
              className={({ isActive }) =>
                `px-3 py-1.5 font-heading uppercase tracking-wider text-xs font-bold border whitespace-nowrap ${
                  isActive
                    ? "border-[#007AFF] text-[#007AFF] bg-[#007AFF]/10"
                    : "border-zinc-800 text-zinc-400"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </header>

      <main className="flex-1 grid-bg">
        {children}
      </main>

      <footer className="border-t border-zinc-800 bg-black/60 py-4 px-6">
        <div className="flex items-center justify-between text-xs text-zinc-500 font-mono">
          <span>OPTIDRIVER v1.0 · LOCAL_MODE</span>
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 bg-[#10B981] rounded-full pulse-slow"></span>
            SYSTEM_ONLINE
          </span>
        </div>
      </footer>
    </div>
  );
}
