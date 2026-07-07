#!/bin/bash

# GanaBaloto - Instalador del Entorno
echo "======================================================="
echo "       🎱 GanaBaloto - Instalador del Entorno 🎱"
echo "======================================================="
echo ""

# Ir al directorio del script
cd "$(dirname "$0")"

# Determinar el nombre del entorno virtual a utilizar según el sistema
if grep -qEi "(Microsoft|WSL)" /proc/version 2>/dev/null; then
    VENV_DIR=".venv_wsl"
else
    VENV_DIR=".venv"
fi

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
echo "[3/4] Creando entorno virtual ($VENV_DIR)..."
if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
    echo "[INFO] El entorno virtual ya existe y es válido."
else
    if [ -d "$VENV_DIR" ]; then
        echo "[WARNING] El directorio $VENV_DIR existe pero no es un entorno virtual válido para Linux/WSL. Recreándolo..."
        rm -rf "$VENV_DIR"
    fi
    if [ $USE_UV -eq 1 ]; then
        uv venv --python 3.12 "$VENV_DIR"
    else
        $PYTHON_CMD -m venv "$VENV_DIR"
    fi
    echo "[OK] Entorno virtual creado."
fi

# 4. Instalar Dependencias
echo ""
echo "[4/4] Instalando librerías..."
source "$VENV_DIR/bin/activate"

if [ $USE_UV -eq 1 ]; then
    uv pip install -r requirements.txt
    if command -v nvidia-smi &> /dev/null; then
        echo "[INFO] GPU NVIDIA detectada. Instalando soporte CUDA para JAX..."
        uv pip install "jax[cuda12]"
    fi
else
    $PYTHON_CMD -m pip install --upgrade pip
    $PYTHON_CMD -m pip install -r requirements.txt
    if command -v nvidia-smi &> /dev/null; then
        echo "[INFO] GPU NVIDIA detectada. Instalando soporte CUDA para JAX..."
        $PYTHON_CMD -m pip install "jax[cuda12]"
    fi
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
    "$VENV_DIR/bin/python" actualizar_resultados.py
fi

echo ""
echo "Instalación finalizada."
