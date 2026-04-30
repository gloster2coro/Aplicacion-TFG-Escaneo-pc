# Optidriver - Checklist de Validación en Windows

Documento de validación paso a paso para probar Optidriver en tu PC Windows 10/11 con permisos de administrador.

## Requisitos Previos

- [ ] Windows 10/11 (64-bit)
- [ ] Python 3.11+ instalado (`python --version`)
- [ ] Node.js 18+ con Yarn (`node --version`, `yarn --version`)
- [ ] MongoDB Community corriendo en localhost:27017 (`sc query MongoDB`)
- [ ] Permisos de administrador

## Instalación

```cmd
:: 1. Copiar el proyecto a C:\optidriver
:: 2. Instalar dependencias Python Windows-específicas
cd C:\optidriver\backend
pip install -r requirements.txt
pip install wmi pywin32

:: 3. Instalar dependencias frontend
cd ..\frontend
yarn install

:: 4. Configurar backend\.env
::    MONGO_URL="mongodb://localhost:27017"
::    DB_NAME="optidriver"
::    EMERGENT_LLM_KEY=sk-emergent-...
```

## Arrancar la aplicación

```cmd
:: Clic derecho run_windows.bat -> Ejecutar como administrador
run_windows.bat
```

Verificar:
- [ ] Ventana del backend abierta (uvicorn corriendo en :8001)
- [ ] Ventana del frontend abierta (yarn start en :3000)
- [ ] Navegador abierto automáticamente en http://localhost:3000
- [ ] Footer muestra "SYSTEM_ONLINE" en verde

## Tests funcionales

### Módulo 1: Dashboard y Métricas
- [ ] Se muestran 3 profile cards (Gaming, Oficina, Óptimo)
- [ ] Las métricas CPU/RAM/Disk se actualizan cada 2s
- [ ] Los valores de CPU/RAM/Disk coinciden con el Task Manager de Windows
- [ ] El contador de procesos coincide (aprox) con Task Manager > Details
- [ ] La vista "CPU cores" muestra el número correcto de cores lógicos de tu CPU

### Módulo 2: Hardware Detection (Driver Management)
Ir a `/drivers`:
- [ ] La sección "HARDWARE_SCAN" muestra tu CPU real (ej: "Intel Core i7-12700K")
- [ ] Se muestra tu RAM total real (ej: "32.0 GB")
- [ ] Se muestra tu GPU real (ej: "NVIDIA GeForce RTX 4070")
- [ ] Se muestra tu placa base real (manufacturer y product)
- [ ] No aparece la etiqueta "(simulado)" (esto indica que WMI funciona)

### Módulo 3: Optimización - Modo SIMULACIÓN
- [ ] Seleccionar perfil "Gaming" → Click "APLICAR OPTIMIZACIÓN"
- [ ] Toast "Creando punto de restauración..." aparece
- [ ] Navega a /optimize con detalle del análisis
- [ ] Lista de procesos a cerrar muestra apps reales corriendo (ej: OneDrive, Teams)
- [ ] No se cierra ningún proceso real (porque simulate=true por defecto)

### Módulo 3b: Optimización - APLICACIÓN REAL
**⚠️ Esto cerrará procesos reales. Guarda tu trabajo antes.**
- [ ] Con permisos admin, editar `/api/optimize/apply` call para enviar `simulate: false`
  - Puedes cambiarlo temporalmente en `/app/frontend/src/pages/Dashboard.jsx` línea que llama a `applyOptimization(selected, true)` → cambiar a `false`
- [ ] Aplicar perfil Gaming
- [ ] Verificar que procesos targets (OneDrive, Teams...) se cierran
- [ ] Verificar en `powercfg /getactivescheme` que el plan cambió a "Alto rendimiento"
- [ ] Verificar que los procesos críticos (explorer.exe, dwm.exe, svchost.exe) SIGUEN corriendo

### Módulo 4: Puntos de Restauración Reales
- [ ] Ir a `/restore`
- [ ] Crear punto manual con descripción "Test manual admin"
- [ ] Abrir `rstrui.exe` (Restaurar sistema) como admin
- [ ] Verificar que el punto aparece en la lista de Windows
- [ ] Volver a Optidriver: el punto debe aparecer con fuente "MANUAL" y SIN etiqueta "SIM"

