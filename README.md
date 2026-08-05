# 🎱 GanaBaloto - Análisis Estadístico y Predictivo Multimodelo (Baloto & Revancha)

Este proyecto es una plataforma avanzada de análisis cuantitativo, modelado estocástico y simulación predictiva para los sorteos históricos de **Baloto** y **Revancha** (Colombia). 

Combina **6 modelos estadísticos y estocásticos independientes** (Cadenas de Markov, Inferencia Bayesiana, Análisis de Hazard/Brechas, Entropía de Selección, Distribución Gaussiana y Computación Vectorizada JAX) para evaluar y proponer combinaciones con perfiles de probabilidad óptimos.

Dispone tanto de un **sistema interactivo por línea de comandos (CLI)** como de una **aplicación web moderna (Flask + React)**.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Core / Lógica** | **Python 3.10+** | Motor de cálculo, procesamiento estadístico y simulación. |
| **Aceleración GPU/CPU** | **JAX & jaxlib** | Computación paralela acelerada por hardware con compilación `@jax.jit` para evaluar millones de combinaciones. |
| **Procesamiento de Datos** | **Pandas & NumPy** | Manipulación de matrices, frecuencias históricas y series de tiempo. |
| **Cálculo Científico** | **SciPy** | Pruebas de hipótesis (Chi-cuadrado, Runs Test de aleatoriedad, distribuciones). |
| **Backend REST API** | **Flask & Flask-CORS** | Servidor web liviano para exponer los servicios de análisis y generación. |
| **Frontend Web** | **React + Vite** | Interfaz web interactiva, moderna y dinámica con tableros y analítica en tiempo real. |
| **Web Scraping** | **Requests & BeautifulSoup4** | Extracción automatizada de los últimos sorteos oficiales de Baloto. |
| **Entorno & Paquetes** | **UV (Astral)** | Gestor de paquetes ultrarrápido escrito en Rust para instalación de dependencias aisladas. |

---

## 📊 Explicación Detallada de los Cálculos y Modelos

GanaBaloto integra un **Índice Compuesto Global (0 a 100 puntos)** que evalúa cada jugada combinando 6 dimensiones estadísticas:

$$\text{Índice Compuesto} = 0.25 \cdot S_{\text{JAX}} + 0.20 \cdot M_{\text{Markov}} + 0.20 \cdot S_{\text{Gauss}} + 0.15 \cdot S_{\text{Bayes}} + 0.10 \cdot S_{\text{Hazard}} + 0.10 \cdot S_{\text{Entropía}}$$

### 1️⃣ Score JAX (ADN Histórico) – Peso: 25%
* **Concepto:** Evalúa el peso y frecuencia acumulada histórica de los 5 números y la Super Balota.
* **Fórmula / Cálculo:** Mide la suma ponderada de apariciones en sorteos pasados, optimizada en JAX. Se normaliza dividiendo entre un umbral de referencia:
  $$\text{Norm}_{\text{JAX}} = \min\left(1.0, \frac{\text{Score JAX}}{0.20}\right)$$
* **Interpretación:** Permite identificar si los números de la combinación pertenecen al núcleo de alta presencia histórica en sorteos premiados.

### 2️⃣ Modelos de Markov Combinados (Global + Posicional) – Peso: 20%
* **Concepto:** Evalúa la probabilidad estocástica de transición entre sorteos consecutivos.
* **Fórmula / Cálculo:** Promedia la probabilidad de transición secuencial global y la matriz de probabilidad de transición posicional ($P_1, P_2, P_3, P_4, P_5, SB$):
  $$M_{\text{Markov}} = 0.5 \cdot \text{Norm}(P_{\text{Markov Global}}) + 0.5 \cdot \text{Norm}(P_{\text{Markov Posicional}})$$
* **Interpretación:** Captura patrones de secuencia dependientes del sorteo inmediatamente anterior.

### 3️⃣ Distribución Normal Gaussiana (Suma de Balotas) – Peso: 20%
* **Concepto:** Mide qué tan cerca se encuentra la suma total de las 5 balotas principales del centro de la campana de Gauss histórica.
* **Fórmula / Cálculo:** Evalúa la suma $S = \sum_{i=1}^5 b_i$ usando la función de densidad de probabilidad gaussiana ($\mu \approx 110, \sigma \approx 30$):
  $$S_{\text{Gauss}} = \exp\left( -\frac{(S - \mu)^2}{2\sigma^2} \right)$$
* **Interpretación:** Penaliza combinaciones con sumas extremas (muy bajas $< 60$ o muy altas $> 160$) y premia la "zona dorada" (~90 a 130).

### 4️⃣ Inferencia Bayesiana Continuada (Bayes Score) – Peso: 15%
* **Concepto:** Aplica probabilidades *a posteriori* utilizando una distribución a priori de Dirichlet / Suavizado Bayesiano.
* **Fórmula / Cálculo:** Pondera la probabilidad esperada de cada balota dado el histórico total de sorteos:
  $$S_{\text{Bayes}} = \frac{1}{K} \sum_{i=1}^K \frac{c_i + \alpha}{N + \alpha \cdot M}$$
  donde $c_i$ es el conteo de la balota, $N$ el total de sorteos, y $\alpha$ el parámetro de suavizado.
