#!/bin/bash

# GanaBaloto Web - Lanzador de la aplicación Flask + React
export PATH="$HOME/.local/bin:$PATH"

echo "======================================================="
echo "       🎱 GanaBaloto Web - Iniciando Interfaz 🎱"
echo "======================================================="
echo ""

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
        echo "[ERROR] No se detectó un entorno virtual (.venv o .venv_wsl) válido para este sistema."
        echo "Por favor, crea uno o ejecuta el script de instalación."
        exit 1
    fi
else
    # En Linux estándar, preferir .venv si es válido, luego .venv_wsl si es válido
    if [ -f ".venv/bin/activate" ]; then
        VENV_DIR=".venv"
    elif [ -f ".venv_wsl/bin/activate" ]; then
        VENV_DIR=".venv_wsl"
    else
        echo "[ERROR] No se detectó un entorno virtual (.venv o .venv_wsl) válido para este sistema."
        echo "Por favor, crea uno o ejecuta el script de instalación."
        exit 1
    fi
fi

echo "[SISTEMA] Activando el entorno virtual en $VENV_DIR..."
source "$VENV_DIR/bin/activate"

# Asegurar que flask esté instalado en el entorno virtual
echo "[SISTEMA] Verificando dependencias de Flask..."
pip install --quiet flask

# Compilar frontend de React si no existe la carpeta dist
if [ ! -d "frontend/dist" ]; then
    echo "[SISTEMA] Compilando frontend React..."
    cd frontend
    npm run build
    cd ..
fi

echo "[SISTEMA] Iniciando servidor Flask en http://localhost:5000..."
python app.py
