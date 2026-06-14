#!/bin/bash

# GanaBaloto - Script de ejecución optimizada con UV
export PATH="$HOME/.local/bin:$PATH"

echo "Iniciando GanaBaloto con entorno optimizado..."

# Ir al directorio del script
cd "$(dirname "$0")"

# Determinar el entorno virtual a utiliza
if [ -d ".venv" ]; then
    VENV_DIR=".venv"
elif [ -d ".venv_wsl" ]; then
    VENV_DIR=".venv_wsl"
else
    # Si ninguno existe, predecir el nombre esperado según el sistema
    if grep -qEi "(Microsoft|WSL)" /proc/version 2>/dev/null; then
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