* **Interpretación:** Evita sesgos por muestras pequeñas y proporciona una estimación estable de probabilidad futura.

### 5️⃣ Análisis de Brechas y Hazard Rate (Atraso/Madurez) – Peso: 10%
* **Concepto:** Evalúa el número de sorteos transcurridos desde la última aparición de cada balota (Gap o Brecha).
* **Fórmula / Cálculo:** Basado en la función de Hazard estocástica para medir la "presión de retorno" de balotas frías o maduras:
  $$S_{\text{Hazard}} = 1 - (1 - \lambda)^{g}$$
  donde $g$ es la brecha actual y $\lambda$ es la tasa constante de retorno esperada.
* **Interpretación:** Identifica números con un atraso significativo que estadísticamente están en ciclo de retorno.

### 6️⃣ Entropía de la Combinación (Dispersión y Aleatoriedad) – Peso: 10%
* **Concepto:** Mide la dispersión espacial y uniformidad de los números para garantizar variabilidad natural.
* **Fórmula / Cálculo:** Evalúa los intervalos entre números ordenados $d_i = b_{i+1} - b_i$ calculando la entropía normalizada de Shannon:
  $$S_{\text{Entropía}} = -\sum p_i \log_2(p_i) / \log_2(K)$$
* **Interpretación:** Penaliza combinaciones no aleatorias (como secuencias consecutivas `1, 2, 3` o agrupamientos apretados).

---

## 🏷️ Sistema de Distintivos e Insignias

Para facilitar la interpretación visual en las sugerencias multimodelo:

| Distintivo | Nombre | Significado |
| :---: | :--- | :--- |
| **🏆** | **Top #1 Recomendación** | Combinación con el **Índice Compuesto Global** más alto del ranking. |
| **🌟** | **Perfil Óptimo (Excelente)** | Combinación con **Índice Compuesto $\ge 70.0/100$**, que supera holgadamente todos los filtros estadísticos. |
| **🧬** | **ADN Ganador JAX** | Indica que el **Score JAX** de la jugada superó el promedio histórico real de los ganadores (`score_meta`). |

---

## ⚙️ Funcionalidades Adicionales

1. **⚙️ Ruedas Combinatorias Reducidas (Wheeling System):**
   Permite seleccionar entre 7 y 15 balotas favoritas y generar un conjunto reducido de tiquetes que garantiza matemáticamente condiciones de acierto (ej. 4 de 5 o 3 de 5) optimizando el presupuesto de juego.

2. **🔍 Analizador Manual de Jugadas:**
   Permite al usuario ingresar cualquier boleto de 5 números + Super Balota para recibir una auditoría instantánea con su *Índice Compuesto* y un veredicto cualitativo detallado punto por punto.

3. **📊 Pruebas de Aleatoriedad y Chi-Cuadrado:**
   Genera reportes de significancia estadística para confirmar si la serie histórica actual del Baloto o Revancha cumple con las propiedades de aleatoriedad esperadas.

---

## 🚀 Instalación y Configuración

### 1️⃣ Instalación Automatizada
El instalador configura un entorno virtual `.venv`, instala **UV** para velocidad y descarga dependencias. Además, detecta automáticamente GPUs NVIDIA para habilitar aceleración CUDA en JAX.

* **Linux / macOS:**
  ```bash
  chmod +x instalar.sh
  ./instalar.sh
  ```
* **Windows:**
  ```cmd
  instalar.bat
  ```

---

## 💻 Ejecución

### 1️⃣ Actualizar Resultados (Web Scraper)
```bash
./actualizar.sh       # Linux / macOS
actualizar.bat        # Windows
```

### 2️⃣ Ejecutar Motor en Consola (CLI)
```bash
./ejecutar_baloto.sh  # Linux / macOS
ejecutar_baloto.bat   # Windows
```

### 3️⃣ Ejecutar Aplicación Web (Flask + React)
```bash
./ejecutar_web.sh     # Linux / macOS
```
O accede manualmente iniciando `app.py` en backend y `npm run dev` en `frontend/`.

---

## 📁 Estructura de Directorios

```
GanaBaloto/
├── .venv/                     # Entorno virtual con dependencias aisladas
├── baloto.json                # Base de datos histórica (Baloto y Revancha)
├── ganabaloto.py              # Motor predictivo principal y CLI interactivo
├── app.py                     # Backend REST API en Flask
├── frontend/                  # Aplicación Frontend React + Vite
├── actualizar_resultados.py   # Script de web scraping oficial
├── GUIA_ANALISIS.md           # Guía de usuario e interpretación
├── README.md                  # Documentación principal del proyecto
├── requirements.txt           # Dependencias de Python
└── *.sh / *.bat               # Lanzadores y utilidades de ejecución
```

---

## 🛡️ Descargo de Responsabilidad

Este software es una herramienta de análisis cuantitativo y exploración de datos históricos con fines educativos y de investigación. Los sorteos de Baloto y Revancha son eventos estadísticamente aleatorios e independientes. El uso de este software no garantiza premios ni beneficios financieros. Juegue con responsabilidad.
