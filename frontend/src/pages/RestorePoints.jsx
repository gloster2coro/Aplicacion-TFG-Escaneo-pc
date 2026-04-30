import React, { useEffect, useState } from "react";
import { toast } from "sonner";
import { ShieldCheck, Plus, ClockCounterClockwise } from "@phosphor-icons/react";
import { createRestorePoint, getRestoreHistory } from "../lib/api";

export default function RestorePoints() {
  const [history, setHistory] = useState([]);
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const load = async () => {
    try {
      const r = await getRestoreHistory();
      setHistory(r.restore_points);
    } catch (e) { /* ignore */ }
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    if (!description.trim()) {
      toast.error("Introduce una descripción");
      return;
    }
    setLoading(true);
    try {
      toast.loading("Creando punto de restauración...", { id: "rp" });
      await createRestorePoint(description);
      toast.success("Punto de restauración creado", { id: "rp" });
      setDescription("");
      await load();
    } catch (e) {
      toast.error("Error al crear punto", { id: "rp" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="px-4 md:px-8 py-8 max-w-7xl mx-auto fade-in" data-testid="page-restore">
      <div className="mb-8">
        <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-[#F59E0B] mb-3">
          // SYSTEM_RESTORE
        </div>
        <h1 className="font-heading text-4xl sm:text-5xl font-black uppercase tracking-tighter leading-none">
          Puntos de <span className="text-[#F59E0B]">Restauración</span>
        </h1>
        <p className="text-zinc-400 mt-3 max-w-2xl text-sm">
          Crea snapshots del sistema antes de aplicar cambios críticos. Optidriver los crea automáticamente
          antes de cada optimización y actualización de drivers.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Create */}
        <div className="card-tactical p-5" data-testid="create-restore-panel">
          <div className="flex items-center gap-2 mb-4">
            <Plus size={20} className="text-[#F59E0B]" weight="bold" />
            <h2 className="font-heading text-lg font-bold uppercase tracking-wider">Crear Punto</h2>
          </div>
          <label className="block text-xs font-mono uppercase tracking-widest text-zinc-400 mb-2">
            Descripción
          </label>
          <input
            value={description}
            onChange={e => setDescription(e.target.value)}
            placeholder="ej: Antes de instalar driver NVIDIA"
            data-testid="restore-description-input"
            className="w-full bg-black border border-zinc-800 px-3 py-2 font-mono text-sm text-zinc-200 focus:border-[#F59E0B] outline-none mb-4"
          />
          <button
            onClick={handleCreate}
            disabled={loading || !description.trim()}
            data-testid="btn-create-manual-restore"
            className="btn-tactical w-full"
            style={{ borderColor: "#F59E0B", color: "#F59E0B" }}
          >
            <ShieldCheck size={16} weight="bold" className="inline mr-2" />
            {loading ? "CREANDO..." : "CREAR AHORA"}
          </button>

          <div className="mt-6 pt-6 border-t border-zinc-800 font-mono text-xs text-zinc-500 space-y-2">
            <div>// AUTO-RESTORE:</div>
            <div>→ Antes de optimización</div>
            <div>→ Antes de actualizar drivers</div>
            <div>// Requiere Windows admin para ser real</div>
          </div>
        </div>

        {/* History */}
        <div className="lg:col-span-2 card-tactical p-5" data-testid="restore-history">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <ClockCounterClockwise size={20} className="text-[#007AFF]" weight="bold" />
              <h2 className="font-heading text-lg font-bold uppercase tracking-wider">Historial</h2>
            </div>
            <span className="text-xs font-mono text-zinc-500">{history.length} POINTS</span>
          </div>

          {history.length === 0 ? (
            <div className="font-mono text-xs text-zinc-500 py-8 text-center">
              // NO_RESTORE_POINTS_YET
            </div>
          ) : (
            <div className="space-y-2 max-h-[600px] overflow-y-auto">
              {history.map((rp, i) => (
                <div key={i} className="border border-zinc-800 p-3 hover:border-zinc-700" data-testid={`restore-point-${i}`}>
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="font-bold text-sm">{rp.description}</div>
                      <div className="text-[10px] font-mono text-zinc-500 mt-1 uppercase tracking-widest">
                        {new Date(rp.timestamp).toLocaleString('es-ES')}
                      </div>
                    </div>
                    <div className="flex flex-col items-end gap-1">
                      <span className={`text-[10px] font-mono uppercase tracking-widest px-2 py-0.5 border ${
                        rp.source === "manual" ? "border-[#007AFF] text-[#007AFF]" : "border-[#10B981] text-[#10B981]"
                      }`}>
                        {rp.source === "manual" ? "MANUAL" : "AUTO"}
                      </span>
                      {rp.simulated && (
                        <span className="text-[10px] font-mono text-[#F59E0B]">SIM</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
