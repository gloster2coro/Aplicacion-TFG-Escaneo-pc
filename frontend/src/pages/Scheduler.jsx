import React, { useEffect, useState } from "react";
import { toast } from "sonner";
import { Clock, Plus, Trash, Play, Pause } from "@phosphor-icons/react";
import {
  getSchedulerStatus, toggleScheduler, getSchedulerRules,
  createSchedulerRule, deleteSchedulerRule, getSchedulerEvents
} from "../lib/api";

const PROFILES = ["gaming", "oficina", "optimo"];

export default function Scheduler() {
  const [status, setStatus] = useState(null);
  const [rules, setRules] = useState([]);
  const [events, setEvents] = useState([]);
  const [name, setName] = useState("");
  const [triggers, setTriggers] = useState("");
  const [profile, setProfile] = useState("gaming");
  const [priority, setPriority] = useState(10);

  const refresh = async () => {
    try {
      const [s, r, e] = await Promise.all([
        getSchedulerStatus(),
        getSchedulerRules(),
        getSchedulerEvents(),
      ]);
      setStatus(s);
      setRules(r.rules);
      setEvents(e.events);
    } catch (err) { /* ignore */ }
  };

  useEffect(() => {
    refresh();
    const t = setInterval(refresh, 5000);
    return () => clearInterval(t);
  }, []);

  const handleToggle = async () => {
    try {
      const r = await toggleScheduler(!status?.enabled);
      setStatus(r);
      toast.success(r.enabled ? "Scheduler ACTIVADO" : "Scheduler DETENIDO");
    } catch (e) {
      toast.error("Error");
    }
  };

  const handleCreate = async () => {
    if (!name.trim() || !triggers.trim()) {
      toast.error("Rellena nombre y procesos trigger");
      return;
    }
    try {
      const triggerList = triggers.split(",").map(t => t.trim()).filter(Boolean);
      await createSchedulerRule({
        name, trigger_processes: triggerList, profile, priority: Number(priority), enabled: true
      });
      toast.success("Regla creada");
      setName(""); setTriggers(""); setPriority(10);
      await refresh();
    } catch (e) {
      toast.error("Error al crear regla");
    }
  };

  const handleDelete = async (id) => {
    await deleteSchedulerRule(id);
    toast.success("Regla eliminada");
    await refresh();
  };

  return (
    <div className="px-4 md:px-8 py-8 max-w-7xl mx-auto fade-in" data-testid="page-scheduler">
      <div className="mb-8">
        <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-[#007AFF] mb-3">
          // AUTO_SCHEDULER
        </div>
        <h1 className="font-heading text-4xl sm:text-5xl font-black uppercase tracking-tighter leading-none">
          Scheduler <span className="text-[#007AFF]">Automático</span>
        </h1>
        <p className="text-zinc-400 mt-3 max-w-2xl text-sm">
          Define reglas que aplicarán perfiles automáticamente cuando ciertos procesos se inicien.
          Por ejemplo: al detectar <span className="font-mono text-[#FF3B30]">steam.exe</span> activa el perfil Gaming.
        </p>
      </div>

      {/* Status bar */}
      <div className="card-tactical p-5 mb-6 flex flex-wrap items-center justify-between gap-3" data-testid="scheduler-status">
        <div className="flex items-center gap-4">
          <div className={`w-3 h-3 rounded-full ${status?.enabled ? "bg-[#10B981] pulse-slow" : "bg-zinc-700"}`}></div>
          <div>
            <div className="font-heading text-lg font-bold uppercase tracking-wider">
              {status?.enabled ? "SCHEDULER ACTIVO" : "SCHEDULER DETENIDO"}
            </div>
            <div className="text-xs font-mono text-zinc-500 mt-0.5">
              Polling cada {status?.interval_seconds || 15}s · {rules.filter(r => r.enabled).length} reglas activas
            </div>
          </div>
        </div>
        <button
          onClick={handleToggle}
          data-testid="btn-toggle-scheduler"
          className={`btn-tactical ${status?.enabled ? "btn-gaming" : ""}`}
        >
          {status?.enabled ? (
            <><Pause size={14} weight="bold" className="inline mr-2" /> DETENER</>
          ) : (
            <><Play size={14} weight="bold" className="inline mr-2" /> INICIAR</>
          )}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Create rule */}
        <div className="card-tactical p-5" data-testid="create-rule-panel">
          <div className="flex items-center gap-2 mb-4">
            <Plus size={20} className="text-[#007AFF]" weight="bold" />
            <h2 className="font-heading text-lg font-bold uppercase tracking-wider">Nueva Regla</h2>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-[10px] font-mono uppercase tracking-widest text-zinc-400 mb-2">Nombre</label>
              <input
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="ej: Gaming al abrir Steam"
                data-testid="rule-name-input"
                className="w-full bg-black border border-zinc-800 px-3 py-2 font-mono text-sm text-zinc-200 focus:border-[#007AFF] outline-none"
              />
            </div>
            <div>
              <label className="block text-[10px] font-mono uppercase tracking-widest text-zinc-400 mb-2">
                Procesos Trigger (separados por coma)
              </label>
              <input
                value={triggers}
                onChange={e => setTriggers(e.target.value)}
                placeholder="steam.exe, epicgameslauncher.exe"
                data-testid="rule-triggers-input"
                className="w-full bg-black border border-zinc-800 px-3 py-2 font-mono text-sm text-zinc-200 focus:border-[#007AFF] outline-none"
              />
            </div>
            <div>
              <label className="block text-[10px] font-mono uppercase tracking-widest text-zinc-400 mb-2">Perfil a Aplicar</label>
              <div className="flex gap-2">
                {PROFILES.map(p => (
                  <button
                    key={p}
                    onClick={() => setProfile(p)}
                    data-testid={`rule-profile-${p}`}
                    className={`flex-1 px-3 py-2 font-heading uppercase tracking-widest text-xs font-bold border ${
                      profile === p
                        ? "border-[#007AFF] text-[#007AFF] bg-[#007AFF]/10"
                        : "border-zinc-800 text-zinc-500 hover:border-zinc-600"
                    }`}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="block text-[10px] font-mono uppercase tracking-widest text-zinc-400 mb-2">
                Prioridad (mayor = se evalúa antes)
              </label>
              <input
                type="number"
                value={priority}
                onChange={e => setPriority(e.target.value)}
                data-testid="rule-priority-input"
                className="w-full bg-black border border-zinc-800 px-3 py-2 font-mono text-sm text-zinc-200 focus:border-[#007AFF] outline-none"
              />
            </div>
            <button
              onClick={handleCreate}
              data-testid="btn-create-rule"
              className="btn-tactical w-full"
            >
              CREAR REGLA
            </button>
          </div>
        </div>

        {/* Rules list */}
        <div className="card-tactical p-5" data-testid="rules-list">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Clock size={20} className="text-[#F59E0B]" weight="bold" />
              <h2 className="font-heading text-lg font-bold uppercase tracking-wider">Reglas</h2>
            </div>
            <span className="text-xs font-mono text-zinc-500">{rules.length} TOTAL</span>
          </div>
          {rules.length === 0 ? (
            <div className="font-mono text-xs text-zinc-500 py-8 text-center">
              // NO_RULES_CONFIGURED
            </div>
          ) : (
            <div className="space-y-2 max-h-[400px] overflow-y-auto">
              {rules.map((rule) => (
                <div key={rule.id} className="border border-zinc-800 p-3 hover:border-zinc-700" data-testid={`rule-${rule.id}`}>
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="font-bold text-sm">{rule.name}</div>
                      <div className="text-[10px] font-mono text-zinc-500 mt-1">
                        TRIGGER: {rule.trigger_processes.join(", ")}
                      </div>
                      <div className="text-[10px] font-mono mt-1">
                        <span className="text-[#007AFF] uppercase">→ {rule.profile}</span>
                        <span className="text-zinc-600 ml-2">P{rule.priority}</span>
                      </div>
                    </div>
                    <button
                      onClick={() => handleDelete(rule.id)}
                      data-testid={`btn-delete-rule-${rule.id}`}
                      className="p-1.5 border border-zinc-800 text-zinc-500 hover:border-[#FF3B30] hover:text-[#FF3B30]"
                    >
                      <Trash size={14} weight="bold" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Recent events */}
      <div className="card-tactical p-5 mt-6" data-testid="scheduler-events">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-heading text-lg font-bold uppercase tracking-wider">Actividad Reciente</h2>
          <span className="text-xs font-mono text-zinc-500">{events.length} EVENTOS</span>
        </div>
        {events.length === 0 ? (
          <div className="font-mono text-xs text-zinc-500">// NO_EVENTS_YET - ACTIVA_EL_SCHEDULER_PARA_EMPEZAR</div>
        ) : (
          <div className="space-y-1 font-mono text-xs max-h-60 overflow-y-auto">
            {events.map((ev, i) => (
              <div key={i} className="flex items-center gap-3 py-1 border-b border-zinc-900 last:border-0">
                <span className="text-[#10B981]">▶</span>
                <span className="text-zinc-400">{ev.rule_name}</span>
                <span className="text-[#007AFF]">{ev.profile}</span>
                <span className="text-zinc-600">· {ev.processes_affected} procs</span>
                {ev.simulated && <span className="text-[#F59E0B]">SIM</span>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
