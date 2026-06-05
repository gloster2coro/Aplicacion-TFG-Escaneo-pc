import React, { useEffect, useState } from "react";
import { toast } from "sonner";
import { Download, Warning, CheckCircle, Cpu, Database, HardDrives } from "@phosphor-icons/react";
import { getDrivers, getHardwareFull, updateDrivers } from "../lib/api";

const MOTHERBOARD_IMG = "https://images.unsplash.com/photo-1694466464626-7bd06595cf2d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA2MTJ8MHwxfHNlYXJjaHwyfHxtb3RoZXJib2FyZCUyMHBjJTIwaGFyZHdhcmV8ZW58MHx8fHwxNzc3NTc2NDEyfDA&ixlib=rb-4.1.0&q=85";

export default function Drivers() {
  const [drivers, setDrivers] = useState([]);
  const [hardware, setHardware] = useState(null);
  const [selected, setSelected] = useState(new Set());
  const [loading, setLoading] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [result, setResult] = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const [d, h] = await Promise.all([getDrivers(), getHardwareFull()]);
      setDrivers(d.drivers);
      setHardware(h);
    } catch (e) {
      toast.error("Error cargando drivers");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const toggle = (name) => {
    const s = new Set(selected);
    s.has(name) ? s.delete(name) : s.add(name);
    setSelected(s);
  };

  const toggleAll = () => {
    const outdated = drivers.filter(d => d.outdated).map(d => d.name);
    if (selected.size === outdated.length) {
      setSelected(new Set());
    } else {
      setSelected(new Set(outdated));
    }
  };

  const handleUpdate = async () => {
    if (selected.size === 0) return;
    setShowModal(true);
  };

  const confirmUpdate = async () => {
    setUpdating(true);
    setShowModal(false);
    try {
      toast.loading(`Actualizando ${selected.size} drivers...`, { id: "upd" });
      const r = await updateDrivers([...selected], true);
      setResult(r);
      toast.success(`${r.successes} drivers actualizados. Punto de restauración creado automáticamente.`, { id: "upd", duration: 5000 });
      setSelected(new Set());
      await load();
    } catch (e) {
      toast.error("Error actualizando drivers", { id: "upd" });
    } finally {
      setUpdating(false);
    }
  };

  const outdated = drivers.filter(d => d.outdated);
  const selectedDrivers = drivers.filter(d => selected.has(d.name));

  return (
    <div className="px-4 md:px-8 py-8 max-w-7xl mx-auto fade-in" data-testid="page-drivers">
      <div className="mb-8">
        <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-[#007AFF] mb-3">
          // DRIVER_MANAGEMENT
        </div>
        <h1 className="font-heading text-4xl sm:text-5xl font-black uppercase tracking-tighter leading-none">
          Gestión de <span className="text-[#007AFF]">Drivers</span>
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Hardware HUD */}
        <aside className="lg:col-span-2">
          <div className="card-tactical overflow-hidden" data-testid="hardware-hud">
            <div className="relative aspect-video overflow-hidden">
              <img src={MOTHERBOARD_IMG} alt="Motherboard scan" className="w-full h-full object-cover opacity-60" />
              <div className="absolute inset-0 bg-black/60"></div>
              <div className="absolute inset-0 grid-bg opacity-40"></div>
              {/* HUD overlay corners */}
              <div className="absolute top-4 left-4 w-8 h-8 border-l-2 border-t-2 border-[#007AFF]"></div>
              <div className="absolute top-4 right-4 w-8 h-8 border-r-2 border-t-2 border-[#007AFF]"></div>
              <div className="absolute bottom-4 left-4 w-8 h-8 border-l-2 border-b-2 border-[#007AFF]"></div>
              <div className="absolute bottom-4 right-4 w-8 h-8 border-r-2 border-b-2 border-[#007AFF]"></div>

              <div className="absolute top-4 left-16 text-[10px] font-mono text-[#007AFF] uppercase tracking-widest">
                [ESCANEO_HARDWARE]
              </div>
              <div className="absolute bottom-4 right-16 text-[10px] font-mono text-[#10B981] uppercase tracking-widest flex items-center gap-2">
                <span className="w-1.5 h-1.5 bg-[#10B981] rounded-full pulse-slow"></span>
                DETECTADO
              </div>

              {hardware && (
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="font-heading text-3xl font-black text-white uppercase">
                      {hardware.motherboard?.manufacturer?.split(' ')[0] || "DESCONOCIDO"}
                    </div>
                    <div className="font-mono text-xs text-[#007AFF] uppercase tracking-widest">
                      {hardware.motherboard?.product || "Motherboard"}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {hardware && (
              <div className="p-5 space-y-4 font-mono text-xs">
                <HardwareLine icon={Cpu} label="CPU" value={hardware.cpu?.name} detail={`${hardware.cpu?.physical_cores}C/${hardware.cpu?.logical_cores}T @ ${hardware.cpu?.max_frequency_mhz}MHz`} />
                <HardwareLine icon={Database} label="RAM" value={`${hardware.memory?.total_gb} GB`} detail={`${hardware.memory?.percent}% en uso`} />
                <HardwareLine icon={HardDrives} label="GPU" value={hardware.gpu?.[0]?.name || "N/A"} detail={hardware.gpu?.[0]?.driver_version ? `Driver ${hardware.gpu[0].driver_version}` : ""} />
                <HardwareLine icon={HardDrives} label="MOBO" value={hardware.motherboard?.product} detail={hardware.motherboard?.manufacturer} />
              </div>
            )}
          </div>
        </aside>

        {/* Drivers table */}
        <section className="lg:col-span-3">
          <div className="card-tactical p-5" data-testid="drivers-table">
            <div className="flex flex-wrap items-center justify-between gap-3 mb-5">
              <div>
                <div className="font-heading text-xl font-bold uppercase tracking-wider">Drivers Instalados</div>
                <div className="text-xs font-mono text-zinc-500 mt-1">
                  {drivers.length} TOTAL · <span className="text-[#F59E0B]">{outdated.length} DESACTUALIZADOS</span>
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={toggleAll}
                  data-testid="btn-select-all-outdated"
                  className="px-3 py-2 font-heading uppercase tracking-widest text-xs font-bold border border-zinc-700 hover:border-[#F59E0B] text-zinc-300 hover:text-[#F59E0B]"
                >
                  Seleccionar desactualizados
                </button>
                <button
                  onClick={handleUpdate}
                  disabled={selected.size === 0 || updating}
                  data-testid="btn-update-drivers"
                  className="btn-tactical text-xs"
                >
                  <Download size={14} weight="bold" className="inline mr-2" />
                  ACTUALIZAR ({selected.size})
                </button>
              </div>
            </div>

            {loading ? (
              <div className="text-sm font-mono text-zinc-500 py-8 text-center">
                <span className="cursor-blink">ESCANEANDO_DRIVERS</span>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-zinc-800 text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                      <th className="text-left py-3 w-8"></th>
                      <th className="text-left py-3">Driver</th>
                      <th className="text-left py-3 hidden md:table-cell">Versión Actual</th>
                      <th className="text-left py-3 hidden md:table-cell">Última</th>
                      <th className="text-left py-3">Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    {drivers.map((d, i) => (
                      <tr
                        key={i}
                        className={`border-b border-zinc-900 hover:bg-zinc-900/30 ${d.outdated ? "" : "opacity-60"}`}
                      >
                        <td className="py-3">
                          <input
                            type="checkbox"
                            checked={selected.has(d.name)}
                            onChange={() => toggle(d.name)}
                            disabled={!d.outdated}
                            data-testid={`driver-checkbox-${i}`}
                            className="accent-[#007AFF] cursor-pointer disabled:cursor-not-allowed"
                          />
                        </td>
                        <td className="py-3">
                          <div className="font-mono text-xs">{d.name}</div>
                          <div className="text-[10px] text-zinc-500 uppercase tracking-widest">{d.device_class}</div>
                        </td>
                        <td className="py-3 hidden md:table-cell font-mono text-xs text-zinc-400">{d.current_version}</td>
                        <td className="py-3 hidden md:table-cell font-mono text-xs">
                          {d.outdated ? (
                            <span className="text-[#10B981]">{d.latest_version}</span>
                          ) : (
                            <span className="text-zinc-500">--</span>
                          )}
                        </td>
                        <td className="py-3">
                          {d.outdated ? (
                            <span className="inline-flex items-center gap-1 px-2 py-1 border border-[#F59E0B] text-[#F59E0B] text-[10px] font-mono uppercase">
                              <Warning size={10} weight="bold" /> Desactualizado
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 px-2 py-1 border border-[#10B981] text-[#10B981] text-[10px] font-mono uppercase">
                              <CheckCircle size={10} weight="bold" /> OK
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {result && (
            <div className="mt-4 card-tactical p-5 border-[#10B981]" data-testid="update-result">
              <div className="flex items-center gap-2 mb-3">
                <CheckCircle size={20} className="text-[#10B981]" weight="bold" />
                <h3 className="font-heading text-lg font-bold uppercase">Resultado</h3>
              </div>
              <div className="text-sm font-mono space-y-1">
                <div>✓ <span className="text-[#10B981]">{result.successes}</span> drivers actualizados con éxito</div>
                {result.failures > 0 && <div>✗ <span className="text-[#FF3B30]">{result.failures}</span> fallidos</div>}
                {result.simulated && <div className="text-[#F59E0B] mt-2">// MODO SIMULACIÓN - se aplicará real en Windows admin</div>}
              </div>
            </div>
          )}
        </section>
      </div>

      {/* Confirmation modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" data-testid="confirm-modal">
          <div className="card-tactical max-w-xl w-full p-6 border-[#F59E0B]">
            <div className="flex items-center gap-3 mb-4">
              <Warning size={28} className="text-[#F59E0B]" weight="bold" />
              <h3 className="font-heading text-2xl font-bold uppercase">Confirmación de Actualización</h3>
            </div>
            <p className="text-sm text-zinc-400 mb-4">
              Se creará un punto de restauración automáticamente antes de actualizar los siguientes drivers:
            </p>
            <div className="max-h-60 overflow-y-auto border border-zinc-800 p-3 mb-4">
              {selectedDrivers.map((d, i) => (
                <div key={i} className="text-xs font-mono py-1.5 border-b border-zinc-900 last:border-0">
                  <div>{d.name}</div>
                  <div className="text-zinc-500 mt-0.5">
                    <span className="text-[#FF3B30]">{d.current_version}</span>
                    {" → "}
                    <span className="text-[#10B981]">{d.latest_version}</span>
                  </div>
                </div>
              ))}
            </div>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowModal(false)}
                data-testid="btn-cancel-update"
                className="px-4 py-2 border border-zinc-700 text-zinc-400 hover:text-white font-heading uppercase text-xs tracking-widest font-bold"
              >
                Cancelar
              </button>
              <button
                onClick={confirmUpdate}
                data-testid="btn-confirm-update"
                className="btn-tactical text-xs"
              >
                Confirmar y Actualizar →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function HardwareLine({ icon: Icon, label, value, detail }) {
  return (
    <div className="flex items-start gap-3 border-l-2 border-[#007AFF] pl-3">
      <Icon size={16} className="text-[#007AFF] mt-0.5" weight="bold" />
      <div className="flex-1 min-w-0">
        <div className="text-[10px] text-zinc-500 uppercase tracking-[0.2em]">{label}</div>
        <div className="text-zinc-200 truncate">{value || "—"}</div>
        {detail && <div className="text-[10px] text-zinc-500 mt-0.5">{detail}</div>}
      </div>
    </div>
  );
}
