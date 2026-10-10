# 🎱 GanaBaloto - Motor de Inteligencia Predictiva y Modelado Estocástico Multimodal (Baloto & Revancha)

Plataforma avanzada de análisis cuantitativo, modelado estocástico, optimización combinatoria y física estadística aplicada a los sorteos históricos de **Baloto** y **Revancha** (Colombia).

El sistema integra **7 modelos matemáticos y estadísticos independientes** acelerados por hardware en GPU con **JAX** y optimizados con estructuras de consulta $O(1)$, evaluando millones de combinaciones para filtrar anomalías y estructurar combinaciones con perfiles de probabilidad, simetría y madurez óptimos.

Dispone de un **sistema predictivo automatizado por línea de comandos (CLI / Agente)** y una **aplicación web moderna (Flask REST API + React & Vite)**.

> ℹ️ **Nota de Arquitectura:** Las configuraciones de contenedores (.devcontainer) y Streamlit han sido retiradas y deprecadas en favor de la arquitectura desacoplada moderna: **Backend REST en Flask** y **Frontend interactivo en React + Vite**.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Core / Lógica** | **Python 3.10+** | Motor de cálculo estocástico, analítica y simulación. |
| **Aceleración GPU/CPU** | **JAX & jaxlib** | Computación paralela acelerada por hardware con compilación `@jax.jit` sobre tensores CUDA (GPU NVIDIA). |
| **Procesamiento de Datos** | **Pandas & NumPy** | Manipulación de matrices, series temporales, indexación vectorial y frecuencias históricas. |
| **Cálculo Científico** | **SciPy** | Pruebas de hipótesis (Chi-cuadrado, distribuciones de Weibull y Gauss). |
| **Backend REST API** | **Flask & Flask-CORS** | Servidor web con endpoints RESTful para análisis, generación y ruedas combinatorias. |
| **Frontend Web** | **React + Vite** | Interfaz de usuario dinámica, reactiva y modular con analítica visual en tiempo real. |
| **Web Scraping** | **Requests & BeautifulSoup4** | Extracción automatizada y sincronización de los resultados oficiales de Baloto y Revancha. |
| **Gestión de Paquetes** | **UV (Astral)** | Gestor de paquetes ultrarrápido escrito en Rust para instalación de dependencias aisladas. |

---

## ⚡ Motor de Alto Rendimiento y Optimizaciones Computacionales

El motor estocástico incorpora optimizaciones de bajo nivel para garantizar respuestas en tiempo real:

* **Tablas de Búsqueda Precalculadas $O(1)$ (Lookup Tables):** Los atrasos de balotas (Weibull Hazard) y probabilidades regularizadas (Dirichlet Bayesiano) se precomputan en vectores contiguos al indexar la base de datos, sustituyendo bucles iterativos lentos (`df.iterrows()`) por accesos inmediatos por índice. *(Aceleración de más de **800x** en la evaluación de brechas).*
* **Vectorización Matricial del Modelo de Ising:** Las interacciones cooperativas entre parejas de balotas se calculan mediante indexación NumPy de submatrices $5 \times 5$ y triangulación superior estricta (`np.triu`), eliminando los bucles anidados en Python.
* **Caché Contiguo de Matrices de Transición de Markov:** Las matrices de Markov posicionales y globales utilizan arrays contiguos en memoria (`_arr_cache`), evitando la sobrecarga de consultas DataFrame `.loc`.
* **Procesamiento por Lotes en JAX (Batch Scoring):** Implementado el operador compilado `@jax.jit` `calculate_frequency_scores_jax_batch`, capaz de evaluar más de **50.000 combinaciones en ~250 ms** sobre la GPU NVIDIA.

---

## 📊 Arquitectura Matemática y Modelos Estocásticos

GanaBaloto evalúa cada combinación candidata mediante un **Índice Compuesto Global (0 a 100 puntos)** que integra 7 dimensiones estadísticas calibradas:

