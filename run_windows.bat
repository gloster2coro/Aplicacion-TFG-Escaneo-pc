@echo off
REM =====================================================
REM Optidriver - Launcher Windows
REM Se ejecuta siempre desde su propia carpeta
REM =====================================================

pushd "%~dp0"
echo ============================================
echo   OPTIDRIVER v1.0 - Launcher
echo   Carpeta: %CD%
echo ============================================

REM Verificar que estamos en la carpeta correcta
if not exist "backend\server.py" (
    echo [ERROR] No se encuentra backend\server.py
    echo         Este .bat debe estar en la carpeta raiz del proyecto
    pause
    popd
    exit /b 1
)

REM Comprobar permisos de admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Ejecutando con permisos de administrador
) else (
    echo [AVISO] No se estan usando permisos de administrador
    echo         Las optimizaciones y restore points funcionaran en modo SIMULACION
    echo         Para funcionalidad real, clic derecho -^> "Ejecutar como administrador"
    echo.
)

REM Comprobar Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo         Descarga Python 3.11 o 3.12 desde https://www.python.org/downloads/
    pause
    popd
    exit /b 1
)

REM Comprobar MongoDB
sc query MongoDB >nul 2>&1
if %errorLevel% neq 0 (
    echo [AVISO] Servicio MongoDB no detectado.
    echo         Descarga: https://www.mongodb.com/try/download/community
    echo         La app no arrancara correctamente sin MongoDB.
    pause
)

echo.
echo [1/3] Instalando dependencias Python...
python -m pip install -r backend\requirements.txt
python -m pip install wmi pywin32

echo.
echo [2/3] Instalando dependencias frontend (si hace falta)...
if not exist "frontend\node_modules" (
    pushd frontend
    call yarn install
    popd
)

echo.
echo [3/3] Arrancando servicios...
start "Optidriver Backend" cmd /k "cd /d %CD%\backend && python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
timeout /t 3 /nobreak >nul
start "Optidriver Frontend" cmd /k "cd /d %CD%\frontend && yarn start"

echo.
echo ============================================
echo   Optidriver arrancando en http://localhost:3000
echo   Backend API en http://localhost:8001/api
echo ============================================
echo.
echo Presiona cualquier tecla para cerrar este launcher
echo (los procesos backend/frontend seguiran corriendo en sus ventanas)
pause >nul
popd
