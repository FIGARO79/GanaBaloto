# 🎱 GanaBaloto - Análisis Estadístico y Predictivo (Baloto & Revancha)

Este proyecto realiza un análisis estadístico avanzado de los sorteos históricos de **Baloto** y **Revancha** (Colombia) para generar combinaciones con mayor probabilidad histórica, integrando modelos de **Cadenas de Markov**, pruebas de aleatoriedad y computación acelerada con **JAX**.

## 🚀 Funcionalidades Principales

*   **Análisis Dual Simultáneo:** Procesa y compara datos de las hojas "Baloto" y "Revancha" en el mismo libro de Excel.
*   **ADN de Ganadores (5+1):** Analiza las combinaciones que ya ganaron el premio mayor para extraer su "perfil estadístico" (Score y Markov).
*   **Cadenas de Markov:** Analiza las transiciones entre números para identificar secuencias probables basadas en el historial específico de cada sorteo.
*   **Prueba de Chi-cuadrado:** Validación científica de la aleatoriedad de los sorteos (Bondad de Ajuste).
*   **Indicador ADN Ganador (⭐):** Marca con una estrella las sugerencias que superan el Score promedio de los ganadores históricos.
*   **Detección de Entorno:** Compatible con **Jupyter/Colab** (visualización HTML) y **Terminal/Consola** (texto limpio).

## 🛠️ Ejecución Rápida (Automática)

He preparado scripts que configuran el entorno, instalan dependencias y ejecutan el programa automáticamente:

### 🐧 Linux / macOS
```bash
./ejecutar_baloto.sh
```

### 🪟 Windows
Haz doble clic en: `ejecutar_baloto.bat`

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
