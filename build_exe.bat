@echo off
REM =========================================
REM Optidriver - PyInstaller .exe build
REM Se ejecuta siempre desde su propia carpeta
REM =========================================

pushd "%~dp0"
echo ============================================
echo   OPTIDRIVER - Build .exe
echo   Carpeta: %CD%
echo ============================================

REM Verificar que estamos en la carpeta correcta
if not exist "launcher.py" (
    echo [ERROR] No se encuentra launcher.py
    echo         Este .bat debe estar en la carpeta raiz del proyecto
    echo         junto a launcher.py, backend\ y frontend\
    pause
    popd
    exit /b 1
)

echo.
echo [1/4] Verificando Python y pip...
python --version
if %errorLevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo         Descarga Python 3.11 o 3.12 desde https://www.python.org/downloads/
    echo         IMPORTANTE: marca "Add Python to PATH" durante la instalacion
    pause
    popd
    exit /b 1
)

REM Usar python -m pip en lugar de pip.exe directamente (evita el error del launcher)
python -m pip install --upgrade pip
python -m pip install pyinstaller
if %errorLevel% neq 0 (
    echo [ERROR] No se pudo instalar PyInstaller.
    echo         Intenta con: python -m pip install --user pyinstaller
    pause
    popd
    exit /b 1
)

echo.
echo [2/4] Instalando dependencias backend...
python -m pip install -r backend\requirements.txt
python -m pip install wmi pywin32 emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

echo.
echo [3/4] Construyendo frontend (production build)...
if not exist "frontend\node_modules" (
    echo [INFO] node_modules no existe, ejecutando yarn install...
    pushd frontend
    call yarn install
    popd
)
pushd frontend
call yarn build
if %errorLevel% neq 0 (
    echo [ERROR] Fallo el build del frontend
    popd
    popd
    pause
    exit /b 1
)
popd

echo.
echo [4/4] Empaquetando con PyInstaller...
python -m PyInstaller ^
    --name "Optidriver" ^
    --onefile ^
    --noconfirm ^
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
    launcher.py

if %errorLevel% neq 0 (
    echo.
    echo [ERROR] PyInstaller fallo. Revisa los mensajes de arriba.
    pause
    popd
    exit /b 1
)

echo.
echo ============================================
echo   BUILD COMPLETADO
echo   Ejecutable: %CD%\dist\Optidriver.exe
echo ============================================
echo.
echo IMPORTANTE:
echo   - MongoDB debe estar corriendo en localhost:27017
echo   - Ejecuta Optidriver.exe como administrador para funciones reales
echo.
pause
popd
