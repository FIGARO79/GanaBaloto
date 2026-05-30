@echo off
TITLE GanaBaloto - Instalacion Inicial
SETLOCAL EnableDelayedExpansion

echo =======================================================
echo        🎱 GanaBaloto - Instalador del Entorno 🎱
echo =======================================================
echo.

:: 1. Verificar Python
echo [1/4] Verificando instalacion de Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no detectado. Por favor instala Python 3.10+ y agregalo al PATH.
    echo Visita: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python detectado.

:: 2. Instalar UV (Opcional pero recomendado para velocidad)
echo.
echo [2/4] Configurando motor de paquetes (UV)...
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] UV no detectado. Intentando instalacion rapida...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" 2>nul
    set "PATH=%PATH%;%USERPROFILE%\.local\bin"
    
    where uv >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo [INFO] No se pudo instalar UV. Se usara PIP (mas lento).
        set USE_UV=0
    ) else (
        echo [OK] UV instalado correctamente.
        set USE_UV=1
    )
) else (
    echo [OK] UV ya esta instalado.
    set USE_UV=1
)

:: 3. Crear Entorno Virtual
echo.
echo [3/4] Creando entorno virtual (.venv)...
if exist .venv (
    echo [INFO] El entorno virtual ya existe.
) else (
    if %USE_UV% EQU 1 (
        uv venv --python 3.12 .venv
    ) else (
        python -m venv .venv
    )
    echo [OK] Entorno virtual creado.
)

:: 4. Instalar Dependencias
echo.
echo [4/4] Instalando librerias (esto puede tardar un momento)...
if %USE_UV% EQU 1 (
    call .venv\Scripts\activate
    uv pip install -r requirements.txt
    nvidia-smi >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [INFO] GPU NVIDIA detectada. Instalando soporte CUDA para JAX...
        uv pip install "jax[cuda12]"
    )
) else (
    call .venv\Scripts\activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    nvidia-smi >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [INFO] GPU NVIDIA detectada. Instalando soporte CUDA para JAX...
        python -m pip install "jax[cuda12]"
    )
)
echo [OK] Dependencias instaladas.

echo.
echo =======================================================
echo    ✅ INSTALACION COMPLETADA CON EXITO
echo =======================================================
echo.
echo Ahora puedes ejecutar el programa usando:
echo    - ejecutar_baloto.bat
echo.
echo O puedes actualizar los resultados ahora mismo con:
echo    - python actualizar_resultados.py (dentro del entorno)
echo.

set /p UPDATE="¿Deseas intentar actualizar los resultados de Baloto ahora? (s/n): "
if /i "%UPDATE%"=="s" (
    echo.
    echo Actualizando resultados...
    python actualizar_resultados.py
)

echo.
echo Instalacion finalizada.
pause
