#!/bin/bash

# GanaBaloto - Script de ejecución optimizada con UV
export PATH="$HOME/.local/bin:$PATH"

echo "Iniciando GanaBaloto con entorno optimizado..."

# Ir al directorio del script
cd "$(dirname "$0")"

# Verificar si uv está instalado, si no, usar python estándar
if command -v uv &> /dev/null
then
    echo "[SISTEMA] Usando motor UV para máximo rendimiento."
    # Crear el entorno solo si no existe para evitar prompts
    if [ ! -d ".venv" ]; then
        uv venv --python 3.12 --quiet .venv
    fi
    source .venv/bin/activate
    uv pip install --quiet -r requirements.txt
else
    echo "[SISTEMA] UV no detectado, usando motor Python estándar."
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    python3 -m pip install --quiet -r requirements.txt
fi

# Ejecutar el script principal
.venv/bin/python ganabaloto.py

# Mantener la consola abierta al finalizar
echo ""
read -p "Presiona [Enter] para salir..."
