@echo off
setlocal EnableDelayedExpansion
pushd "%~dp0"

echo ===============================================
echo   OPTIDRIVER - Build .exe (PyInstaller)
echo   Carpeta proyecto: %CD%
echo ===============================================
echo.

if not exist "launcher.py" (
    echo [ERROR] No se encuentra launcher.py
    echo         Ejecuta este .bat desde la carpeta raiz del proyecto
    pause & popd & exit /b 1
)

echo [1/4] Verificando Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python no esta en PATH. Instala Python 3.12 con "Add to PATH"
    pause & popd & exit /b 1
)
echo.

echo [2/4] Instalando dependencias Python...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] No se pudo actualizar pip
    pause & popd & exit /b 1
)
python -m pip install pyinstaller
python -m pip install -r backend\requirements.txt
python -m pip install wmi pywin32 2>nul
echo.

echo [3/4] Construyendo frontend (production build)...
pushd frontend
if not exist "node_modules" (
    echo    Instalando node_modules (primera vez)...
    call yarn install
    if errorlevel 1 (
        echo [ERROR] yarn install fallo
        popd & popd & pause & exit /b 1
    )
)
call yarn build
if errorlevel 1 (
    echo [ERROR] yarn build fallo. Revisa errores de compilacion arriba.
    popd & popd & pause & exit /b 1
)
popd
echo.

echo [4/4] Empaquetando con PyInstaller...
python -m PyInstaller ^
    --name "Optidriver" ^
    --onefile ^
    --noconfirm ^
    --clean ^
    --add-data "backend;backend" ^
    --add-data "frontend\build;frontend\build" ^
    --hidden-import=uvicorn ^
    --hidden-import=uvicorn.logging ^
    --hidden-import=uvicorn.loops ^
    --hidden-import=uvicorn.loops.auto ^
    --hidden-import=uvicorn.protocols ^
    --hidden-import=uvicorn.protocols.http ^
    --hidden-import=uvicorn.protocols.http.auto ^
    --hidden-import=uvicorn.protocols.websockets ^
    --hidden-import=uvicorn.protocols.websockets.auto ^
    --hidden-import=uvicorn.lifespan ^
    --hidden-import=uvicorn.lifespan.on ^
    --hidden-import=wmi ^
    --hidden-import=win32com ^
    --hidden-import=win32com.client ^
    --hidden-import=emergentintegrations ^
    --hidden-import=motor ^
    --hidden-import=psutil ^
    --hidden-import=reportlab ^
    launcher.py

if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller fallo. Revisa mensajes arriba.
    pause & popd & exit /b 1
)

echo.
echo ===============================================
echo   BUILD COMPLETADO
echo   Ejecutable: %CD%\dist\Optidriver.exe
echo ===============================================
echo.
echo IMPORTANTE:
echo   - MongoDB debe estar corriendo en localhost:27017
echo   - Clic derecho -^> "Ejecutar como administrador" para modo real
echo.
pause
popd
endlocal
