@echo off
setlocal EnableDelayedExpansion
pushd "%~dp0"

echo ===============================================
echo   OPTIDRIVER v1.0 - Launcher
echo   Carpeta proyecto: %CD%
echo ===============================================
echo.

REM ----- Verificaciones previas -----
if not exist "backend\server.py" (
    echo [ERROR] No se encuentra backend\server.py
    echo         Este .bat debe estar en la carpeta raiz del proyecto
    echo         Carpeta actual: %CD%
    pause & popd & exit /b 1
)

REM Permisos admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Ejecutando con permisos de administrador
) else (
    echo [AVISO] Sin permisos de admin - funcionara en modo SIMULACION
    echo         Clic derecho al .bat -^> "Ejecutar como administrador" para modo real
)

REM Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta en el PATH
    echo         Instala Python 3.12 desde https://www.python.org/downloads/
    echo         MARCA "Add python.exe to PATH" durante la instalacion
    pause & popd & exit /b 1
)

REM Node/yarn
yarn --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] yarn no esta instalado
    echo         Instala Node.js desde https://nodejs.org/ y luego: npm install -g yarn
    pause & popd & exit /b 1
)

REM MongoDB (solo aviso)
sc query MongoDB >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Servicio MongoDB no detectado
    echo         Descarga: https://www.mongodb.com/try/download/community
    echo         La app no podra persistir datos sin MongoDB
    echo.
    timeout /t 3 >nul
)

REM .env
if not exist "backend\.env" (
    echo [INFO] Creando backend\.env con valores por defecto...
    (
        echo MONGO_URL=mongodb://localhost:27017
        echo DB_NAME=optidriver
        echo CORS_ORIGINS=*
        echo EMERGENT_LLM_KEY=sk-emergent-d83C7B7B88130617f2
    ) > backend\.env
)

echo [1/3] Instalando dependencias Python...
python -m pip install --upgrade pip --quiet
python -m pip install -r backend\requirements.txt --quiet
python -m pip install wmi pywin32 --quiet 2>nul
echo.

echo [2/3] Instalando dependencias frontend (primera vez puede tardar)...
if not exist "frontend\node_modules" (
    pushd frontend
    call yarn install
    popd
)
echo.

echo [3/3] Arrancando servicios...
start "Optidriver Backend" cmd /k "cd /d %CD%\backend && python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
timeout /t 4 /nobreak >nul
start "Optidriver Frontend" cmd /k "cd /d %CD%\frontend && yarn start"

echo.
echo ===============================================
echo   OPTIDRIVER arrancando...
echo   Frontend:     http://localhost:3000
echo   Backend API:  http://localhost:8001/api
echo ===============================================
echo.
echo Las ventanas "Optidriver Backend" y "Optidriver Frontend"
echo siguen corriendo. CIERRALAS para detener la app.
echo.
pause
popd
endlocal
