# 📘 Guía de Interpretación de Resultados - GanaBaloto

Esta guía explica de forma sencilla y práctica cada modelo estadístico, cálculo e insignia del motor **GanaBaloto** para ayudarte a evaluar y seleccionar tus combinaciones de números (Baloto y Revancha).

---

## 📐 1. El Índice Compuesto Global (0 a 100 Puntos)
GanaBaloto evalúa cada combinación mediante un **Índice Compuesto Global** multidimensional de 0 a 100 puntos que integra **6 modelos estadísticos independientes**:

$$\text{Índice Compuesto} = 0.25 \cdot S_{\text{JAX}} + 0.20 \cdot M_{\text{Markov}} + 0.20 \cdot S_{\text{Gauss}} + 0.15 \cdot S_{\text{Bayes}} + 0.10 \cdot S_{\text{Hazard}} + 0.10 \cdot S_{\text{Entropía}}$$

---

## 📊 2. Desglose de los 6 Modelos Predictivos

### 1️⃣ Score JAX (ADN Histórico) – Peso: 25% 🧬
* **Qué es:** Califica la frecuencia e intensidad de aparición acumulada histórica de los 5 números y la Super Balota.
* **Uso:** Mide si la jugada comparte el perfil estadístico de las combinaciones premiadas en el pasado.
* **Norm:** Se normaliza con relación al umbral histórico promedio de ganadores reales (`score_meta`).

### 2️⃣ Cadenas de Markov (Global y Posicional) – Peso: 20% ⛓️
* **Qué es:** Analiza la probabilidad estocástica de que un número o secuencia "llame" a otros en sorteos consecutivos.
* **Cálculo:** Combina la matriz de transición secuencial global con la probabilidad de transición por posición específica ($P_1 \dots P_5, SB$).
* **Ejemplo:** Evalúa con qué frecuencia la aparición del 43 en un sorteo atrae la salida del 1 en el siguiente.

### 3️⃣ Distribución Normal Gaussiana (Suma de Balotas) – Peso: 20% 🔔
* **Qué es:** Evalúa si la suma total de las 5 balotas principales cae dentro de la curva de densidad normal histórica ($\mu \approx 110, \sigma \approx 30$).
* **Zona Dorada:** Premia combinaciones con sumas entre **90 y 130**. Penaliza combinaciones extremas (muy bajas $< 60$ o muy altas $> 160$).

### 4️⃣ Inferencia Bayesiana Continuada (Bayes Score) – Peso: 15% 🎯
* **Qué es:** Aplica probabilidades *a posteriori* con suavizado de Dirichlet para estimar la probabilidad esperada de cada balota.
* **Ventaja:** Evita sesgos por muestras pequeñas y estabiliza la predicción ante variaciones aleatorias.

### 5️⃣ Análisis de Brechas y Hazard Rate (Atraso/Madurez) – Peso: 10% ⏳
* **Qué es:** Mide el número de sorteos consecutivos transcurridos desde la última aparición de cada balota (Gap).
* **Interpretación:**
  * **NORMAL (6–12 sorteos):** Ciclo habitual de rotación.
  * **ALTA / MADURA (13–25 sorteos):** **¡Número Maduro!** Mayor "presión de retorno" basada en la función de Hazard estocástica.

### 6️⃣ Entropía de Shannon (Dispersión y Aleatoriedad) – Peso: 10% 🌀
* **Qué es:** Mide la dispersión espacial y uniformidad de los intervalos entre balotas.
* **Objetivo:** Penaliza jugadas poco aleatorias (secuencias consecutivas como `1, 2, 3` o agrupaciones apretadas) y premia combinaciones con variabilidad natural.

---

## 🧪 3. Prueba de Chi-Cuadrado y Aleatoriedad (Runs Test)
* **Qué es:** Verifica estadísticamente si los resultados del sorteo se comportan como azar puro o si presentan desviaciones estructurales.
* **p-value > 0.05:** Distribución uniforme acorde al azar.
* **p-value < 0.05:** Detección de sesgos o patrones aprovechables por los modelos predictivos.

---

## 🏷️ 4. Sistema de Distintivos e Insignias (🏆 / 🌟 / 🧬)

En los tableros de sugerencias y análisis, las combinaciones destacan con los siguientes distintivos:

| Distintivo | Nombre | Significado e Interpretación |
| :---: | :--- | :--- |
| **🏆** | **Top #1 Recomendación** | Combinación que obtuvo la máxima puntuación en el **Índice Compuesto Global** del sorteo. |
| **🌟** | **Perfil Óptimo (Excelente)** | Jugada con un **Índice Compuesto $\ge 70.0/100$**, superando holgadamente todos los filtros estadísticos. |
| **🧬** | **ADN Ganador JAX** | Indica que el **Score JAX** de la jugada alcanzó o superó el promedio histórico real de los tiquetes ganadores pasados (`score_meta`). |

---

## 🛠️ 5. Herramientas Avanzadas de Análisis y Apuestas

### 🔍 Analizador Manual de Jugadas
Permite ingresar cualquier boleto personalizado (5 balotas + Super Balota) para obtener:
* El **Índice Compuesto Global (0 a 100)** y desglose por cada uno de los 6 modelos.
* Un **Veredicto Cualitativo** instantáneo indicando fortalezas, advertencias de suma/entropía o nivel de madurez.

### ⚙️ Ruedas Combinatorias Reducidas (Wheeling System)
Permite elegir entre 7 y 15 de tus números preferidos para generar un sistema reducido de tiquetes optimizados que garantiza aciertos matemáticos (ej. 4 de 5 o 3 de 5) minimizando el gasto total.

---

## 💡 Estrategia Maestra Sugerida

1. **Prioriza el Perfil Global:** Selecciona jugadas con el **Trofeo 🏆** o distintivo **Perfil Óptimo 🌟 ($\ge 70/100$)**.
2. **Exige el ADN Ganador:** Elige combinaciones con la insignia **ADN 🧬**, asegurando que sus frecuencias compitan con los ganadores históricos.
3. **Verifica la Suma Gaussiana:** Confirma que la suma de las 5 balotas principales esté en la **Zona Dorada (90 a 130)**.
4. **Combina Balotas Calientes y Maduras:** Incluye 1 o 2 números con **Brecha Alta (Gap entre 13 y 25)** junto a números de alta frecuencia reciente.
5. **Optimiza tu Presupuesto:** Usa las **Ruedas Combinatorias** si deseas jugar varios números con respaldo matemático.

---
*Nota: Este sistema aplica analítica avanzada e inteligencia predictiva sobre datos históricos para maximizar la eficiencia estadística de tus tiquetes, pero el azar sigue siendo un componente fundamental.*
