@echo off
REM =========================================
REM Optidriver - PyInstaller .exe build
REM =========================================

echo [1/4] Instalando PyInstaller...
pip install pyinstaller

echo [2/4] Construyendo frontend (production build)...
cd frontend
call yarn build
cd ..

echo [3/4] Empaquetando con PyInstaller...
pyinstaller ^
    --name "Optidriver" ^
    --onefile ^
    --windowed ^
    --icon=frontend/public/favicon.ico ^
    --add-data "backend;backend" ^
    --add-data "frontend/build;frontend/build" ^
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
    launcher.py

echo [4/4] Listo! Revisa dist\Optidriver.exe
echo.
echo IMPORTANTE: MongoDB debe estar corriendo en localhost:27017
echo             Ejecuta como administrador para funciones reales de Windows
pause
