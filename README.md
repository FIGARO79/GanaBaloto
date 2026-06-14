# 🎱 GanaBaloto - Análisis Estadístico y Predictivo (Baloto & Revancha)

Este proyecto realiza un análisis estadístico avanzado de los sorteos históricos de **Baloto** y **Revancha** (Colombia) para generar combinaciones con mayor probabilidad estadística. Integra modelos de **Cadenas de Markov**, pruebas de aleatoriedad y computación paralela acelerada por hardware (CPU/GPU) mediante **JAX**.

---

## 🛠️ Stack Tecnológico

El proyecto está construido sobre las siguientes tecnologías y librerías de Python:

| Tecnología / Librería | Categoría | Propósito |
| :--- | :--- | :--- |
| **Python 3.10+** | Lenguaje Principal | Base lógica y ejecución del sistema. |
| **JAX & jaxlib** | Computación de Alto Rendimiento | Aceleración matemática en paralelo con soporte para CPU y GPU CUDA 12. |
| **Pandas** | Análisis de Datos | Manipulación, filtrado y modelado de las series históricas de sorteos. |
| **SciPy** | Computación Científica | Pruebas estadísticas avanzadas (Chi-cuadrado, Runs Test, etc.). |
| **JSON** | Almacenamiento de Datos | Lectura y actualización de la base de datos histórica ligera (`baloto.json`). |
| **BeautifulSoup4 & Requests** | Extracción de Datos | Web scraping automatizado para obtener los últimos sorteos oficiales de la web de Baloto. |
| **Tabulate** | Interfaz de Usuario | Formateo e impresión de tablas legibles en la interfaz de línea de comandos. |
| **UV (Astral)** | Gestor de Paquetes | Motor de entorno ultrarrápido escrito en Rust para la instalación óptima de dependencias. |

---

## 📈 Metodología de Análisis Predictivo

GanaBaloto no genera jugadas al azar. Utiliza procesos estadísticos validados para proponer combinaciones con bases históricas coherentes:

1. **Cadenas de Markov de Primer Orden:**
   Analiza la secuencia histórica de sorteos para construir matrices de probabilidad de transición. Esto evalúa la probabilidad de que un número aparezca en función de los números que salieron en los sorteos inmediatamente anteriores.

2. **Test Chi-Cuadrado de Bondad de Ajuste:**
   Determina si la distribución de frecuencias de los números a lo largo del tiempo es verdaderamente uniforme o si presenta anomalías y desviaciones estadísticas significativas.

3. **Prueba de Rachas (Runs Test) de Wald-Wolfowitz:**
   Evalúa la hipótesis de aleatoriedad en la secuencia de sorteos para confirmar si las muestras históricas muestran independencia matemática.

4. **Score JAX (Métrica de Aptitud):**
   Algoritmo vectorizado optimizado con `@jax.jit` que evalúa cada jugada propuesta contra todo el histórico de resultados en microsegundos, calculando la frecuencia ponderada de los números y superbalotas.

---

## 🚀 Instalación y Configuración

El proyecto cuenta con instaladores inteligentes para automatizar la configuración del entorno virtual.

### Requisitos Previos
* Tener instalado **Python 3.10** o superior.
* Tener instalado **git** (opcional).

### 1️⃣ Instalación Automatizada
El instalador crea un entorno virtual (`.venv`), instala el gestor de paquetes **UV** para máximo rendimiento y descarga las dependencias. Adicionalmente, detecta si posee una GPU NVIDIA en el sistema para instalar de forma predeterminada el soporte CUDA necesario para JAX.

* **Linux / macOS:**
  ```bash
  chmod +x instalar.sh
  ./instalar.sh
  ```
* **Windows:**
  Haz doble clic en `instalar.bat` o ejecútalo desde la terminal de comandos:
  ```cmd
  instalar.bat
  ```

---

## 💻 Instrucciones de Uso y Ejecución

Una vez completado el paso de instalación, dispone de dos utilidades principales para su uso diario:

### 1️⃣ Actualizar Base de Datos (Web Scraping)
Descarga en tiempo real los últimos sorteos oficiales de la plataforma de Baloto y los añade al archivo histórico `baloto.json`.

* **Linux / macOS:**
  ```bash
  ./actualizar.sh
  ```
* **Windows:**
  Ejecutar `actualizar.bat`

### 2️⃣ Generar Análisis y Sugerencias de Jugadas
Inicia el motor predictivo interactivo en consola, el cual cargará la base de datos histórica, inicializará el compilador JAX (utilizando CPU o GPU según disponibilidad) y presentará las sugerencias de juego.

* **Linux / macOS:**
  ```bash
  ./ejecutar_baloto.sh
  ```
* **Windows:**
  Ejecutar `ejecutar_baloto.bat`

---

## 📁 Estructura de Directorios

```
GanaBaloto/
├── .venv/                     # Entorno virtual con las librerías aisladas
├── baloto.json                # Base de datos histórica (Estructura: "Baloto" y "Revancha")
├── ganabaloto.py              # Script principal del motor predictivo y generación
├── actualizar_resultados.py   # Script de web scraping para extracción de sorteos
├── GUIA_ANALISIS.md           # Guía de usuario para la interpretación de estadísticas
├── requirements.txt           # Definición de dependencias principales de Python
├── instalar.sh / .bat         # Scripts de instalación e inicialización del entorno
├── actualizar.sh / .bat       # Scripts de ejecución del web scraper
└── ejecutar_baloto.sh / .bat  # Scripts de ejecución del software de análisis
```

---

## 🛡️ Descargo de Responsabilidad

Este software es una herramienta didáctica y científica de análisis de datos históricos. Los juegos de azar como Baloto y Revancha son eventos estadísticamente independientes y aleatorios. El uso de este sistema no garantiza la obtención de premios ni ganancias financieras. Juegue con responsabilidad.
