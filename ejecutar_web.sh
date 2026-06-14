#!/bin/bash

# GanaBaloto Web - Lanzador de la aplicación Flask + React
export PATH="$HOME/.local/bin:$PATH"

echo "======================================================="
echo "       🎱 GanaBaloto Web - Iniciando Interfaz 🎱"
echo "======================================================="
echo ""

# Ir al directorio del script
cd "$(dirname "$0")"

# Determinar el entorno virtual a utilizar
if [ -d ".venv_wsl" ]; then
    VENV_DIR=".venv_wsl"
elif [ -d ".venv" ]; then
    VENV_DIR=".venv"
else
    echo "[ERROR] No se detectó un entorno virtual (.venv o .venv_wsl)."
    echo "Por favor, crea uno o ejecuta el script de instalación."
    exit 1
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