### Módulo 5: Drivers Reales (parcial)
- [ ] En `/drivers` verificar que `pnputil /enum-drivers` se ejecuta (ver logs backend)
- [ ] La UI muestra drivers (actualmente usa dataset simulado - ver Roadmap)
- [ ] Modal de confirmación funciona con botón "Confirmar y Actualizar"
- [ ] Se crea restore point automático antes de "actualización"

### Módulo 6: IA GPT-5.2
- [ ] Ir a `/ai`
- [ ] Seleccionar perfil "Gaming", presupuesto "Medio"
- [ ] Click "EJECUTAR ANÁLISIS IA"
- [ ] Esperar 30-90s
- [ ] Respuesta estructurada aparece con:
  - [ ] Veredicto (APTO/PARCIALMENTE_APTO/NO_APTO)
  - [ ] Puntuación /100
  - [ ] Juegos compatibles con tus FPS estimados según tu hardware real
  - [ ] Juegos no compatibles con motivo
  - [ ] Mejoras recomendadas con precios EUR
- [ ] Chat libre: escribir "Cuál es el mejor monitor 4K por <500€?" y obtener respuesta

### Módulo 7: PDF Documentación
- [ ] Click en botón "PDF" del header
- [ ] Se descarga `optidriver_documentacion.pdf`
- [ ] Abrir el PDF → contiene 10 secciones (Intro, Arquitectura, Módulos, API, Instalación, Estructura, DB, Decisiones, Uso, Compilación)

### Módulo 8: Scheduler (auto-apply profiles)
- [ ] Ir a `/scheduler`
- [ ] Crear regla: `steam.exe` → `gaming`
- [ ] Habilitar el scheduler
- [ ] Lanzar Steam
- [ ] Verificar que el perfil Gaming se aplica automáticamente (toast de notificación)

### Módulo 9: Comparativa Before/After
- [ ] Tras aplicar una optimización, ir a /optimize
- [ ] Panel "COMPARATIVA DE IMPACTO" muestra métricas antes vs después
- [ ] CPU, RAM y procesos comparados con flechas de mejora/empeora

## Empaquetado .exe

### Opción A - PyInstaller (single .exe)
```cmd
build_exe.bat
:: Output: dist\Optidriver.exe (~150 MB)
```
- [ ] Ejecutar `dist\Optidriver.exe`
- [ ] Se abre ventana/navegador correctamente
- [ ] Todas las funciones anteriores funcionan

### Opción B - Electron (installer)
```cmd
build_electron.bat
:: Output: dist-electron\Optidriver Setup 1.0.0.exe
```
- [ ] Ejecutar el installer → instala en Program Files
- [ ] Shortcut en escritorio creado
- [ ] Click derecho shortcut → "Ejecutar como administrador"
- [ ] App se abre en ventana nativa (sin barra de navegador)

## Resultados

Anota aquí cualquier problema encontrado:

| Módulo | Resultado | Notas |
|--------|-----------|-------|
| Dashboard | ⬜ OK / ⬜ Fail | |
| Drivers HUD | ⬜ OK / ⬜ Fail | |
| Optimize SIM | ⬜ OK / ⬜ Fail | |
| Optimize REAL | ⬜ OK / ⬜ Fail | |
| Restore points | ⬜ OK / ⬜ Fail | |
| IA GPT-5.2 | ⬜ OK / ⬜ Fail | |
| PDF | ⬜ OK / ⬜ Fail | |
| Scheduler | ⬜ OK / ⬜ Fail | |
| Before/After | ⬜ OK / ⬜ Fail | |
| PyInstaller | ⬜ OK / ⬜ Fail | |
| Electron | ⬜ OK / ⬜ Fail | |

## Troubleshooting

**"ModuleNotFoundError: No module named 'wmi'"**
→ `pip install wmi pywin32`

**"Access is denied" al crear restore point**
→ Ejecuta run_windows.bat como administrador

**"System Restore is disabled"**
→ `powershell Enable-ComputerRestore -Drive "C:\"` como admin

**"MongoDB connection refused"**
→ Arrancar servicio: `net start MongoDB`

**GPT-5.2 timeout**
→ La IA puede tardar hasta 90s. Esperar. Si falla, revisar EMERGENT_LLM_KEY en backend\.env
