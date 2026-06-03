# 📦 EMPAQUETAR OPTIDRIVER PARA OTRO PC

Guía para llevar Optidriver a otro ordenador (el del aula, del profesor, de un compañero) con la mínima fricción posible.

---

## 🎯 ¿Qué necesita el otro PC?

Optidriver es una app web local. Para funcionar en un PC nuevo necesitas:
1. **El ejecutable** `Optidriver.exe` (lo generas con PyInstaller)
2. **MongoDB Community** instalado (5 minutos, installer estándar)

Eso es todo. **No** necesita Python, Node.js, Yarn, ni nada más.

---

## 🔨 Paso 1: Generar Optidriver.exe en TU PC

En CMD **como administrador**:
```cmd
cd /d C:\Optidriver
build_exe.bat
```

Espera 5-10 minutos. Al finalizar verás:
```
BUILD COMPLETADO
Ejecutable: C:\Optidriver\dist\Optidriver.exe
```

✅ El archivo `Optidriver.exe` resultante pesa **~150 MB** y contiene:
- Python embebido
- Backend FastAPI completo
- Frontend React compilado (HTML + CSS + JS)
- Todas las librerías

---

## 📦 Paso 2: Preparar el paquete de distribución

Crea una carpeta `OptidriverDemo` con:

```
OptidriverDemo/
├── Optidriver.exe                  ← desde dist\Optidriver.exe
├── mongodb-installer.msi           ← descargar de mongodb.com
├── INSTRUCCIONES.txt               ← el que te creo abajo
└── presentacion.pdf                ← el PDF de docs descargado
```

### 2.1 - Copia el .exe
```cmd
copy C:\Optidriver\dist\Optidriver.exe C:\OptidriverDemo\
```

### 2.2 - Descarga MongoDB installer
👉 https://www.mongodb.com/try/download/community → Windows MSI

Renómbralo a `mongodb-installer.msi` y ponlo en `OptidriverDemo/`.

### 2.3 - Descarga el PDF de docs
Con tu Optidriver corriendo en local:
- Abre: http://localhost:8001/api/docs/pdf
- Se descarga `optidriver_documentacion.pdf` → ponlo en `OptidriverDemo/`

### 2.4 - Crea `INSTRUCCIONES.txt`

Copia este contenido en un archivo `INSTRUCCIONES.txt`:

```
========================================
   OPTIDRIVER - INSTALACIÓN
========================================

Requisitos: Windows 10 o 11 (64 bits)

PASO 1: Instalar MongoDB (una vez)
   - Ejecuta mongodb-installer.msi
   - Acepta opciones por defecto
   - IMPORTANTE: marca "Install MongoDB as a Service"
   - Espera a que termine la instalación

PASO 2: Ejecutar Optidriver
   - Clic derecho en Optidriver.exe
   - Selecciona "Ejecutar como administrador"
   - Se abrirá tu navegador automáticamente en localhost
   - ¡Listo!

NOTAS:
   - La primera vez tarda 10-15 segundos en arrancar
   - El asistente IA requiere internet (usa GPT-5.2)
   - Las optimizaciones reales requieren ejecutar como admin
   - Sin admin funciona en modo SIMULACIÓN (seguro)
```

### 2.5 - Comprime la carpeta
- Clic derecho en `OptidriverDemo/` → Enviar a → Carpeta comprimida (.zip)

Resultado: `OptidriverDemo.zip` (~300-400 MB)

---

## 💾 Paso 3: Transferir al PC destino

Opciones:
- 🔌 **USB**: copia el ZIP al pendrive
- ☁️ **Drive/WeTransfer**: sube y descarga
- 🌐 **GitHub Releases**: sube el ZIP como "release" en tu repo

---

## ▶️ Paso 4: Demo en el PC del profesor

1. Descomprimir el ZIP
2. Doble clic en `mongodb-installer.msi` (solo la primera vez en ese PC)
3. Clic derecho en `Optidriver.exe` → "Ejecutar como administrador"
4. El navegador abre solo → demo lista

---

## 🆘 Alternativa: Demo sin .exe (modo desarrollador)

Si no consigues hacer el build del .exe, puedes llevar el código fuente:

1. En tu PC: `git clone` o ZIP del repo de GitHub
2. Copia la carpeta `Optidriver/` al PC destino (USB)
3. En el PC destino instala:
   - Python 3.12 (con "Add to PATH")
   - Node.js + yarn (`npm install -g yarn`)
   - MongoDB Community
4. Ejecutar: `cd Optidriver && run_windows.bat`

Funciona igual pero requiere instalar más cosas en el PC destino.

---

## 💡 Tip para la demo

Ten **siempre abierto** el PDF de documentación (`presentacion.pdf`) en una pestaña aparte. Si la app tarda en cargar o algo va lento durante la demo, puedes mostrar el PDF mientras explicas. Te da margen.

---

## 📊 Tiempos estimados

| Tarea | Tiempo |
|-------|--------|
| Build del .exe en tu PC | 5-10 min |
| Instalación MongoDB en PC destino | 3-5 min |
| Primer arranque del .exe | 10-15 seg |
| Arranques posteriores | 5-10 seg |
| Análisis IA (GPT-5.2) | 30-90 seg |
