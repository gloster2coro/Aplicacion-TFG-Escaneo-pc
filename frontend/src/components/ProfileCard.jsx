import React from "react";
import { ArrowRight } from "@phosphor-icons/react";

export default function ProfileCard({ profile, title, subtitle, description, icon: Icon, color, selected, onSelect, testid }) {
  return (
    <button
      onClick={() => onSelect(profile)}
      data-testid={testid}
      className={`group relative text-left overflow-hidden border-2 p-8 transition-all duration-300 ${
        selected
          ? "border-current"
          : "border-zinc-800 hover:border-current"
      }`}
      style={{ color, backgroundColor: selected ? `${color}15` : '#121212' }}
    >
      {/* Corner accent */}
      <div className="absolute top-0 right-0 w-16 h-16 border-l border-b border-current opacity-30"></div>
      <div className="absolute bottom-0 left-0 w-16 h-16 border-r border-t border-current opacity-30"></div>

      <div className="relative z-10">
        <div className="flex items-start justify-between mb-6">
          <div
            className="w-14 h-14 border-2 border-current flex items-center justify-center"
            style={{ backgroundColor: `${color}20` }}
          >
            <Icon size={28} weight="bold" />
          </div>
          <span className="text-[10px] font-mono uppercase tracking-[0.2em] text-zinc-500">
            PERFIL_{profile.toUpperCase()}
          </span>
        </div>

        <h3 className="font-heading text-4xl font-black uppercase tracking-tight leading-none text-white mb-2">
          {title}
        </h3>
        <div className="font-mono text-xs uppercase tracking-widest mb-4" style={{ color }}>
          {subtitle}
        </div>

        <p className="text-sm text-zinc-400 leading-relaxed mb-8 font-body">
          {description}
        </p>

        <div className="flex items-center justify-between">
          <span className="font-heading uppercase tracking-widest text-sm font-bold">
            {selected ? "SELECCIONADO" : "Seleccionar"}
          </span>
          <ArrowRight
            size={20}
            weight="bold"
            className={`transition-transform ${selected ? "translate-x-2" : "group-hover:translate-x-2"}`}
          />
        </div>
      </div>
    </button>
  );
}
