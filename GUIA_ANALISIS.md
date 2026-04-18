# 📘 Guía de Interpretación de Resultados - GanaBaloto

Esta guía explica de forma sencilla cada cálculo del script con ejemplos reales para ayudarte a elegir tus números.

---

## 1. Probabilidad Teórica
*   **Qué es:** La probabilidad matemática pura de ganar antes de mirar cualquier dato.
*   **El Número:** **1 en 15,401,568**.
*   **Ejemplo:** Imagina un estadio lleno con 15 millones de pelotas blancas y solo 1 pelota roja. La probabilidad teórica es la posibilidad de sacar la roja con los ojos vendados al primer intento.

## 2. Prueba de Chi-cuadrado (Bondad de Ajuste) 🧪
*   **Qué es:** Nos dice si el Baloto es "justo" o si hay números que salen más de lo normal por alguna razón física o de tendencia.
*   **Cómo leer el p-value:**
    *   **Si es mayor a 0.05 (Ej: 0.95):** El sorteo es puramente al azar. No hay trucos.
    *   **Si es menor a 0.05 (Ej: 0.002):** **¡Atención!** Hay números que están saliendo mucho más que otros de forma sospechosa. El modelo predictivo es más útil aquí.

## 3. Cadenas de Markov (Transiciones) ⛓️
*   **Qué es:** Analiza si un número "llama" a otro en la secuencia ganadora.
*   **Ejemplo:** El reporte muestra que la transición **43 → 1** tiene una probabilidad del **16%**. Esto significa que cuando el 43 aparece, hay una tendencia histórica a que el 1 también esté presente en ese sorteo o en la secuencia ordenada.

## 4. Números Calientes y Fríos 🔥❄️
*   **Calientes:** Los que más han salido en los últimos 50 juegos.
*   **Fríos:** Los que llevan mucho tiempo sin aparecer.
*   **Consejo:** Lo ideal es una mezcla (ej: 3 calientes y 2 fríos).

## 5. Análisis de Sumas y Paridad ⚖️
*   **Suma:** La suma de tus 5 números debería estar entre **80 y 160**.
*   **Paridad:** Lo ideal es tener **2 pares y 3 impares** (o al revés).

## 6. Gap Analysis (Brecha de Inactividad) ⏳
*   **Qué es:** Cuántos sorteos han pasado desde la última vez que vimos un número.
*   **¿Contra qué se compara?** Contra el **promedio teórico de 8.6 sorteos**.
*   **Interpretación de la Brecha:**
    *   **BAJA (0-5):** Número muy reciente (Caliente).
    *   **NORMAL (6-12):** Está en su ciclo habitual de aparición.
    *   **ALTA (13-25):** **¡Número Maduro!** Estadísticamente está "retrasado" y tiene mayor probabilidad de aparecer pronto para equilibrar su promedio.
    *   **EXTREMA (26+):** Número muy frío. Puede tardar mucho más en despertar.
*   **Ejemplo:** Si el número 1 tiene una brecha de **11**, ya pasó su promedio de 8.6. Es un gran candidato para incluir en tu jugada.

## 7. Puntaje de Frecuencia (Score JAX) ⚡
*   **Qué es:** Una calificación de 0 a 1 para toda tu combinación.
*   **Interpretación:** A mayor Score, más "ganadores" han sido esos números históricamente. Busca combinaciones con Score superior a **0.14**.

---

## 💡 Estrategia Maestra
1.  Busca números con **Brecha (Gap) entre 10 y 20**. Son los que están "por caer".
2.  Elige una sugerencia automática que tenga un **Score alto**.
3.  Asegúrate de que la **Super Balota** sugerida sea una de las "Calientes".

---
*Nota: Este análisis aumenta tus probabilidades estadísticas basándose en datos históricos, pero el azar sigue siendo el factor determinante.*
