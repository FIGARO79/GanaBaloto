#!/bin/bash

# GanaBaloto - Script de ejecución optimizada con UV
export PATH="$HOME/.local/bin:$PATH"

echo "Iniciando GanaBaloto con entorno optimizado..."

# Ir al directorio del script
cd "$(dirname "$0")"

# Determinar el entorno virtual a utilizar según el sistema y su validez
if grep -qEi "(Microsoft|WSL)" /proc/version 2>/dev/null; then
    # En WSL, preferir .venv_wsl si es válido, luego .venv si es válido
    if [ -f ".venv_wsl/bin/activate" ]; then
        VENV_DIR=".venv_wsl"
    elif [ -f ".venv/bin/activate" ]; then
        VENV_DIR=".venv"
    else
        VENV_DIR=".venv_wsl"
    fi
else
    # En Linux estándar, preferir .venv si es válido, luego .venv_wsl si es válido
    if [ -f ".venv/bin/activate" ]; then
        VENV_DIR=".venv"
    elif [ -f ".venv_wsl/bin/activate" ]; then
        VENV_DIR=".venv_wsl"
    else
        VENV_DIR=".venv"
    fi
fi

# Verificar si uv está instalado, si no, usar python estánda
if command -v uv &> /dev/null
then
    echo "[SISTEMA] Usando motor UV para máximo rendimiento."
    # Crear el entorno solo si no existe para evitar prompts
    if [ ! -d "$VENV_DIR" ]; then
        uv venv --python 3.12 --quiet "$VENV_DIR"
    fi
    source "$VENV_DIR/bin/activate"
    uv pip install --quiet -r requirements.txt
    if command -v nvidia-smi &> /dev/null; then
        echo "[SISTEMA] GPU NVIDIA detectada. Instalando soporte CUDA para JAX..."
        uv pip install --quiet "jax[cuda12]"
    fi
else
    echo "[SISTEMA] UV no detectado, usando motor Python estándar."
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
    fi
    source "$VENV_DIR/bin/activate"
    python3 -m pip install --quiet -r requirements.txt
    if command -v nvidia-smi &> /dev/null; then
        echo "[SISTEMA] GPU NVIDIA detectada. Instalando soporte CUDA para JAX..."
        python3 -m pip install --quiet "jax[cuda12]"
    fi
fi

# Ejecutar el script principal
"$VENV_DIR/bin/python" ganabaloto.py

# Mantener la consola abierta al finaliza
echo ""
read -p "Presiona [Enter] para salir..."
