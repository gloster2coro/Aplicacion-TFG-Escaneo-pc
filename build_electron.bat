@echo off
REM =========================================
REM Optidriver - Electron .exe build
REM Se ejecuta siempre desde su propia carpeta
REM =========================================

pushd "%~dp0"
echo ============================================
echo   OPTIDRIVER - Build Electron
echo   Carpeta: %CD%
echo ============================================

if not exist "electron\package.json" (
    echo [ERROR] No se encuentra electron\package.json
    echo         Ejecuta este .bat desde la carpeta raiz del proyecto
    pause
    popd
    exit /b 1
)

echo.
echo [1/3] Construyendo frontend...
pushd frontend
if not exist "node_modules" call yarn install
call yarn build
if %errorLevel% neq 0 (
    echo [ERROR] Fallo build del frontend
    popd
    popd
    pause
    exit /b 1
)
popd

echo.
echo [2/3] Instalando dependencias Electron...
pushd electron
call yarn install
if %errorLevel% neq 0 (
    echo [ERROR] yarn install fallo en electron
    popd
    popd
    pause
    exit /b 1
)

echo.
echo [3/3] Empaquetando con electron-builder...
call yarn build
if %errorLevel% neq 0 (
    echo [ERROR] electron-builder fallo
    popd
    popd
    pause
    exit /b 1
)
popd

echo.
echo ============================================
echo   BUILD COMPLETADO
echo   Instalador: %CD%\dist-electron\
echo   Ejecuta "Optidriver Setup 1.0.0.exe"
echo ============================================
pause
popd
