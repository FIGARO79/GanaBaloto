#!/bin/bash

# GanaBaloto Web - Lanzador de la aplicación Streamlit
export PATH="$HOME/.local/bin:$PATH"

echo "======================================================="
echo "       🎱 GanaBaloto Web - Iniciando Interfaz 🎱"
echo "======================================================="
echo ""

# Ir al directorio del script
cd "$(dirname "$0")"

# Determinar el entorno virtual a utilizar
if [ -d ".venv" ]; then
    VENV_DIR=".venv"
elif [ -d ".venv_wsl" ]; then
    VENV_DIR=".venv_wsl"
else
    echo "[ERROR] No se detectó un entorno virtual (.venv o .venv_wsl)."
    echo "Por favor, crea uno o ejecuta el script de instalación."
    exit 1
fi

echo "[SISTEMA] Activando el entorno virtual en $VENV_DIR..."
source "$VENV_DIR/bin/activate"

echo "[SISTEMA] Lanzando Streamlit..."
streamlit run app.py