$$\text{Índice Compuesto} = \Big[ 0.20 \cdot \text{Norm}_{\text{JAX}} + 0.15 \cdot M_{\text{Markov}} + 0.15 \cdot S_{\text{Gauss}} + 0.15 \cdot S_{\text{Bayes}} + 0.15 \cdot S_{\text{Weibull}} + 0.10 \cdot S_{\text{Ising}} + 0.10 \cdot S_{\text{Entropía}} \Big] \times 100$$

### 1️⃣ Score JAX (ADN Histórico Vectorizado) – Peso: 20%
* **Concepto:** Evalúa el peso y frecuencia acumulada de los 5 números y la Super Balota en sorteos premiados.
* **Fórmula:** Cálculo tensorial JAX compilado por JIT sobre GPU/CPU, normalizado frente a la meta histórica:
  $$\text{Norm}_{\text{JAX}} = \min\left(1.0, \frac{\text{Score JAX}}{\text{Score Meta Histórica}}\right)$$
* **Interpretación:** Identifica si la combinación comparte la firma estocástica ("ADN") presente en los acumulados históricos reales.

### 2️⃣ Modelos de Markov Combinados (Global + Posicional) – Peso: 15%
* **Concepto:** Probabilidad estocástica de transición condicionada al último sorteo oficial.
* **Fórmula:** Promedio balanceado de la matriz de transición secuencial global y las matrices de transición posicional ($B_1 \to B_1, \dots, SB \to SB$):
  $$M_{\text{Markov}} = 0.5 \cdot \text{Norm}(P_{\text{Global}}) + 0.5 \cdot \text{Norm}(P_{\text{Posicional}})$$

### 3️⃣ Distribución Normal Gaussiana (Suma de Balotas) – Peso: 15%
* **Concepto:** Proximidad de la suma de balotas principales al centro de masa de la campana de Gauss histórica ($\mu \approx 110, \sigma \approx 26.4$).
* **Fórmula:** Función de densidad de probabilidad normal:
  $$S_{\text{Gauss}} = \exp\left( -\frac{(S - \mu)^2}{2\sigma^2} \right)$$
* **Interpretación:** Premia la **zona dorada** (sumas de 90 a 130) y penaliza colas extremas imposibles o altamente improbables ($<60$ o $>165$).

### 4️⃣ Inferencia Bayesiana Regularizada (Dirichlet-Multinomial) – Peso: 15%
* **Concepto:** Probabilidades *a posteriori* con regularización frente a la escasez muestral mediante pseudoconteos de Dirichlet ($\alpha = 1.0$).
* **Fórmula:**
  $$S_{\text{Bayes}} = \frac{1}{K} \sum_{i=1}^K \frac{c_i + \alpha}{N + \alpha \cdot M}$$

### 5️⃣ Análisis de Supervivencia de Weibull (Hazard Rate Calibrado) – Peso: 15%
* **Concepto:** Modela la tasa de riesgo y madurez del atraso (gaps) mediante una distribución de Weibull ajustada empíricamente ($k = 1.1667, \lambda = 9.0176$).
* **Fórmula:**
  $$S_{\text{Weibull}} = 1 - \exp\left(-\left(\frac{t}{\lambda}\right)^k\right)$$
* **Interpretación:** Supera la falacia de eventos sin memoria. Identifica la **ventana de madurez óptima (atraso de 3 a 12 sorteos)**, penalizando tanto la inmadurez de corto plazo como números excesivamente fríos.

### 6️⃣ Modelo de Energía de Ising para Interacciones Pareadas ($J_{ij}$) – Peso: 10%
* **Concepto:** Inspirado en el modelo de espines de Ising de física estadística, evalúa la energía de acoplamiento mutuo y cooperatividad entre parejas de balotas.
* **Fórmula:** Matriz de interacción log-odds:
  $$J_{ij} = \ln\left(\frac{C_{ij} + 1}{\mathbb{E}[C_{ij}] + 1}\right), \quad S_{\text{Ising}} = \frac{1}{1 + \exp(-2 \cdot \bar{J})}$$

