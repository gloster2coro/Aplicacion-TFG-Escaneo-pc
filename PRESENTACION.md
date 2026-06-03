# 🎓 OPTIDRIVER - PRESENTACIÓN PARA PROFESORES

Documento de presentación técnica del proyecto. Pensado para leer ante el tribunal académico.

---

## 1. ¿Qué es Optidriver?

Optidriver es una aplicación de escritorio para Windows diseñada para **optimizar el rendimiento del sistema operativo**, **gestionar drivers** y **ofrecer recomendaciones inteligentes de hardware mediante IA**.

La aplicación parte de un problema real: muchos usuarios tienen ordenadores potentes pero **con configuraciones no adaptadas al uso que les dan**. Por ejemplo, un PC para gaming pierde FPS porque está ejecutando OneDrive, Teams y otros procesos en segundo plano. Optidriver detecta estos casos y los optimiza automáticamente según el perfil de uso que elija el usuario.

---

## 2. Objetivos del proyecto

1. **Automatizar la optimización** del sistema según perfiles de uso (Gaming, Oficina, Óptimo).
2. **Centralizar la detección y actualización de drivers** en una sola interfaz.
3. **Ofrecer recomendaciones de hardware personalizadas** mediante inteligencia artificial, adaptadas al presupuesto del usuario.
4. **Garantizar la seguridad** mediante creación automática de puntos de restauración antes de cualquier cambio crítico.
5. **Proporcionar una interfaz moderna** estilo "command center", inspirada en los paneles de control profesionales.

---

## 3. Arquitectura técnica

Optidriver utiliza una **arquitectura cliente-servidor local**: aunque es una aplicación de escritorio, internamente funciona como una aplicación web que se ejecuta exclusivamente en el ordenador del usuario.

| Componente | Tecnología | Función |
|------------|------------|---------|
| Backend | **Python 3.12 + FastAPI** | Lógica de negocio, integración con Windows API, IA |
| Frontend | **React 19 + Shadcn UI + TailwindCSS** | Interfaz de usuario tactical dark-theme |
| Base de datos | **MongoDB** | Persistencia de perfiles, logs, sesiones IA |
| Inteligencia Artificial | **GPT-5.2 (OpenAI)** | Recomendaciones inteligentes |
| Acceso al sistema | **psutil, WMI, winreg, PowerShell** | Lectura/modificación de Windows |
| Empaquetado | **PyInstaller** | Compilación a .exe distribuible |

### ¿Por qué esta arquitectura?

