# 🚀 OPTIDRIVER - Guía de Instalación en Windows

Aplicación local para optimización de Windows con asistente IA (GPT-5.2), gestión de drivers y scheduler automático.

---

## ✅ Requisitos previos

Instala estos 3 programas en tu Windows 10/11:

### 1. Python 3.12 (NO 3.14)
- 👉 Descarga: https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
- Durante la instalación: **MARCA la casilla `Add python.exe to PATH`**
- Verifica: abre CMD y ejecuta `python --version` (debe responder `Python 3.12.x`)

### 2. Node.js 18+ con Yarn
- 👉 Descarga Node.js LTS: https://nodejs.org/
- Durante la instalación: marca también **"Add to PATH"**
- Abre un CMD nuevo y ejecuta:
  ```cmd
  npm install -g yarn
  yarn --version
  ```

### 3. MongoDB Community Server
- 👉 Descarga: https://www.mongodb.com/try/download/community
- Instalar como **servicio** (marca "Install MongoDB as a Service" durante el setup)
- Verifica en CMD: `sc query MongoDB` → debe decir `STATE: RUNNING`

---

## 📥 Instalación de Optidriver

### Paso 1: Descargar el proyecto

**Opción A** - Desde GitHub (recomendado):
```cmd
git clone https://github.com/TU_USUARIO/optidriver.git C:\Optidriver
```

**Opción B** - Descargar ZIP:
1. En GitHub → botón verde "Code" → "Download ZIP"
2. Extraer en `C:\Optidriver\` (la ruta completa debe ser ASCII, sin acentos ni espacios)

### Paso 2: Configurar el archivo `.env`

Crea/edita `C:\Optidriver\backend\.env` con este contenido:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=optidriver
CORS_ORIGINS=*
EMERGENT_LLM_KEY=sk-emergent-d83C7B7B88130617f2
```

### Paso 3: Ejecutar

Abre **CMD como administrador** y:

```cmd
cd /d C:\Optidriver
run_windows.bat
```

Se abrirán 2 ventanas (backend + frontend) y el navegador automáticamente en `http://localhost:3000`.

---

## 🔨 Construir .exe (opcional)

Si quieres un **ejecutable standalone** en lugar de abrir navegador:

```cmd
cd /d C:\Optidriver
build_exe.bat
```

El resultado estará en: `C:\Optidriver\dist\Optidriver.exe`

---

## 🆘 Solución de problemas

### `Fatal error in launcher: Unable to create process`
- Problema con pip de Python 3.14
- **Solución:** desinstalar Python 3.14 y instalar 3.12

### `El sistema no puede encontrar la ruta especificada`
- Estás ejecutando el .bat desde otra carpeta
- **Solución:** siempre ejecuta `cd /d C:\Optidriver` antes

### `Couldn't find a package.json file in "C:\Windows\System32"`
- Mismo problema de ruta incorrecta
- **Solución:** `cd /d C:\Optidriver` antes de ejecutar

### `SyntaxError: Missing semicolon` en api.js
- Archivo corrupto durante la descarga del ZIP
- **Solución:** usar `git clone` (Opción A) en lugar de descargar ZIP

### `ModuleNotFoundError: No module named 'wmi'`
- Falta instalar dependencias Windows-específicas
- **Solución:** `python -m pip install wmi pywin32`

### `MongoDB connection refused`
- MongoDB no está corriendo
- **Solución:** `net start MongoDB` (como admin)

### La IA (GPT-5.2) no responde
- Clave EMERGENT_LLM_KEY no configurada o sin saldo
- **Solución:** verifica el archivo `backend\.env` y que tengas créditos en Emergent

---

## 🛡️ Modo simulación vs real

Por defecto Optidriver funciona en **modo simulación**: te muestra qué haría pero no lo aplica (seguro).

Para **modo real** (cerrar procesos, modificar registro, crear restore points):
1. Ejecutar `run_windows.bat` con clic derecho → **"Ejecutar como administrador"**
2. En el código, algunos endpoints aceptan `simulate: false` (ya está expuesto desde la UI)

⚠️ Siempre se crea un **punto de restauración automático** antes de aplicar cualquier cambio crítico.

---

## 📂 Estructura del proyecto

```
Optidriver/
├── backend/                 # FastAPI + Python
│   ├── server.py
│   ├── optidriver/
│   │   ├── hardware.py     # Detección CPU/GPU/RAM
│   │   ├── optimizer.py    # Lógica de perfiles
│   │   ├── drivers.py      # Gestión drivers
│   │   ├── restore.py      # Puntos restauración
│   │   ├── ai_assistant.py # GPT-5.2
│   │   ├── scheduler.py    # Auto-scheduler
│   │   ├── metrics_compare.py
│   │   └── docs.py         # PDF
│   ├── requirements.txt
│   └── .env                # Credenciales (crea este archivo)
├── frontend/                # React + Shadcn
│   ├── src/
│   └── package.json
├── electron/                # Wrapper Electron (opcional)
├── launcher.py              # Entry point para .exe
├── run_windows.bat          # Arrancar en modo dev
├── build_exe.bat            # Construir .exe con PyInstaller
├── build_electron.bat       # Construir installer Electron
├── WINDOWS_VALIDATION_CHECKLIST.md
└── README_WINDOWS.md        # Este archivo
```

---

## 🔗 URLs locales

- Frontend: http://localhost:3000
- Backend API: http://localhost:8001/api
- PDF docs: http://localhost:8001/api/docs/pdf
- MongoDB: mongodb://localhost:27017

---

¿Problemas? Revisa primero `WINDOWS_VALIDATION_CHECKLIST.md` para tests paso a paso.
