@echo off
REM =========================================
REM Optidriver - Electron .exe build
REM =========================================

echo [1/3] Construyendo frontend...
cd frontend
call yarn build
cd ..

echo [2/3] Instalando dependencias Electron...
cd electron
call yarn install
call yarn add electron electron-builder --dev

echo [3/3] Empaquetando con electron-builder...
call yarn build

echo.
echo Instalador generado en dist-electron\
echo Ejecuta "Optidriver Setup 1.0.0.exe" para instalar
pause
