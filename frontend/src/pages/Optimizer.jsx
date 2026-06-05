import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { toast } from "sonner";
import { Warning, CheckCircle, Stop, Gear, TrendUp, TrendDown } from "@phosphor-icons/react";
import { analyzeProfile, applyOptimization, getOptimizeLogs } from "../lib/api";

const PROFILES = ["gaming", "oficina", "optimo"];

export default function Optimizer() {
  const location = useLocation();
  const initialAnalysis = location.state?.analysis;
  const initialResult = location.state?.result;

  const [profile, setProfile] = useState(initialAnalysis?.profile || "optimo");
  const [analysis, setAnalysis] = useState(initialAnalysis || null);
  const [result, setResult] = useState(initialResult || null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getOptimizeLogs().then(r => setLogs(r.logs)).catch(() => {});
  }, [result]);

  const doAnalyze = async (p) => {
    setLoading(true);
    try {
      const a = await analyzeProfile(p);
      setAnalysis(a);
      setResult(null);
    } catch (e) {
      toast.error("Error analizando");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!initialAnalysis) doAnalyze(profile);
    // eslint-disable-next-line
  }, []);

  const doApply = async () => {
    setLoading(true);
    try {
      toast.loading("Aplicando optimización...", { id: "opt" });
      const r = await applyOptimization(profile, true);
      setResult(r);
      toast.success(`Optimización aplicada. ${r.processes_affected} procesos afectados.`, { id: "opt" });
    } catch (e) {
      toast.error("Error al aplicar", { id: "opt" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="px-4 md:px-8 py-8 max-w-7xl mx-auto fade-in" data-testid="page-optimizer">
      <div className="mb-8">
        <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-[#007AFF] mb-3">
          // MOTOR_OPTIMIZACION
        </div>
        <h1 className="font-heading text-4xl sm:text-5xl font-black uppercase tracking-tighter leading-none">
          Motor de <span className="text-[#007AFF]">Optimización</span>
        </h1>
      </div>

      {/* Profile selector */}
      <div className="mb-8 flex flex-wrap gap-2" data-testid="profile-selector">
        {PROFILES.map(p => (
          <button
            key={p}
            onClick={() => { setProfile(p); doAnalyze(p); }}
            data-testid={`select-profile-${p}`}
            className={`px-5 py-2 font-heading uppercase tracking-widest text-sm font-bold border-2 transition-colors ${
              profile === p
                ? "border-[#007AFF] bg-[#007AFF]/10 text-[#007AFF]"
                : "border-zinc-800 text-zinc-500 hover:border-zinc-600"
            }`}
          >
            {p}
          </button>
        ))}
      </div>

      {analysis && (
        <>
          <section className="card-tactical p-6 mb-6" data-testid="analysis-summary">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500 mb-1">
                  RESULTADO_DEL_ANÁLISIS
                </div>
                <div className="font-heading text-2xl font-bold uppercase">{profile}</div>
                <p className="text-sm text-zinc-400 mt-2 max-w-2xl">{analysis.description}</p>
              </div>
              <button
                onClick={doApply}
                disabled={loading}
                data-testid="btn-apply-optimization"
                className="btn-tactical glow-primary"
              >
                {loading ? "EJECUTANDO..." : "EJECUTAR AHORA →"}
              </button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
              <StatBox label="Procesos a cerrar" value={analysis.processes_to_close.length} color="#FF3B30" testid="stat-processes" />
              <StatBox label="Apps de inicio" value={analysis.startup_to_disable.length} color="#F59E0B" testid="stat-startup" />
              <StatBox label="Plan de energía" value={analysis.power_plan} color="#007AFF" testid="stat-power" />
              <StatBox label="Efectos visuales" value={analysis.visual_effects} color="#A1A1AA" testid="stat-visual" />
            </div>
          </section>

          <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Processes to close */}
            <div className="card-tactical p-5" data-testid="processes-panel">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-heading text-lg font-bold uppercase tracking-wider flex items-center gap-2">
                  <Stop size={18} className="text-[#FF3B30]" weight="bold" />
                  Procesos Objetivo
                </h3>
                <span className="text-xs font-mono text-zinc-500">
                  {analysis.processes_to_close.length} ELEMENTOS
                </span>
              </div>
              <div className="max-h-80 overflow-y-auto">
                {analysis.processes_to_close.length === 0 ? (
                  <div className="text-sm text-zinc-500 font-mono">// NO_HAY_PROCESOS_OBJETIVO</div>
                ) : (
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-zinc-800 text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                        <th className="text-left py-2">Proceso</th>
                        <th className="text-right py-2">MEM %</th>
                        <th className="text-right py-2">CPU %</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysis.processes_to_close.map((p, i) => (
                        <tr key={i} className="border-b border-zinc-900 hover:bg-zinc-900/30">
                          <td className="py-2 font-mono text-xs">{p.name}</td>
                          <td className="py-2 text-right font-mono text-xs text-[#FF3B30]">{p.memory_percent?.toFixed(1)}</td>
                          <td className="py-2 text-right font-mono text-xs text-[#F59E0B]">{p.cpu_percent?.toFixed(1)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>

            {/* Startup apps */}
            <div className="card-tactical p-5" data-testid="startup-panel">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-heading text-lg font-bold uppercase tracking-wider flex items-center gap-2">
                  <Gear size={18} className="text-[#F59E0B]" weight="bold" />
                  Apps de Inicio
                </h3>
                <span className="text-xs font-mono text-zinc-500">
                  {analysis.startup_to_disable.length} ELEMENTOS
                </span>
              </div>
              <div className="max-h-80 overflow-y-auto">
                {analysis.startup_to_disable.length === 0 ? (
                  <div className="text-sm text-zinc-500 font-mono">// NO_HAY_APPS_DE_INICIO</div>
                ) : (
                  <div className="space-y-2">
                    {analysis.startup_to_disable.map((s, i) => (
                      <div key={i} className="border border-zinc-800 p-3 hover:border-zinc-700">
                        <div className="font-mono text-sm">{s.name}</div>
                        <div className="text-[10px] font-mono text-zinc-600 mt-1 truncate">{s.command}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </section>

          {result && (
            <section className="card-tactical p-6 mb-6 border-[#10B981]" data-testid="result-panel">
              <div className="flex items-center gap-3 mb-4">
                <CheckCircle size={24} className="text-[#10B981]" weight="bold" />
                <h3 className="font-heading text-xl font-bold uppercase">Resultado de la Ejecución</h3>
              </div>
              {result.simulated && (
                <div className="mb-4 p-3 border border-[#F59E0B] bg-[#F59E0B]/10 flex items-start gap-3" data-testid="simulation-warning">
                  <Warning size={20} className="text-[#F59E0B] flex-shrink-0 mt-0.5" weight="bold" />
                  <div className="text-xs font-mono text-[#F59E0B]">
                    MODO SIMULACIÓN ACTIVO · Los cambios se aplicarán realmente cuando ejecutes la app en Windows con permisos de administrador.
                  </div>
                </div>
              )}
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div><span className="text-zinc-500 font-mono text-xs">PROCESOS AFECTADOS:</span> <span className="font-bold ml-2">{result.processes_affected}</span></div>
                <div><span className="text-zinc-500 font-mono text-xs">COMANDOS SISTEMA:</span> <span className="font-bold ml-2">{result.system_commands?.length || 0}</span></div>
              </div>
              {result.system_commands && (
                <div className="mt-4 space-y-2">
                  {result.system_commands.map((c, i) => (
                    <div key={i} className="font-mono text-xs bg-black p-3 border border-zinc-800">
                      <div className="text-[#10B981]">{c.description}</div>
                      <div className="text-zinc-500 mt-1 break-all">$ {c.command}</div>
                    </div>
                  ))}
                </div>
              )}
              {result.comparison && (
                <div className="mt-6" data-testid="comparison-panel">
                  <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-[#007AFF] mb-3">
                    COMPARATIVA DE IMPACTO · ANTES → DESPUÉS
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <ComparisonCell label="CPU" data={result.comparison.cpu_percent} unit="%" testid="comp-cell-cpu" />
                    <ComparisonCell label="MEMORIA" data={result.comparison.memory_percent} unit="%" testid="comp-cell-memory" />
                    <ComparisonCell label="DISCO" data={result.comparison.disk_percent} unit="%" testid="comp-cell-disk" />
                    <ComparisonCell label="PROCESOS" data={result.comparison.processes_count} unit="" testid="comp-cell-procs" />
                  </div>
                </div>
              )}
            </section>
          )}
        </>
      )}

      {logs.length > 0 && (
        <section className="card-tactical p-5" data-testid="logs-panel">
          <h3 className="font-heading text-lg font-bold uppercase tracking-wider mb-4">HISTORIAL</h3>
          <div className="space-y-1 font-mono text-xs">
            {logs.slice(0, 10).map((l, i) => (
              <div key={i} className="flex items-center gap-3 py-1 border-b border-zinc-900">
                <span className="text-zinc-500">{new Date(l.timestamp).toLocaleString('es-ES')}</span>
                <span className="text-[#007AFF] uppercase">{l.profile}</span>
                <span className="text-zinc-400">{l.processes_affected} procs</span>
                {l.simulated && <span className="text-[#F59E0B]">SIM</span>}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

function StatBox({ label, value, color, testid }) {
  return (
    <div className="border border-zinc-800 p-4" data-testid={testid}>
      <div className="text-[10px] font-mono uppercase tracking-[0.2em] text-zinc-500">{label}</div>
      <div className="font-heading text-2xl font-bold mt-1" style={{ color }}>{value}</div>
    </div>
  );
}

function ComparisonCell({ label, data, unit, testid }) {
  const improved = data.improved;
  const color = improved ? "#10B981" : data.delta === 0 ? "#A1A1AA" : "#FF3B30";
  const Arrow = improved ? TrendDown : TrendUp;
  return (
    <div className="border border-zinc-800 p-3" data-testid={testid}>
      <div className="flex items-center justify-between mb-2">
        <div className="text-[10px] font-mono uppercase tracking-[0.2em] text-zinc-500">{label}</div>
        <Arrow size={14} weight="bold" style={{ color }} />
      </div>
      <div className="font-mono text-xs space-y-0.5">
        <div className="flex justify-between">
          <span className="text-zinc-500">ANTES</span>
          <span className="text-zinc-300">{data.before}{unit}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-zinc-500">DESPUÉS</span>
          <span className="text-zinc-300">{data.after}{unit}</span>
        </div>
        <div className="flex justify-between pt-1 border-t border-zinc-900">
          <span style={{ color }}>DELTA</span>
          <span style={{ color }}>
            {data.delta > 0 ? "+" : ""}{data.delta}{unit} ({data.delta_percent > 0 ? "+" : ""}{data.delta_percent}%)
          </span>
        </div>
      </div>
    </div>
  );
}
