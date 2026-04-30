import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { GameController, Briefcase, Lightning, Cpu, HardDrives, Database, Pulse as Activity } from "@phosphor-icons/react";
import { toast } from "sonner";
import ProfileCard from "../components/ProfileCard";
import MetricCard from "../components/MetricCard";
import { getHardwareMetrics, getCurrentProfile, applyOptimization, analyzeProfile } from "../lib/api";

const PROFILES = [
  {
    profile: "gaming",
    title: "Gaming",
    subtitle: "Max Performance",
    description: "Cierra procesos no esenciales, desactiva efectos visuales y activa el plan de alto rendimiento. Ideal para exprimir cada FPS.",
    icon: GameController,
    color: "#FF3B30",
  },
  {
    profile: "oficina",
    title: "Oficina",
    subtitle: "Balanced Productivity",
    description: "Rendimiento equilibrado con efectos visuales activos. Optimiza sin sacrificar la experiencia de usuario en tareas de ofimática.",
    icon: Briefcase,
    color: "#F4F4F5",
  },
  {
    profile: "optimo",
    title: "Óptimo",
    subtitle: "Auto Balance",
    description: "Balance general automático. Optimización moderada recomendada para uso diario sin configuración manual.",
    icon: Lightning,
    color: "#007AFF",
  },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const [metrics, setMetrics] = useState(null);
  const [currentProfile, setCurrentProfile] = useState(null);
  const [selected, setSelected] = useState(null);
  const [applying, setApplying] = useState(false);

  useEffect(() => {
    getCurrentProfile().then(r => {
      setCurrentProfile(r.profile);
      if (r.profile) setSelected(r.profile);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    let active = true;
    const tick = async () => {
      try {
        const m = await getHardwareMetrics();
        if (active) setMetrics(m);
      } catch (e) { /* ignore */ }
    };
    tick();
    const interval = setInterval(tick, 2000);
    return () => { active = false; clearInterval(interval); };
  }, []);

  const handleApply = async () => {
    if (!selected) return;
    setApplying(true);
    try {
      toast.loading("Analizando sistema y aplicando optimizaciones...", { id: "apply" });
      const analysis = await analyzeProfile(selected);
      const result = await applyOptimization(selected, true);
      toast.success(
        `Perfil "${selected}" aplicado. ${result.processes_affected} procesos afectados. Punto de restauración creado automáticamente.`,
        { id: "apply", duration: 5000 }
      );
      setCurrentProfile(selected);
      // Navigate to optimizer page to show details
      navigate("/optimize", { state: { analysis, result } });
    } catch (e) {
      toast.error("Error al aplicar optimización", { id: "apply" });
    } finally {
      setApplying(false);
    }
  };

  return (
    <div className="px-4 md:px-8 py-8 max-w-7xl mx-auto fade-in">
      {/* Hero */}
      <div className="mb-12" data-testid="dashboard-hero">
        <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-[#007AFF] mb-3">
          // SYSTEM CONTROL
        </div>
        <h1 className="font-heading text-5xl sm:text-6xl font-black uppercase tracking-tighter leading-none mb-4">
          Command<br />
          <span className="text-[#007AFF]">Your Machine</span>
        </h1>
        <p className="text-zinc-400 max-w-2xl text-base leading-relaxed">
          Selecciona un perfil de optimización, escanea tus drivers, y consulta al asistente IA
          para obtener recomendaciones tácticas sobre tu hardware.
        </p>
        {currentProfile && (
          <div className="mt-4 inline-flex items-center gap-2 px-3 py-1.5 border border-[#10B981] bg-[#10B981]/10 text-[#10B981] font-mono text-xs uppercase tracking-widest" data-testid="current-profile-badge">
            <span className="w-2 h-2 bg-[#10B981] rounded-full pulse-slow"></span>
            PERFIL ACTIVO: {currentProfile}
          </div>
        )}
      </div>

      {/* Profile selector */}
      <section className="mb-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-heading text-2xl font-bold uppercase tracking-tight">
            SELECCIONA TU PERFIL
          </h2>
          <div className="text-xs font-mono text-zinc-500 uppercase tracking-widest">
            3 PROFILES AVAILABLE
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {PROFILES.map(p => (
            <ProfileCard
              key={p.profile}
              {...p}
              selected={selected === p.profile}
              onSelect={setSelected}
              testid={`profile-card-${p.profile}`}
            />
          ))}
        </div>
        <div className="mt-6 flex flex-col sm:flex-row items-start sm:items-center gap-4 justify-between">
          <div className="text-xs text-zinc-500 font-mono">
            {selected
              ? `> PROFILE_SELECTED: ${selected.toUpperCase()} // PRESS APPLY TO EXECUTE`
              : "> SELECT_A_PROFILE_TO_CONTINUE..."
            }
          </div>
          <button
            onClick={handleApply}
            disabled={!selected || applying}
            data-testid="btn-apply-profile"
            className="btn-tactical glow-primary"
          >
            {applying ? "APLICANDO..." : "APLICAR OPTIMIZACIÓN →"}
          </button>
        </div>
      </section>

      {/* Real-time metrics */}
      <section className="mb-12" data-testid="metrics-section">
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-heading text-2xl font-bold uppercase tracking-tight">
            MÉTRICAS EN TIEMPO REAL
          </h2>
          <div className="text-xs font-mono text-zinc-500 uppercase tracking-widest flex items-center gap-2">
            <span className="w-2 h-2 bg-[#10B981] rounded-full pulse-slow"></span>
            LIVE · 2s REFRESH
          </div>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            label="CPU USAGE"
            value={metrics ? metrics.cpu_percent.toFixed(1) : "--"}
            unit="%"
            percent={metrics?.cpu_percent}
            color="#007AFF"
            icon={Cpu}
            testid="metric-cpu"
          />
          <MetricCard
            label="MEMORY"
            value={metrics ? metrics.memory_used_gb.toFixed(1) : "--"}
            unit={`/ ${metrics?.memory_total_gb?.toFixed(0) || "--"} GB`}
            percent={metrics?.memory_percent}
            color="#FF3B30"
            icon={Database}
            testid="metric-memory"
          />
          <MetricCard
            label="DISK"
            value={metrics ? metrics.disk_used_gb.toFixed(0) : "--"}
            unit={`/ ${metrics?.disk_total_gb?.toFixed(0) || "--"} GB`}
            percent={metrics?.disk_percent}
            color="#F59E0B"
            icon={HardDrives}
            testid="metric-disk"
          />
          <MetricCard
            label="PROCESSES"
            value={metrics ? metrics.processes_count : "--"}
            color="#10B981"
            icon={Activity}
            testid="metric-processes"
          />
        </div>

        {metrics?.cpu_per_core && (
          <div className="mt-6 card-tactical p-5" data-testid="cpu-cores">
            <div className="flex items-center justify-between mb-4">
              <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500">
                CPU CORES · PER-CORE UTILIZATION
              </div>
              <div className="text-xs font-mono text-zinc-400">
                {metrics.cpu_per_core.length} CORES
              </div>
            </div>
            <div className="grid grid-cols-4 sm:grid-cols-8 md:grid-cols-12 gap-2">
              {metrics.cpu_per_core.map((c, i) => (
                <div key={i} className="text-center">
                  <div className="text-[9px] font-mono text-zinc-500">C{i}</div>
                  <div
                    className="mt-1 h-20 border border-zinc-800 bg-black relative flex items-end"
                  >
                    <div
                      className="w-full transition-all duration-500"
                      style={{
                        height: `${c}%`,
                        background: c > 80 ? "#FF3B30" : c > 50 ? "#F59E0B" : "#007AFF"
                      }}
                    />
                  </div>
                  <div className="text-[9px] font-mono text-zinc-400 mt-1">{c.toFixed(0)}%</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Quick actions */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={() => navigate("/drivers")}
          data-testid="quick-drivers"
          className="card-tactical p-6 text-left hover:border-[#007AFF]"
        >
          <HardDrives size={32} weight="bold" className="text-[#007AFF] mb-3" />
          <div className="font-heading text-xl font-bold uppercase">Gestión Drivers</div>
          <div className="text-sm text-zinc-500 mt-1">Escanea y actualiza drivers</div>
        </button>
        <button
          onClick={() => navigate("/ai")}
          data-testid="quick-ai"
          className="card-tactical p-6 text-left hover:border-[#007AFF]"
        >
          <Cpu size={32} weight="bold" className="text-[#10B981] mb-3" />
          <div className="font-heading text-xl font-bold uppercase">Asistente IA</div>
          <div className="text-sm text-zinc-500 mt-1">Recomendaciones GPT-5.2</div>
        </button>
        <button
          onClick={() => navigate("/restore")}
          data-testid="quick-restore"
          className="card-tactical p-6 text-left hover:border-[#007AFF]"
        >
          <Activity size={32} weight="bold" className="text-[#F59E0B] mb-3" />
          <div className="font-heading text-xl font-bold uppercase">Restauración</div>
          <div className="text-sm text-zinc-500 mt-1">Puntos de restauración</div>
        </button>
      </section>
    </div>
  );
}
