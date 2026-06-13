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
    if [ ! -d ".venv_wsl" ]; then
        uv venv --python 3.12 --quiet .venv_wsl
    fi
    source .venv_wsl/bin/activate
    uv pip install --quiet -r requirements.txt
    if command -v nvidia-smi &> /dev/null; then
        echo "[SISTEMA] GPU NVIDIA detectada. Instalando soporte CUDA para JAX..."
        uv pip install --quiet "jax[cuda12]"
    fi
else
    echo "[SISTEMA] UV no detectado, usando motor Python estándar."
    if [ ! -d ".venv_wsl" ]; then
        python3 -m venv .venv_wsl
    fi
    source .venv_wsl/bin/activate
    python3 -m pip install --quiet -r requirements.txt
    if command -v nvidia-smi &> /dev/null; then
        echo "[SISTEMA] GPU NVIDIA detectada. Instalando soporte CUDA para JAX..."
        python3 -m pip install --quiet "jax[cuda12]"
    fi
fi

# Ejecutar el script principal
.venv_wsl/bin/python ganabaloto.py

# Mantener la consola abierta al finalizar
echo ""
read -p "Presiona [Enter] para salir..."
