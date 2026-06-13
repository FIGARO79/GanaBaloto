@echo off
TITLE GanaBaloto - Ejecucion Automatica

echo Iniciando GanaBaloto...

:: Ir al directorio del script
cd /d "%~dp0"

:: Verificar si uv está instalado
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [SISTEMA] UV no detectado. Intentando instalar UV para mejorar el rendimiento...
    :: Intentar PowerShell primero
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" 2>nul
    
    :: Agregar la ruta por defecto de UV al PATH de esta sesión
    set "PATH=%PATH%;%USERPROFILE%\.local\bin"
    
    :: Verificar si PowerShell funcionó
    where uv >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo [SISTEMA] Instalacion de PowerShell fallo. Intentando con PIP...
        python -m pip install --quiet uv 2>nul
    )

    :: Verificacion final
    where uv >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo [ADVERTENCIA] No se pudo instalar UV automaticamente. Se usara Python estandar.
        set USE_UV=0
    ) else (
        echo [EXITO] UV instalado correctamente.
        set USE_UV=1
    )
) else (
    set USE_UV=1
)

if %USE_UV% EQU 1 (
    echo [SISTEMA] Usando motor UV para maximo rendimiento.
    :: Crear entorno solo si no existe
    if not exist .venv (
        uv venv --python 3.12 --quiet .venv
    )
    call .venv\Scripts\activate
    uv pip install --quiet -r requirements.txt
) else (
    echo [SISTEMA] Usando motor Python estandar.
    if not exist .venv (
        python -m venv .venv
    )
    call .venv\Scripts\activate
    python -m pip install --quiet -r requirements.txt
)

:: Ejecutar el script
.venv\Scripts\python ganabaloto.py

:: Desactivar entorno virtual
call deactivate

echo.
echo [INFO] El programa ha finalizado. Puedes cerrar esta ventana manualmente.
powershell -NoExit
