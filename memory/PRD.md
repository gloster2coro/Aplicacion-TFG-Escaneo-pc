# OPTIDRIVER - PRD

## Problema Original
Desarrollar **Optidriver**: aplicación profesional para optimizar rendimiento de Windows, gestionar drivers, y ofrecer recomendaciones inteligentes vía IA. Usuario eligió **Opción A: Web App local** con **GPT-5.2**.

## Arquitectura
- Backend: FastAPI + MongoDB (puerto 8001, prefix /api)
- Frontend: React 19 + Shadcn UI + Phosphor icons (tema "Performance Pro" dark tactical)
- IA: GPT-5.2 via emergentintegrations (EMERGENT_LLM_KEY)
- Hardware: psutil (cross-platform) + wmi/winreg (solo Windows)

## User Personas
1. **Gamer**: busca máximo FPS, cierra apps en background
2. **Oficinista**: quiere productividad sin romper estética
3. **Usuario general**: solo quiere "que vaya rápido"

## Core Requirements (static)
- 3 perfiles optimización (Gaming/Oficina/Óptimo) con lista blanca de procesos críticos
- Detección hardware (CPU/GPU/RAM/Mobo) con imagen HUD motherboard
- Gestión drivers con aviso versión actual→nueva y actualización batch
- Asistente IA con análisis de compatibilidad de juegos + recomendaciones upgrade/PC según presupuesto
- Puntos de restauración automáticos antes de cambios críticos + creación manual
- Documentación PDF descargable

## Implementado (30-Abr-2026)
- ✅ Backend completo: 18 endpoints (/api/hardware, /api/system, /api/optimize, /api/drivers, /api/restore, /api/ai, /api/docs/pdf)
- ✅ Frontend: 5 páginas (Dashboard, Optimizer, Drivers, AI Assistant, Restore Points)
- ✅ Integración GPT-5.2 con análisis estructurado JSON (veredicto, score, juegos compatibles, mejoras, equipos recomendados)
- ✅ Chat libre con terminal aesthetic + IBM Plex Mono
- ✅ Hardware HUD de motherboard con datos overlay
- ✅ Auto-creación de restore point antes de optimizar/actualizar drivers
- ✅ PDF de documentación generado dinámicamente con reportlab
- ✅ Script `run_windows.bat` para ejecución local con permisos admin
- ✅ Persistencia MongoDB (profiles, optimization_logs, driver_updates, restore_points, ai_sessions, ai_chat_messages)
- ✅ Testing agent: 100% backend (15/15) + 100% frontend (11/11)

## Implementado (30-Abr-2026 - Iteración 2)
- ✅ **Packaging .exe**: `launcher.py` (entry point), `build_exe.bat` (PyInstaller single .exe)
- ✅ **Electron wrapper**: `/app/electron/` con main.js, preload.js, electron-builder config NSIS con requireAdministrator
- ✅ **Windows Validation Checklist**: `/app/WINDOWS_VALIDATION_CHECKLIST.md` (pruebas paso a paso + troubleshooting)
- ✅ **Scheduler automático**: página `/scheduler`, reglas CRUD (name, trigger_processes, profile, priority), toggle on/off, polling cada 15s, aplica perfil cuando procesos trigger están corriendo
- ✅ **Before/After metrics**: panel "COMPARATIVA DE IMPACTO" tras aplicar optimización, 4 métricas (CPU/Memory/Disk/Procs) con before/after/delta/delta_percent, colores verde-mejoró/rojo-empeoró
- ✅ Nuevos endpoints: /api/scheduler/* (status, toggle, rules CRUD, events), /api/metrics/* (snapshot, latest-comparison)
- ✅ Testing agent: 100% backend (24/24), 100% frontend tras fix

## Bugfixes (07-Feb-2026)
- 🐛➡️✅ **Optimizador no aplicaba cambios reales**: `Optimizer.jsx` enviaba `simulate=true` hardcoded. Añadido toggle MODO_EJECUCIÓN (Simulación/Real) con modal de confirmación. Botón REAL solo activo si backend corre en Windows (nuevo endpoint `/api/system/info` expone `is_windows`/`is_admin`).
- 🐛➡️✅ **Chat IA devolvía JSON crudo y parecía bloqueado**: separados `ANALYZE_SYSTEM_PROMPT` (JSON) y `CHAT_SYSTEM_PROMPT` (texto conversacional natural en español). Timeout axios extendido a 180s para AI endpoints. Errores reales del backend ahora visibles en UI.


## Notas Técnicas
- En entorno Linux (preview) los datos Windows-específicos son simulados (drivers, GPU, mobo, servicios)
- En Windows real con admin: funciones operativas reales (psutil procesos, wmi hardware, pnputil drivers, PowerShell Checkpoint-Computer)
- IA responde en 30-90s; timeout configurado a 120s

## Backlog / Next Tasks
- **P1**: Electron wrapper para compilación .exe + instalador Windows
- **P1**: Validación real en Windows 10/11 con permisos admin
- **P2**: Scheduler de optimizaciones (ej: aplicar perfil Gaming al lanzar Steam)
- **P2**: Comparativa histórica de rendimiento (before/after metrics)
- **P2**: Export/Import de perfiles personalizados
- **P3**: Notificaciones system tray (cuando drivers críticos estén desactualizados)
- **P3**: Dark/Light theme toggle (actualmente solo dark tactical)
- **P3**: i18n (actualmente solo ES)
