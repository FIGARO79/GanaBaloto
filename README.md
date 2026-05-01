# 🎱 GanaBaloto - Análisis Estadístico y Predictivo (Baloto & Revancha)

Este proyecto realiza un análisis estadístico avanzado de los sorteos históricos de **Baloto** y **Revancha** (Colombia) para generar combinaciones con mayor probabilidad histórica, integrando modelos de **Cadenas de Markov**, pruebas de aleatoriedad y computación acelerada con **JAX**.

## 🚀 Instalación y Ejecución

He preparado scripts que configuran el entorno, instalan dependencias y ejecutan el programa automáticamente:

### 1️⃣ Instalación Inicial (Solo la primera vez)
Este paso crea el entorno virtual e instala todas las librerías necesarias.

*   **Windows:** Haz doble clic en `instalar.bat`
*   **Linux / macOS:** `./instalar.sh`

### 2️⃣ Ejecución Diaria
Una vez instalado, tienes dos opciones:

*   **Actualizar Resultados (Web):** Si quieres descargar los últimos sorteos antes de analizar.
    *   Windows: `actualizar.bat`
    *   Linux/macOS: `./actualizar.sh`

*   **Ejecutar Análisis:** Abre el programa principal para generar jugadas.
    *   Windows: `ejecutar_baloto.bat`
    *   Linux/macOS: `./ejecutar_baloto.sh`

---

## 📈 Documentación

### 📘 Guía de Análisis (¡Muy Importante!)
Si quieres entender qué significa el p-value, el Score JAX o la estrella (⭐) en tus resultados:

👉 **[Leer Guía de Interpretación de Resultados](GUIA_ANALISIS.md)**

## 📁 Estructura del Proyecto

*   `ganabaloto.py`: Script principal de análisis.
*   `baloto.xlsx`: Base de datos histórica (Hojas: "Baloto" y "Revancha").
*   `ejecutar_baloto.sh / .bat`: Scripts de automatización.
*   `requirements.txt`: Lista de librerías necesarias.
*   `GUIA_ANALISIS.md`: Guía detallada de interpretación.

---
*Nota: Este software es una herramienta de análisis estadístico basada en datos históricos y no garantiza premios en juegos de azar.*
