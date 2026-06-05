import React, { useState, useRef, useEffect } from "react";
import { toast } from "sonner";
import { Robot, PaperPlaneRight, Sparkle, CurrencyDollar } from "@phosphor-icons/react";
import { aiAnalyze, aiChat } from "../lib/api";

const BUDGETS = [
  { key: "bajo", label: "Bajo", range: "<500€", color: "#10B981" },
  { key: "medio", label: "Medio", range: "500-1500€", color: "#007AFF" },
  { key: "alto", label: "Alto", range: ">1500€", color: "#FF3B30" },
];

const PROFILES = [
  { key: "gaming", label: "Gaming" },
  { key: "oficina", label: "Oficina" },
  { key: "optimo", label: "Óptimo" },
];

export default function AIAssistant() {
  const [profile, setProfile] = useState("gaming");
  const [budget, setBudget] = useState("medio");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role: "system", text: "// OPTIDRIVER IA v1.0 · GPT-5.2 CARGADO · LISTO" },
  ]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [chatting, setChatting] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const runAnalysis = async () => {
    setLoading(true);
    setAnalysis(null);
    try {
      toast.loading("Analizando tu hardware con GPT-5.2...", { id: "ai" });
      const r = await aiAnalyze(profile, budget, sessionId);
      setAnalysis(r.recommendation);
      setSessionId(r.session_id);
      toast.success("Análisis completado", { id: "ai" });
    } catch (e) {
      toast.error("Error en el análisis IA", { id: "ai" });
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || chatting) return;
    const userMsg = { role: "user", text: input };
    setMessages(m => [...m, userMsg]);
    const msg = input;
    setInput("");
    setChatting(true);
    try {
      const r = await aiChat(msg, sessionId, !sessionId);
      setSessionId(r.session_id);
      setMessages(m => [...m, { role: "assistant", text: r.response }]);
    } catch (e) {
      setMessages(m => [...m, { role: "error", text: "// ERROR: No se pudo contactar con el asistente" }]);
    } finally {
      setChatting(false);
    }
  };

  return (
    <div className="px-4 md:px-8 py-8 max-w-7xl mx-auto fade-in" data-testid="page-ai">
      <div className="mb-8">
        <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-[#10B981] mb-3">
          // ASISTENTE_IA · GPT-5.2
        </div>
        <h1 className="font-heading text-4xl sm:text-5xl font-black uppercase tracking-tighter leading-none">
          Asistente <span className="text-[#10B981]">Táctico</span>
        </h1>
        <p className="text-zinc-400 mt-3 max-w-2xl text-sm">
          Analiza tu hardware, comprueba compatibilidad con juegos populares y recibe recomendaciones
          personalizadas de upgrade o equipos nuevos según tu presupuesto.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Control panel */}
        <aside className="lg:col-span-2 space-y-4">
          <div className="card-tactical p-5" data-testid="ai-controls">
            <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500 mb-3">
              CONFIGURACIÓN
            </div>

            <label className="block text-xs font-mono uppercase tracking-widest text-zinc-400 mb-2">
              Perfil de uso
            </label>
            <div className="flex gap-2 mb-5">
              {PROFILES.map(p => (
                <button
                  key={p.key}
                  onClick={() => setProfile(p.key)}
                  data-testid={`ai-profile-${p.key}`}
                  className={`flex-1 px-3 py-2 font-heading uppercase tracking-widest text-xs font-bold border transition-colors ${
                    profile === p.key
                      ? "border-[#10B981] text-[#10B981] bg-[#10B981]/10"
                      : "border-zinc-800 text-zinc-500 hover:border-zinc-600"
                  }`}
                >
                  {p.label}
                </button>
              ))}
            </div>

            <label className="block text-xs font-mono uppercase tracking-widest text-zinc-400 mb-2">
              <CurrencyDollar size={12} className="inline mr-1" weight="bold" />
              Presupuesto
            </label>
            <div className="space-y-2 mb-5">
              {BUDGETS.map(b => (
                <button
                  key={b.key}
                  onClick={() => setBudget(b.key)}
                  data-testid={`ai-budget-${b.key}`}
                  className={`w-full p-3 border text-left transition-colors ${
                    budget === b.key
                      ? "border-current bg-current/10"
                      : "border-zinc-800 text-zinc-500 hover:border-zinc-600"
                  }`}
                  style={{ color: budget === b.key ? b.color : undefined }}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-heading uppercase text-sm font-bold">{b.label}</span>
                    <span className="font-mono text-xs">{b.range}</span>
                  </div>
                </button>
              ))}
            </div>

            <button
              onClick={runAnalysis}
              disabled={loading}
              data-testid="btn-run-analysis"
              className="btn-tactical w-full flex items-center justify-center gap-2 glow-success"
              style={{ borderColor: "#10B981", color: "#10B981" }}
            >
              <Sparkle size={16} weight="bold" />
              {loading ? "ANALIZANDO..." : "EJECUTAR ANÁLISIS IA"}
            </button>
          </div>

          {/* Chat */}
          <div className="card-tactical p-5 flex flex-col" style={{ height: '500px' }} data-testid="ai-chat">
            <div className="flex items-center gap-2 mb-3 pb-3 border-b border-zinc-800">
              <Robot size={18} className="text-[#10B981]" weight="bold" />
              <span className="font-heading uppercase tracking-widest text-sm font-bold">CHAT TERMINAL</span>
              <span className="ml-auto text-[10px] font-mono text-zinc-500">GPT-5.2</span>
            </div>
            <div ref={scrollRef} className="flex-1 overflow-y-auto font-mono text-xs space-y-3 pb-2">
              {messages.map((m, i) => (
                <div key={i} className={
                  m.role === "user" ? "text-[#007AFF]"
                  : m.role === "assistant" ? "text-zinc-200"
                  : m.role === "error" ? "text-[#FF3B30]"
                  : "text-zinc-500"
                }>
                  <div className="text-[10px] uppercase tracking-widest opacity-60">
                    {m.role === "user" ? "> USUARIO" : m.role === "assistant" ? "< IA" : m.role === "error" ? "! ERROR" : "# SISTEMA"}
                  </div>
                  <div className="whitespace-pre-wrap leading-relaxed mt-0.5">{m.text}</div>
                </div>
              ))}
              {chatting && (
                <div className="text-[#10B981] cursor-blink text-[10px]">PROCESANDO</div>
              )}
            </div>
            <div className="flex gap-2 pt-3 border-t border-zinc-800">
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && sendMessage()}
                placeholder="Pregunta al asistente..."
                data-testid="ai-chat-input"
                className="flex-1 bg-black border border-zinc-800 px-3 py-2 font-mono text-xs text-zinc-200 focus:border-[#10B981] outline-none"
              />
              <button
                onClick={sendMessage}
                disabled={chatting || !input.trim()}
                data-testid="btn-send-message"
                className="px-3 border border-[#10B981] text-[#10B981] hover:bg-[#10B981] hover:text-black disabled:opacity-40"
              >
                <PaperPlaneRight size={16} weight="bold" />
              </button>
            </div>
          </div>
        </aside>

        {/* Analysis output */}
        <section className="lg:col-span-3">
          <div className="card-tactical p-6 min-h-[600px]" data-testid="ai-output">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center gap-2">
                <Robot size={22} className="text-[#10B981]" weight="bold" />
                <h2 className="font-heading text-xl font-bold uppercase tracking-wider">SALIDA DEL ANÁLISIS</h2>
              </div>
              {analysis?.veredicto && (
                <span
                  className={`px-3 py-1 border font-mono text-xs uppercase tracking-widest ${
                    analysis.veredicto === "APTO" ? "border-[#10B981] text-[#10B981] bg-[#10B981]/10" :
                    analysis.veredicto === "NO_APTO" ? "border-[#FF3B30] text-[#FF3B30] bg-[#FF3B30]/10" :
                    "border-[#F59E0B] text-[#F59E0B] bg-[#F59E0B]/10"
                  }`}
                  data-testid="verdict-badge"
                >
                  {analysis.veredicto}
                </span>
              )}
            </div>

            {!analysis && !loading && (
              <div className="font-mono text-xs text-zinc-500 space-y-1">
                <div>// ESPERANDO_ANÁLISIS</div>
                <div className="cursor-blink">LISTO</div>
              </div>
            )}

            {loading && (
              <div className="font-mono text-xs text-[#10B981] space-y-2">
                <div>{"> Iniciando escaneo de hardware..."}</div>
                <div>{"> Enviando reporte a GPT-5.2..."}</div>
                <div>{"> Analizando compatibilidad..."}</div>
                <div className="cursor-blink">{"> Procesando"}</div>
              </div>
            )}

            {analysis && (
              <div className="space-y-6 font-body fade-in">
                {/* Score */}
                {analysis.puntuacion_general !== undefined && (
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500">PUNTUACIÓN</span>
                      <span className="font-heading text-3xl font-black text-[#10B981]">
                        {analysis.puntuacion_general}/100
                      </span>
                    </div>
                    <div className="progress-tactical">
                      <div
                        className="progress-tactical-fill"
                        style={{
                          width: `${analysis.puntuacion_general}%`,
                          background: analysis.puntuacion_general > 70 ? "#10B981" : analysis.puntuacion_general > 40 ? "#F59E0B" : "#FF3B30"
                        }}
                      />
                    </div>
                  </div>
                )}

                {/* Tactical summary */}
                {analysis.resumen_tactical && (
                  <div className="font-mono text-sm text-[#10B981] border-l-2 border-[#10B981] pl-3 py-1">
                    {"> "}{analysis.resumen_tactical}
                  </div>
                )}

                {/* Analysis */}
                {analysis.analisis && (
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500 mb-2">ANÁLISIS</div>
                    <p className="text-sm text-zinc-300 leading-relaxed">{analysis.analisis}</p>
                  </div>
                )}

                {/* Games compatible */}
                {analysis.juegos_compatibles?.length > 0 && (
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-[#10B981] mb-2">JUEGOS COMPATIBLES</div>
                    <div className="space-y-2">
                      {analysis.juegos_compatibles.map((g, i) => (
                        <div key={i} className="border border-[#10B981]/30 p-3 flex items-center justify-between">
                          <div>
                            <div className="font-bold text-sm">{g.nombre}</div>
                            <div className="text-[10px] font-mono text-zinc-500 uppercase">{g.config} · {g.fps_estimado} FPS</div>
                          </div>
                          <span className="text-[#10B981] font-mono text-xs">✓ APTO</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Games not compatible */}
                {analysis.juegos_no_compatibles?.length > 0 && (
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-[#FF3B30] mb-2">JUEGOS NO COMPATIBLES</div>
                    <div className="space-y-2">
                      {analysis.juegos_no_compatibles.map((g, i) => (
                        <div key={i} className="border border-[#FF3B30]/30 p-3">
                          <div className="font-bold text-sm">{g.nombre}</div>
                          <div className="text-[10px] font-mono text-zinc-500 mt-1">{g.razon}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Upgrade recommendations */}
                {analysis.mejoras_recomendadas?.length > 0 && (
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-[#007AFF] mb-2">MEJORAS RECOMENDADAS</div>
                    <div className="space-y-2">
                      {analysis.mejoras_recomendadas.map((m, i) => (
                        <div key={i} className="border border-[#007AFF]/30 p-3">
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-heading text-sm font-bold uppercase">{m.componente}</span>
                            <span className="font-mono text-xs text-[#007AFF]">{m.precio_eur}€</span>
                          </div>
                          <div className="text-xs text-zinc-400 font-mono">
                            <span className="text-[#FF3B30]">{m.actual}</span>
                            {" → "}
                            <span className="text-[#10B981]">{m.recomendado}</span>
                          </div>
                          {m.impacto && <div className="text-[10px] font-mono text-zinc-500 mt-1 uppercase">Impacto: {m.impacto}</div>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Full PC recommendations */}
                {analysis.equipos_recomendados?.length > 0 && (
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-[#F59E0B] mb-2">EQUIPOS RECOMENDADOS</div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {analysis.equipos_recomendados.map((e, i) => (
                        <div key={i} className="border border-[#F59E0B]/30 p-3">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-[10px] font-mono uppercase tracking-widest text-[#F59E0B]">{e.tipo}</span>
                            <span className="font-mono text-xs">{e.precio_eur}€</span>
                          </div>
                          <div className="font-bold text-sm">{e.modelo}</div>
                          {e.razon && <div className="text-[10px] text-zinc-500 mt-1">{e.razon}</div>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
