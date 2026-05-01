#!/bin/bash

# GanaBaloto - Instalador del Entorno
echo "======================================================="
echo "       🎱 GanaBaloto - Instalador del Entorno 🎱"
echo "======================================================="
echo ""

# 1. Verificar Python
echo "[1/4] Verificando instalación de Python..."
if command -v python3 &> /dev/null
then
    echo "[OK] Python 3 detectado."
    PYTHON_CMD=python3
elif command -v python &> /dev/null
then
    echo "[OK] Python detectado."
    PYTHON_CMD=python
else
    echo "[ERROR] Python no detectado. Por favor instala Python 3.10+."
    exit 1
fi

# 2. Instalar UV (Opcional)
echo ""
echo "[2/4] Configurando motor de paquetes (UV)..."
export PATH="$HOME/.local/bin:$PATH"

if command -v uv &> /dev/null
then
    echo "[OK] UV ya está instalado."
    USE_UV=1
else
    echo "[INFO] UV no detectado. Intentando instalación rápida..."
    curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null
    
    if command -v uv &> /dev/null
    then
        echo "[OK] UV instalado correctamente."
        USE_UV=1
    else
        echo "[INFO] No se pudo instalar UV. Se usará PIP (más lento)."
        USE_UV=0
    fi
fi

# 3. Crear Entorno Virtual
echo ""
echo "[3/4] Creando entorno virtual (.venv)..."
if [ -d ".venv" ]; then
    echo "[INFO] El entorno virtual ya existe."
else
    if [ $USE_UV -eq 1 ]; then
        uv venv --python 3.12 .venv
    else
        $PYTHON_CMD -m venv .venv
    fi
    echo "[OK] Entorno virtual creado."
fi

# 4. Instalar Dependencias
echo ""
echo "[4/4] Instalando librerías..."
source .venv/bin/activate

if [ $USE_UV -eq 1 ]; then
    uv pip install -r requirements.txt
else
    $PYTHON_CMD -m pip install --upgrade pip
    $PYTHON_CMD -m pip install -r requirements.txt
fi
echo "[OK] Dependencias instaladas."

echo ""
echo "======================================================="
echo "   ✅ INSTALACIÓN COMPLETADA CON ÉXITO"
echo "======================================================="
echo ""
echo "Ahora puedes ejecutar el programa usando:"
echo "   ./ejecutar_baloto.sh"
echo ""

read -p "¿Deseas intentar actualizar los resultados de Baloto ahora? (s/n): " UPDATE
if [[ "$UPDATE" =~ ^[Ss]$ ]]; then
    echo ""
    echo "Actualizando resultados..."
    python3 actualizar_resultados.py
fi

echo ""
echo "Instalación finalizada."
