# 📘 Guía de Interpretación de Resultados - GanaBaloto

Esta guía explica de forma sencilla cada cálculo del script con ejemplos reales para ayudarte a elegir tus números.

---

## 1. Probabilidad Teórica
*   **Qué es:** La probabilidad matemática pura de ganar antes de mirar cualquier dato.
*   **El Número:** **1 en 15,401,568**.

## 2. Prueba de Chi-cuadrado (Bondad de Ajuste) 🧪
*   **Qué es:** Nos dice si el sorteo es puramente al azar o si hay patrones.
*   **p-value > 0.05:** Azar puro.
*   **p-value < 0.05:** Patrones detectados (el modelo predictivo es muy útil aquí).

## 3. ADN de Ganadores (Histórico 5+1) 🏆
*   **Qué es:** El script analiza las combinaciones que **ya ganaron** en la vida real.
*   **Uso:** Calcula el Score JAX promedio de todos los ganadores históricos. 
*   **Interpretación:** Si los ganadores históricos tienen un Score de **0.1450**, cualquier combinación nueva que alcance esa cifra tiene el mismo "peso estadístico" que un tiquete ganador del pasado.

## 4. Cadenas de Markov (Transiciones) ⛓️
*   **Qué es:** Analiza si un número "llama" a otro.
*   **Ejemplo:** Si después del 43 suele salir el 1, esa transición tiene una probabilidad alta (ej. 16%).

## 5. Gap Analysis (Brecha de Inactividad) ⏳
*   **¿Contra qué se compara?** Contra el promedio teórico de **8.6 sorteos**.
*   **Interpretación:**
    *   **NORMAL (6-12):** Ciclo habitual.
    *   **ALTA (13-25):** **¡Número Maduro!** Estadísticamente está "retrasado" y tiene mayor probabilidad de aparecer pronto.

## 6. Puntaje de Frecuencia (Score JAX) y Estrella (⭐) ⚡
*   **Score JAX:** Calificación de 0 a 1 para la combinación.
*   **La Estrella (⭐):** Si ves una estrella en la columna **"ADN Ganador"**, significa que esa combinación sugerida tiene un Score **igual o superior** al promedio de los ganadores reales del pasado.
*   **Ejemplo:** Si el promedio de ganadores es 0.145 y tu sugerencia tiene **0.1510**, recibirá una **⭐**.

---

## 💡 Estrategia Maestra
1.  Busca combinaciones con la **Estrella (⭐)**.
2.  Verifica que incluyan al menos un número con **Brecha (Gap) alta** (entre 13 y 20).
3.  Asegúrate de que la **Super Balota** sea una de las "Calientes".

---
*Nota: Este análisis aumenta tus probabilidades estadísticas basándose en datos históricos, pero el azar sigue siendo el factor determinante.*
