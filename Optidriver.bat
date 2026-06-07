@echo off
pushd "%~dp0"
title Optidriver Launcher
color 0B

echo ===============================================
echo   OPTIDRIVER v1.0
echo   Creado por @albertomosu
echo ===============================================
echo.

REM ----- Verificar instalacion previa -----
if not exist "backend\.env" (
    color 0C
    echo [ERROR] Falta backend\.env
    echo Ejecuta primero INSTALAR.bat
    pause & popd & exit /b 1
)
if not exist "frontend\node_modules" (
    color 0C
    echo [ERROR] Falta frontend\node_modules
    echo Ejecuta primero INSTALAR.bat
    pause & popd & exit /b 1
)

REM ----- Permisos admin -----
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Permisos de administrador
    echo      Las optimizaciones se aplicaran REALMENTE
) else (
    echo [AVISO] Sin permisos de administrador
    echo         Funcionara en modo SIMULACION (seguro)
    echo         Para modo real: clic derecho -^> "Ejecutar como administrador"
)
echo.

REM ----- Arrancar MongoDB si no esta -----
sc query MongoDB | findstr "RUNNING" >nul
if errorlevel 1 (
    echo Arrancando MongoDB...
    net start MongoDB >nul 2>&1
    if errorlevel 1 (
        color 0E
        echo [AVISO] No se pudo arrancar MongoDB.
        echo         La app no podra guardar datos.
        echo         Comprueba que MongoDB este instalado correctamente.
        timeout /t 3 >nul
    ) else (
        echo [OK] MongoDB arrancado
    )
) else (
    echo [OK] MongoDB ya esta corriendo
)
echo.

REM ----- Arrancar Backend y Frontend -----
echo ===============================================
echo   Arrancando Optidriver...
echo.
echo   Backend:  http://localhost:8001
echo   Frontend: http://localhost:3000
echo.
echo   El navegador se abrira automaticamente en 30s
echo ===============================================
echo.

start "Optidriver Backend" cmd /k "cd /d %CD%\backend && python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
timeout /t 5 /nobreak >nul

start "Optidriver Frontend" cmd /k "cd /d %CD%\frontend && yarn start"

color 0A
echo.
echo  Las 2 ventanas estan arrancando:
echo    - "Optidriver Backend"  (servidor API en puerto 8001)
echo    - "Optidriver Frontend" (interfaz web en puerto 3000)
echo.
echo  Para DETENER la aplicacion:
echo    Cierra las 2 ventanas (Optidriver Backend y Frontend)
echo.
echo  Puedes cerrar esta ventana cuando se abra el navegador.
echo.
pause
popd