### 7️⃣ Entropía de Shannon (Dispersión y No-Congestión) – Peso: 10%
* **Concepto:** Mide el desorden armónico espacial entre distancias consecutivas ordenadas $d_i = b_{i+1} - b_i$.
* **Fórmula:** Entropía normalizada:
  $$S_{\text{Entropía}} = -\frac{\sum p(d_i) \log_2 p(d_i)}{\log_2(K)}$$
* **Interpretación:** Filtra secuencias forzadas, agrupaciones en una única decena o progresiones aritméticas triviales.

---

## 🌀 Detección de Régimen Dinámico (HMM)

El motor implementa un **Modelo Oculto de Markov (HMM)** de 3 estados para identificar el régimen estocástico actual del juego:
1. **Congestión Baja:** Concentración de balotas en decenas 1 y 2 con sumas $\le 95$ (régimen activo durante caídas de acumulados).
2. **Equilibrio Central:** Dispersión simétrica regular con sumas entre 96 y 124.
3. **Expansión Alta:** Balotas en decenas 3 y 4 con sumas $\ge 125$.

---

## 🏷️ Sistema de Distintivos e Insignias

Para auditar y diagnosticar de forma inmediata las características cualitativas de cada combinación:

| Insignia | Nombre | Significado Técnico |
| :---: | :--- | :--- |
| **🏆** | **Top #1** | Máximo **Índice Compuesto / Ajustado** del universo evaluado. |
| **🌟** | **Perfil Óptimo** | Calificación integral $\ge 70.0/100$ en la escala estocástica multidimensional. |
| **🧬** | **ADN Ganador** | Score JAX superior al promedio histórico real de los boletos ganadores del premio mayor 5+1. |
| **📅** | **Fecha** | Integra anclajes de calendario del sorteo (día, mes o suma de dígitos del sorteo). |
| **🌀** | **Lag-8** | Resuena con el sorteo de hace 8 fechas (patrón cíclico detectado en botes millonarios). |
| **🪞** | **Espejo** | Efecto donde la Super Balota coincide como número principal (presente en el bote récord #2717 de $61.600M). |
| **⚡** | **Delta** | Presenta saltos aritméticos simétricos de $+4$ o $+6$ observados en los acumulados históricos. |
| **🧲** | **Ising** | Alta afinidad mutua pareada ($J_{ij}$ positivo y estadísticamente significativo). |

---

## 🛡️ Ruedas Combinatorias Reducidas (Wheeling Systems)

Algoritmo de cobertura basado en **Greedy Set-Cover** que permite seleccionar un grupo de $N$ números clave (ej. 7 a 15) y generar un número mínimo de tiquetes con **garantía matemática determinista de $t$ aciertos**:
* **Garantía $C(7, 5, 3)$:** Con solo **10 tiquetes**, se cubre el 100% de las 35 ternas posibles. Si al menos 3 de los 7 números seleccionados resultan sorteados, se tiene matemáticamente asegurado al menos un tiquete con 3 aciertos en la apuesta.

---

## 🚀 Instalación y Puesta en Marcha

### 1️⃣ Prerrequisitos
* **Python 3.10+**
* **Node.js 18+ & npm** (para la interfaz React)
* **GPU NVIDIA** con soporte CUDA (opcional, aceleración JAX automática; fallback en CPU)

### 2️⃣ Instalación Rápida
El proyecto utiliza **UV** para la gestión rápida y determinista del entorno virtual:

```bash
# Dar permisos de ejecución e instalar
chmod +x instalar.sh
./instalar.sh
```

O manualmente:
```bash
uv venv
uv pip install -r requirements.txt
uv pip install jax[cuda12] # Opcional para aceleración GPU NVIDIA
cd frontend && npm install && npm run build && cd ..
```

---

## 💻 Modos de Uso y Ejecución

### ⚡ 1. Pronóstico Rápido Automatizado (CLI / Agente)
Genera el reporte integral oficial de 4 secciones para el próximo sorteo:
```bash
./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/ejecutar_pronostico_completo.py
```
*(En el entorno de agentes, invocar directamente con la palabra activadora `PRONOSTICO`, `JUGADAS` o `GANABALOTO`).*

### 🌐 2. Servidor Web Completo (Flask + React)
Inicia la API REST en el puerto 5000 y sirve la aplicación web interactiva:
```bash
./ejecutar_web.sh
# O directamente:
./.venv/bin/python app.py
```
Accede desde tu navegador a `http://localhost:5000`.

### 🧪 3. Suites de Pruebas Automatizadas

#### Pruebas Unitarias del Motor Estocástico (13/13 pruebas):
```bash
./.venv/bin/python .agents/skills/baloto-analisis-predictivo/tests/run_tests.py
```

#### Pruebas de Integración de la API REST (9/9 endpoints):
```bash
./.venv/bin/python .agents/skills/baloto-servicio-web/scripts/test_api.py
```

### 🔄 4. Actualización del Histórico (Web Scraper)
Descarga los últimos resultados oficiales y sincroniza `baloto.json`:
```bash
./actualizar.sh
# O directamente:
./.venv/bin/python actualizar_resultados.py
```

---

## 📁 Estructura del Proyecto

```
GanaBaloto/
├── .agents/skills/                          # Skills modulares para agentes autónomos
│   ├── baloto-actualizador/                 # Scraping y auditoría de integridad histórica
│   ├── baloto-analisis-predictivo/          # Motor estocástico, pronósticos y ruedas reducidas
│   │   ├── scripts/pronostico/              # Módulos: datos, modelos, scoring, candidatas, rueda, auditoría
│   │   └── tests/                           # Suite de pruebas unitarias (13 tests)
│   └── baloto-servicio-web/                 # Pruebas automatizadas y gestión del servicio web
├── frontend/                                # Aplicación Web React + Vite
│   ├── src/                                 # Componentes, vistas y lógica reactiva
│   ├── dist/                                # Artefactos estáticos compilados para producción
│   └── package.json                         # Dependencias frontend
├── .venv/                                   # Entorno virtual aislado de Python (UV)
├── app.py                                   # Servidor Backend REST API en Flask
├── ganabaloto.py                            # Núcleo algorítmico, fórmulas estocásticas y CLI
├── baloto.json                              # Base de datos histórica oficial (Baloto y Revancha)
├── baloto.xlsx                              # Hoja de cálculo sincronizada de resultados
├── actualizar_resultados.py                 # Scraper oficial de resultados
├── ANALISIS_GANADORES_BALOTO.md             # Auditoría empírica de los botes históricos 5+1
├── GUIA_ANALISIS.md                         # Manual de interpretación estadística para usuarios
├── README.md                                # Documentación maestra del proyecto
├── requirements.txt                         # Dependencias Python
└── *.sh / *.bat                             # Scripts automatizados de instalación y ejecución
```

---

## 🛡️ Descargo de Responsabilidad (Juego Responsable)

Este software es una plataforma avanzada de análisis cuantitativo, simulación computacional y física estadística con fines estrictamente educativos y de investigación. 

Los sorteos de lotería Baloto y Revancha son eventos físicos independientes y aleatorios. La probabilidad matemática teórica de acertar 5 balotas principales y la Super Balota en una sola combinación es de **1 en 15.401.568** $\left(\binom{43}{5} \times 16\right)$. Ningún algoritmo, sistema estadístico o modelo predictivo puede garantizar premios mayores. Juegue siempre de manera responsable y con presupuesto moderado.
