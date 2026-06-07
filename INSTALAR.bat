@echo off
pushd "%~dp0"
title Optidriver - Instalacion
color 0B
echo ===============================================
echo   OPTIDRIVER - INSTALACION
echo   Solo hace falta ejecutarlo la PRIMERA vez
echo ===============================================
echo.

REM ----- Verificar Python -----
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [FALTA] Python NO esta instalado
    echo.
    echo  1. Descarga Python 3.12:
    echo     https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
    echo  2. Durante la instalacion MARCA: "Add python.exe to PATH"
    echo  3. Cuando termine, vuelve a ejecutar este INSTALAR.bat
    echo.
    pause & popd & exit /b 1
)
echo [OK] Python detectado:
python --version
echo.

REM ----- Verificar Node -----
node --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [FALTA] Node.js NO esta instalado
    echo.
    echo  1. Descarga Node.js LTS: https://nodejs.org/
    echo  2. Durante la instalacion marca "Add to PATH"
    echo  3. Cuando termine, vuelve a ejecutar este INSTALAR.bat
    echo.
    pause & popd & exit /b 1
)
echo [OK] Node.js detectado:
node --version
echo.

REM ----- Verificar/Instalar Yarn -----
yarn --version >nul 2>&1
if errorlevel 1 (
    echo Instalando yarn...
    call npm install -g yarn
)
echo [OK] Yarn detectado:
yarn --version
echo.

REM ----- Verificar MongoDB -----
sc query MongoDB >nul 2>&1
if errorlevel 1 (
    color 0E
    echo [AVISO] MongoDB NO esta instalado como servicio
    echo.
    echo  1. Descarga MongoDB Community:
    echo     https://www.mongodb.com/try/download/community
    echo  2. Durante la instalacion MARCA: "Install MongoDB as a Service"
    echo  3. Cuando termine, vuelve a ejecutar este INSTALAR.bat
    echo.
    pause & popd & exit /b 1
)
echo [OK] MongoDB detectado
echo.

REM ----- Crear backend\.env si no existe -----
if not exist "backend\.env" (
    echo Creando backend\.env...
    > backend\.env echo MONGO_URL=mongodb://localhost:27017
    >> backend\.env echo DB_NAME=optidriver
    >> backend\.env echo CORS_ORIGINS=*
    >> backend\.env echo EMERGENT_LLM_KEY=sk-emergent-d83C7B7B88130617f2
    echo [OK] backend\.env creado
) else (
    echo [OK] backend\.env ya existe
)
echo.

REM ----- Crear frontend\.env si no existe -----
if not exist "frontend\.env" (
    echo Creando frontend\.env...
    > frontend\.env echo REACT_APP_BACKEND_URL=http://localhost:8001
    >> frontend\.env echo WDS_SOCKET_PORT=0
    echo [OK] frontend\.env creado
) else (
    echo [OK] frontend\.env ya existe
)
echo.

REM ----- Instalar dependencias Python -----
echo ===============================================
echo  Instalando dependencias Python...
echo ===============================================
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
python -m pip install wmi pywin32
echo.

REM ----- Instalar dependencias Frontend -----
echo ===============================================
echo  Instalando dependencias Frontend
echo  (la primera vez tarda 3-5 minutos)
echo ===============================================
pushd frontend
call yarn install
if errorlevel 1 (
    color 0C
    echo [ERROR] yarn install fallo
    popd & popd & pause & exit /b 1
)
popd

echo.
color 0A
echo ===============================================
echo   INSTALACION COMPLETA
echo.
echo   Ahora ejecuta Optidriver.bat para arrancar
echo   la aplicacion.
echo ===============================================
echo.
pause
popd
