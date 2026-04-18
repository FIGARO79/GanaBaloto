# 🎱 GanaBaloto - Análisis Estadístico y Predictivo (Baloto & Revancha)

Este proyecto realiza un análisis estadístico avanzado de los sorteos históricos de **Baloto** y **Revancha** (Colombia) para generar combinaciones con mayor probabilidad histórica, integrando modelos de **Cadenas de Markov**, pruebas de aleatoriedad y computación acelerada con **JAX**.

## 🚀 Funcionalidades Principales

*   **Análisis Dual Simultáneo:** Procesa y compara datos de las hojas "Baloto" y "Revancha" en el mismo libro de Excel.
*   **Cadenas de Markov:** Analiza las transiciones entre números para identificar secuencias probables basadas en el historial específico de cada sorteo.
*   **Prueba de Chi-cuadrado:** Validación científica de la aleatoriedad de los sorteos (Bondad de Ajuste).
*   **Computación Acelerada:** Uso de **JAX** para el cálculo ultrarrápido de puntajes de frecuencia.
*   **Detección de Entorno:** Compatible con **Jupyter/Colab** (visualización HTML) y **Terminal/Consola** (texto limpio).

## 🛠️ Ejecución Rápida (Automática)

He preparado scripts que configuran el entorno, instalan dependencias y ejecutan el programa automáticamente:

### 🐧 Linux / macOS
Abre una terminal en la carpeta del proyecto y ejecuta:
```bash
./ejecutar_baloto.sh
```

### 🪟 Windows
Simplemente busca el archivo y haz doble clic en él:
`ejecutar_baloto.bat`

---

## 📈 Uso y Documentación

Para ejecutar el análisis y generar combinaciones sugeridas, simplemente corre:

```bash
python3 ganabaloto.py
```

### 📘 Guía de Análisis (¡Muy Importante!)
Si no estás seguro de cómo interpretar los resultados (como el p-value, el Score JAX o el Gap Analysis), he preparado una guía detallada:

👉 **[Leer Guía de Interpretación de Resultados](GUIA_ANALISIS.md)**

En esta guía encontrarás ejemplos prácticos sobre:
*   Cómo saber si un número está "maduro" para salir (Gap Analysis).
*   Qué significa que el sorteo sea "Aleatorio" o tenga "Patrones".
*   Cómo elegir la mejor combinación basada en el Score de frecuencia.

## 📁 Estructura del Proyecto

*   `ganabaloto.py`: Script principal de análisis.
*   `baloto.xlsx`: Base de datos histórica (Hojas: "Baloto" y "Revancha").
*   `ejecutar_baloto.sh / .bat`: Scripts de automatización.
*   `requirements.txt`: Lista de librerías necesarias.
*   `README.md`: Documentación.
*   `GUIA_ANALISIS.md`: Guía detallada para interpretar los resultados.

---
*Nota: Este software es una herramienta de análisis estadístico basada en datos históricos y no garantiza premios en juegos de azar.*
