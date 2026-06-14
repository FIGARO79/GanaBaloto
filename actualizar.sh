#!/bin/bash

# GanaBaloto - Actualizador de Resultados
echo "======================================================="
echo "    🎱 GanaBaloto - Actualizador de Resultados 🎱"
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
    # Si ninguno existe, predecir el nombre esperado según el sistema
    if grep -qEi "(Microsoft|WSL)" /proc/version 2>/dev/null; then
        VENV_DIR=".venv_wsl"
    else
        VENV_DIR=".venv"
    fi
fi

# Verificar si el entorno virtual existe
if [ ! -d "$VENV_DIR" ]; then
    echo "[ERROR] No se detectó el entorno virtual ($VENV_DIR)."
    echo "Por favor, ejecuta primero './instalar.sh'."
    exit 1
fi

# Activar entorno e iniciar actualización
echo "[SISTEMA] Activando entorno y buscando sorteos nuevos..."
source "$VENV_DIR/bin/activate"
"$VENV_DIR/bin/python" actualizar_resultados.py

echo ""
echo "[INFO] Proceso de actualización finalizado."
read -p "Presiona [Enter] para salir..."
