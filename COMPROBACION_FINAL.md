# ✅ COMPROBACIÓN FINAL - OPTIDRIVER EN TU PC

Lista de verificación para asegurarte de que TODO funciona antes de la presentación.

---

## 🔍 Paso 1: Comprobaciones de entorno

Abre **CMD como administrador** y ejecuta uno por uno:

```cmd
python --version
```
✅ Debe responder: `Python 3.12.x` (NO 3.14)

```cmd
node --version
```
✅ Debe responder: `v18.x.x` o superior

```cmd
yarn --version
```
✅ Debe responder: `1.22.x` o superior

```cmd
sc query MongoDB
```
✅ Debe contener: `STATE : 4  RUNNING`

Si alguno falla → revisa `README_WINDOWS.md`.

---

## 🚀 Paso 2: Arrancar la aplicación

```cmd
cd /d C:\Optidriver
run_windows.bat
```

✅ Verifica que:
1. Se abre la ventana **"Optidriver Backend"** → debe mostrar `Application startup complete` y `Uvicorn running on http://0.0.0.0:8001`
2. Se abre la ventana **"Optidriver Frontend"** → debe mostrar `Compiled successfully!` y `webpack compiled successfully`
3. Se abre el **navegador** automáticamente en http://localhost:3000
4. Ves el dashboard con título grande **"COMMAND YOUR MACHINE"**

---

## 🧪 Paso 3: Tests funcionales (5 minutos)

### Test 1: Dashboard y métricas en tiempo real
- [ ] Las métricas CPU/MEMORY/DISK/PROCESSES muestran valores reales (no `--`)
- [ ] Los valores cambian cada 2 segundos
- [ ] Las barras de CPU CORES muestran el número correcto de cores

### Test 2: Selección de perfil
- [ ] Click en card "GAMING" → se selecciona (borde rojo)
- [ ] Click en card "OFICINA" → se selecciona (borde blanco)
- [ ] Click en card "ÓPTIMO" → se selecciona (borde azul)
- [ ] Botón "APLICAR OPTIMIZACIÓN" se activa cuando hay perfil seleccionado

### Test 3: Aplicar optimización
- [ ] Selecciona "Gaming" y click "APLICAR OPTIMIZACIÓN"
- [ ] Aparece toast de confirmación
- [ ] Navega a `/optimize` automáticamente
- [ ] Ves panel "COMPARATIVA DE IMPACTO" con CPU/MEMORY/DISK/PROCS antes y después

### Test 4: Módulo Drivers
- [ ] Click en nav "DRIVERS"
- [ ] Ves la imagen de motherboard a la izquierda
- [ ] Ves CPU, RAM, GPU, Mobo reales de tu PC
- [ ] Tabla con drivers a la derecha
- [ ] Botón "Seleccionar desactualizados" marca los outdated
- [ ] Click "ACTUALIZAR (n)" abre modal de confirmación

### Test 5: Asistente IA (GPT-5.2)
- [ ] Click en nav "ASISTENTE IA"
- [ ] Selecciona perfil "Gaming" + presupuesto "Medio"
- [ ] Click "EJECUTAR ANÁLISIS IA"
- [ ] **Espera 30-90 segundos** (es normal, GPT-5.2 tarda)
- [ ] Aparece veredicto, puntuación, juegos compatibles, mejoras recomendadas
- [ ] En el chat: escribe "Hola" + Enter → recibe respuesta

### Test 6: Scheduler
- [ ] Click en nav "SCHEDULER"
- [ ] Click "INICIAR" → status cambia a verde "SCHEDULER ACTIVO"
- [ ] Crea una regla: nombre "Test", trigger "explorer.exe", profile "gaming", click "CREAR REGLA"
- [ ] La regla aparece en la lista a la derecha
- [ ] Espera 15-30 segundos → aparece evento en "Actividad Reciente"

### Test 7: Puntos de Restauración
- [ ] Click en nav "RESTAURACIÓN"
- [ ] Escribe descripción "Test demo" → click "CREAR AHORA"
- [ ] El punto aparece en el historial
- [ ] El botón "RESTORE POINT" del header también funciona

### Test 8: Documentación PDF
- [ ] Click en botón "PDF" del header
- [ ] Se descarga `optidriver_documentacion.pdf`
- [ ] Abre el PDF → tiene varias páginas con explicación técnica

---

## ✅ Si TODOS los tests pasan

¡Estás listo para construir el .exe y presentar! Salta al siguiente documento: **`EMPAQUETAR_PARA_OTRO_PC.md`**

## ❌ Si algún test falla

Mira la sección **"Solución de problemas"** del `README_WINDOWS.md` o pregúntame con captura del error.