La elección de tecnologías web (React + FastAPI) sobre alternativas nativas (como C# WPF o Python tkinter) se basa en **tres ventajas clave**:

1. **Interfaz más moderna y mantenible**: el ecosistema React permite componentes reutilizables, animaciones fluidas y diseño responsivo profesional con muy poco código.

2. **Separación clara backend/frontend**: facilita el testing, la escalabilidad y el desarrollo paralelo de funcionalidades.

3. **Distribución sencilla**: PyInstaller bundlea Python + backend + frontend estático en un único `.exe` portable, sin necesidad de instalar runtimes.

---

## 4. Módulos funcionales

### 4.1 - Módulo de Optimización del Sistema

El usuario selecciona uno de tres perfiles:

- **Gaming** — Máximo rendimiento. Cierra procesos no esenciales (OneDrive, Teams, Chrome), activa el plan de energía "Alto rendimiento" y desactiva efectos visuales.
- **Oficina** — Productividad equilibrada. Mantiene efectos visuales y plan balanceado.
- **Óptimo** — Balance automático para uso diario.

**Implementación**: El motor de optimización (`optimizer.py`) mantiene una **lista blanca de procesos críticos** del sistema operativo (smss.exe, csrss.exe, explorer.exe, dwm.exe, svchost.exe, etc.) que **nunca** se tocan. Solo se cierran procesos no esenciales identificados por nombre, garantizando estabilidad del sistema.

### 4.2 - Módulo de Gestión de Drivers

Utiliza **WMI (Windows Management Instrumentation)** para detectar el hardware real del ordenador: CPU, GPU, RAM, placa base. Lista los drivers instalados, identifica los desactualizados comparando versiones, y permite actualización individual o por lotes con confirmación previa.

La interfaz incluye un "HUD de hardware" con imagen del motherboard sobre la cual se superponen los datos técnicos detectados, simulando un panel de diagnóstico profesional.

### 4.3 - Asistente IA (GPT-5.2)

Este es el módulo diferenciador del proyecto. El asistente recibe:
- El reporte completo de hardware detectado
- El perfil de uso seleccionado
- El presupuesto del usuario (bajo / medio / alto)

Y devuelve un análisis estructurado en formato JSON con:
- **Veredicto general** (APTO, PARCIALMENTE_APTO, NO_APTO)
- **Puntuación** de 0 a 100
- **Lista de juegos compatibles** con FPS estimados y configuración gráfica recomendada
- **Lista de juegos NO compatibles** con motivos técnicos
- **Mejoras de hardware específicas** (modelo concreto y precio en euros)
- **Equipos completos recomendados** si el upgrade no merece la pena

La interfaz se presenta como un **terminal estilo consola** con tipografía monoespaciada (IBM Plex Mono), reforzando la estética técnica de la app.

### 4.4 - Sistema de Restauración

Antes de aplicar cualquier optimización o actualizar drivers, Optidriver crea automáticamente un **punto de restauración del sistema** mediante PowerShell (`Checkpoint-Computer`). Esto permite revertir cualquier cambio si algo sale mal.

También se pueden crear puntos manualmente desde la interfaz.

### 4.5 - Scheduler Automático

Funcionalidad avanzada: el usuario define **reglas** del tipo "si detectas el proceso X corriendo, aplica el perfil Y". Por ejemplo: cuando arranca `steam.exe`, aplicar automáticamente el perfil Gaming. El scheduler corre en segundo plano comprobando procesos cada 15 segundos.

### 4.6 - Comparativa Before/After

Cada vez que se aplica una optimización, Optidriver captura una "fotografía" de las métricas (CPU, RAM, disco, número de procesos) **antes** y **después**. La interfaz muestra una tabla comparativa con la mejora porcentual de cada métrica, dando feedback visual claro al usuario sobre el impacto de la optimización.

---

## 5. Decisiones técnicas destacadas

### 5.1 - Modo simulación por defecto
Por seguridad, todas las operaciones críticas se ejecutan en **modo simulación** salvo que el usuario lo desactive explícitamente. Esto evita que un click accidental cierre procesos importantes o modifique el registro de Windows.

### 5.2 - Lista blanca de procesos críticos
En lugar de una lista negra (procesos a cerrar), Optidriver usa una **lista blanca de procesos a NO tocar**. Este enfoque defensivo garantiza que ningún proceso crítico del kernel (smss, csrss, lsass, etc.) se vea afectado.

### 5.3 - Estructura JSON para la IA
El asistente IA está forzado a responder en JSON estructurado, no en texto libre. Esto permite parsear la respuesta y renderizarla en componentes específicos de la UI, asegurando una experiencia consistente.

### 5.4 - Documentación generada dinámicamente
El PDF de documentación técnica se genera **en tiempo real** desde el backend usando ReportLab. No es un PDF estático: se reconstruye cada vez que el usuario lo descarga, incluyendo datos actualizados sobre la API REST disponible.

---

## 6. Base de datos

Optidriver usa MongoDB con las siguientes colecciones:

| Colección | Contenido |
|-----------|-----------|
| `profiles` | Perfil activo seleccionado por el usuario |
| `optimization_logs` | Historial de optimizaciones aplicadas (con before/after) |
| `driver_updates` | Registro de actualizaciones de drivers |
| `restore_points` | Historial de puntos de restauración |
| `ai_sessions` | Sesiones del asistente IA (análisis completos) |
| `ai_chat_messages` | Mensajes del chat libre con la IA |
| `scheduler_rules` | Reglas configuradas en el scheduler automático |
| `scheduler_events` | Eventos disparados por el scheduler |

La elección de MongoDB sobre SQL se justifica por la **flexibilidad de schema**: los logs de la IA tienen estructura compleja y variable (listas anidadas de juegos, mejoras, equipos recomendados) que se modelan mejor como documentos JSON que como filas relacionales.

---

## 7. Pruebas y validación

El proyecto incluye **24 tests automatizados de backend** (pytest) y **11 flujos end-to-end del frontend** (Playwright). Todos pasan al 100%. Los tests cubren:

- Health checks de todos los endpoints REST
- Persistencia en MongoDB tras cada operación crítica
- Creación automática de restore points
- Integración con GPT-5.2 (con timeouts adecuados de 120 segundos)
- Navegación entre todas las páginas del frontend
- Modales de confirmación de driver update
- Activación/desactivación del scheduler
- Generación del PDF de documentación

---

## 8. Aprendizajes y retos del proyecto

### Reto 1: Acceso a APIs de Windows desde Python web
El acceso al hardware real y a operaciones del sistema operativo (cerrar procesos, modificar registro, crear restore points) requirió combinar varias librerías: `psutil` para métricas multiplataforma, `wmi` para hardware via WMI, `winreg` para registro, y `subprocess` para PowerShell. La integración fue uno de los retos técnicos principales.

### Reto 2: Estructurar la salida de la IA
Lograr que GPT-5.2 devuelva consistentemente JSON válido y parseable, sin desviarse a texto libre, requirió un **system prompt detallado** que define exactamente el esquema esperado. Se implementó parseo defensivo que detecta y limpia bloques markdown que el modelo a veces incluye.

### Reto 3: Empaquetado distribuible
Convertir una aplicación web (que normalmente requiere Python, Node.js y un servidor MongoDB) en un único `.exe` portable mediante PyInstaller fue complejo. Hubo que configurar manualmente los `--hidden-import` para cada submódulo de uvicorn, motor, wmi, etc., porque PyInstaller no los detectaba automáticamente al ser imports dinámicos.

### Reto 4: Diseño de la interfaz
El brief del proyecto pedía una interfaz "profesional". En lugar de aplicar plantillas genéricas, se optó por un diseño **"Performance Pro"** propio: tema oscuro tactical, tipografías Barlow Condensed e IBM Plex Mono, sin bordes redondeados, con acentos azules y rojos. La estética busca evocar paneles de control militares o de centros de comando, alineándose con la naturaleza técnica de la aplicación.

---

## 9. Posibles mejoras futuras

1. **Detección real de drivers via pnputil**: actualmente la lista de drivers se simula. Una mejora sería parsear la salida de `pnputil /enum-drivers` para mostrar los drivers reales del PC.
2. **Notificaciones System Tray**: integrar un icono en la bandeja del sistema con notificaciones cuando el scheduler aplique cambios.
3. **Telemetría anónima**: con opt-in del usuario, recopilar estadísticas globales tipo "media de FPS ganados por perfil Gaming" para crear un ranking público y validar el impacto real.
4. **Multi-idioma**: actualmente solo en español. Añadir inglés y portugués ampliaría el público objetivo.
5. **Integración con Steam API**: detectar qué juegos tiene instalados el usuario para personalizar el análisis de compatibilidad.

---

## 10. Conclusión

Optidriver demuestra cómo una **arquitectura web moderna** (React + FastAPI) puede empaquetarse como aplicación de escritorio Windows distribuible, aprovechando lo mejor de ambos mundos: la potencia y mantenibilidad del desarrollo web junto con el acceso completo al sistema operativo nativo.

La integración de **inteligencia artificial generativa** (GPT-5.2) eleva el proyecto de una simple utilidad de limpieza a un **asistente experto** que da consejos personalizados de hardware adaptados al presupuesto del usuario, algo que ningún producto comercial del segmento ofrece actualmente.

Finalmente, el enfoque defensivo (modo simulación, listas blancas, puntos de restauración automáticos) garantiza que la aplicación sea **segura para usuarios no técnicos**, una característica esencial para una herramienta que modifica configuraciones críticas del sistema operativo.

---

## 📊 Datos rápidos para la defensa

- **Líneas de código**: ~3500 (backend Python + frontend React)
- **Endpoints REST**: 24
- **Páginas frontend**: 5 (Dashboard, Optimizer, Drivers, AI, Scheduler, Restore)
- **Cobertura de tests**: 100% en flujos críticos
- **Tiempo de desarrollo**: ~2 iteraciones (MVP + features avanzadas)
- **Dependencias backend**: 11 (slim)
- **Tamaño del .exe final**: ~150 MB (incluye Python embebido)

---

## 🎤 Posibles preguntas del tribunal y respuestas

**P: ¿Por qué no hicisteis una app nativa con C# o Electron?**
R: Evaluamos las opciones. C# requería conocer WPF/WinForms y limitaba la reutilización del código. Electron habría aumentado mucho el tamaño del binario (>200 MB solo Chromium). FastAPI + React + PyInstaller nos dio la mejor relación entre productividad de desarrollo, calidad de UI y portabilidad.

**P: ¿Cómo garantizáis que no se cierre un proceso crítico?**
R: Mediante una lista blanca explícita de procesos del kernel y del sistema (definida en `optimizer.py`). El motor verifica cada candidato contra esta lista antes de proceder. Además, por defecto todo se ejecuta en modo simulación.

**P: ¿La IA realmente entiende el hardware del usuario?**
R: Sí. Le pasamos en el prompt un JSON estructurado con CPU (modelo, núcleos, frecuencia), RAM (GB totales y disponibles), GPU (modelo y memoria), motherboard. GPT-5.2 lo compara con su conocimiento de requisitos de juegos y mercado de componentes. Hemos validado que las recomendaciones de precios y modelos son realistas y actuales.

**P: ¿Funciona sin internet?**
R: Las funciones core (optimización, monitoreo, drivers, restore points, scheduler) sí. Solo el asistente IA necesita internet porque GPT-5.2 está en la nube de OpenAI.

**P: ¿Es seguro contra malware o uso indebido?**
R: El código es abierto y revisable. No hace conexiones a servidores propios, solo a la API de OpenAI para el asistente. Todas las operaciones críticas requieren permisos de administrador explícitos.
