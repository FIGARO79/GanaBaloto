@echo off
TITLE GanaBaloto - Ejecucion Automatica

echo Iniciando GanaBaloto...

:: Verificar si uv está instalado
where uv >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [SISTEMA] Usando motor UV para maximo rendimiento.
    :: Crear entorno solo si no existe
    if not exist .venv (
        uv venv --python 3.12 --quiet .venv
    )
    call .venv\Scripts\activate
    uv pip install --quiet -r requirements.txt
) else (
    echo [SISTEMA] UV no detectado, usando motor Python estandar.
    if not exist .venv (
        python -m venv .venv
    )
    call .venv\Scripts\activate
    python -m pip install --quiet -r requirements.txt
)

:: Ejecutar el script
python ganabaloto.py

echo.
echo Presiona cualquier tecla para salir...
pause > nul
