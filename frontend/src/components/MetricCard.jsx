import React from "react";

export default function MetricCard({ label, value, unit, percent, color = "#007AFF", testid, icon: Icon }) {
  const p = Math.min(100, Math.max(0, percent ?? 0));
  return (
    <div className="card-tactical p-5" data-testid={testid}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="text-[10px] font-bold uppercase tracking-[0.25em] text-zinc-500 font-mono">
            {label}
          </div>
          <div className="mt-2 font-heading text-4xl font-black">
            {value}
            {unit && <span className="text-lg text-zinc-400 ml-1">{unit}</span>}
          </div>
        </div>
        {Icon && (
          <div className="p-2 border border-zinc-800" style={{ color }}>
            <Icon size={20} weight="bold" />
          </div>
        )}
      </div>
      {percent !== undefined && (
        <>
          <div className="progress-tactical">
            <div
              className="progress-tactical-fill"
              style={{ width: `${p}%`, background: color }}
            />
          </div>
          <div className="mt-2 flex justify-between text-[10px] font-mono text-zinc-500 uppercase tracking-wider">
            <span>USO</span>
            <span style={{ color }}>{p.toFixed(1)}%</span>
          </div>
        </>
      )}
    </div>
  );
}
