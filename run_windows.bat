@echo off
cd /d "%~dp0"
REM ======================================================
REM Optidriver - Launcher para Windows
REM Ejecuta backend + frontend en local
REM Requiere ejecutar como administrador para funciones completas
REM ======================================================

echo =============================================
echo   OPTIDRIVER v1.0 - Launcher
echo =============================================

REM Comprobar permisos de admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Ejecutando con permisos de administrador
) else (
    echo [AVISO] No se estan usagno permisos de administrador
    echo         Las optimizaciones y restore points se ejecutaran en modo SIMULACION
    echo         Para funcionalidad completa, clic derecho -^> "Ejecutar como administrador"
    echo.
)

REM Comprobar MongoDB
sc query MongoDB >nul 2>&1
if %errorLevel% neq 0 (
    echo [AVISO] Servicio MongoDB no detectado. Asegurate de tenerlo instalado y corriendo.
    echo         Descarga: https://www.mongodb.com/try/download/community
    pause
)

echo.
echo [1/3] Instalando dependencias Python (Windows)...
cd backend
python -m pip install -r requirements.txt
python -m pip install wmi pywin32
cd ..

echo.
echo [2/3] Instalando dependencias frontend...
cd frontend
call yarn install
cd ..

echo.
echo [3/3] Arrancando servicios...
start "Optidriver Backend" cmd /k "cd backend && python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
timeout /t 3 /nobreak >nul
start "Optidriver Frontend" cmd /k "cd frontend && yarn start"

echo.
echo =============================================
echo   Optidriver arrancando en http://localhost:3000
echo   Backend API en http://localhost:8001/api
echo =============================================
echo.
echo Presiona cualquier tecla para cerrar este launcher
echo (los procesos backend/frontend seguiran corriendo en sus ventanas)
pause >nul
