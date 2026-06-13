#!/bin/bash

# GanaBaloto - Actualizador de Resultados
echo "======================================================="
echo "    🎱 GanaBaloto - Actualizador de Resultados 🎱"
echo "======================================================="
echo ""

# Ir al directorio del script
cd "$(dirname "$0")"

# Verificar si el entorno virtual existe
if [ ! -d ".venv" ]; then
    echo "[ERROR] No se detectó el entorno virtual."
    echo "Por favor, ejecuta primero './instalar.sh'."
    exit 1
fi

# Activar entorno e iniciar actualización
echo "[SISTEMA] Activando entorno y buscando sorteos nuevos..."
source .venv/bin/activate
.venv/bin/python actualizar_resultados.py

echo ""
echo "[INFO] Proceso de actualización finalizado."
read -p "Presiona [Enter] para salir..."
