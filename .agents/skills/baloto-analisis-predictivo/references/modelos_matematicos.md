# Modelos Matemáticos y Métricas Estadísticas de GanaBaloto

GanaBaloto integra 6 modelos estocásticos y estadísticos independientes para calcular el **Índice Compuesto Global (0 a 100)**:

$$\text{Índice Compuesto} = 0.25 \cdot S_{\text{JAX}} + 0.20 \cdot M_{\text{Markov}} + 0.20 \cdot S_{\text{Gauss}} + 0.15 \cdot S_{\text{Bayes}} + 0.10 \cdot S_{\text{Hazard}} + 0.10 \cdot S_{\text{Entropía}}$$

---

## 1. Score JAX (ADN Histórico) – Peso: 25%
- **Objetivo**: Medir la intensidad de aparición de las balotas en sorteos históricos premiados.
- **Normalización**: 
  $$\text{Norm}_{\text{JAX}} = \min\left(1.0, \frac{\text{Score JAX}}{0.20}\right)$$
- **Insignia ADN Ganador (🧬)**: Se otorga si el `Score JAX` de la jugada es igual o superior al promedio histórico de los ganadores reales (`score_meta` ≈ 0.145 - 0.150).

## 2. Cadenas de Markov (Global y Posicional) – Peso: 20%
- **Markov Global**: Evalúa la probabilidad de transición $P(b_i \to b_j)$ observada históricamente entre sorteos consecutivos.
- **Markov Posicional**: Evalúa la matriz de transición posicional por columna ($B_1, B_2, B_3, B_4, B_5, SB$) dado el último sorteo real.
- **Cálculo combinado**:
  $$M_{\text{Markov}} = 0.5 \cdot \text{Norm}(P_{\text{Markov Global}}) + 0.5 \cdot \text{Norm}(P_{\text{Markov Posicional}})$$

## 3. Distribución Normal Gaussiana (Suma de Balotas) – Peso: 20%
- **Objetivo**: Evaluar la cercanía de la suma $S = \sum_{i=1}^5 b_i$ a la media teórica/empírica ($\mu \approx 110, \sigma \approx 26.4$).
- **Fórmula**:
  $$S_{\text{Gauss}} = \exp\left( -\frac{(S - \mu)^2}{2\sigma^2} \right)$$
- **Zona Dorada**: Sumas entre **90 y 130**. Sumas < 60 o > 160 son penalizadas por su baja frecuencia empírica.

## 4. Inferencia Bayesiana con Prior Dirichlet – Peso: 15%
- **Objetivo**: Probabilidad *a posteriori* con suavizado de Laplace/Dirichlet para evitar sobreajuste en números poco frecuentes:
  $$S_{\text{Bayes}} = \frac{1}{K} \sum_{i=1}^K \frac{c_i + \alpha}{N + \alpha \cdot M}$$
  donde $c_i$ es el conteo, $N$ el total de sorteos, y $\alpha=1$ (suavizado uniforme).

## 5. Análisis de Brechas y Hazard Rate (Poisson) – Peso: 10%
- **Objetivo**: Evaluar la "presión de retorno" de balotas maduras o frías en función del número de sorteos transcurridos desde su última aparición ($g$).
- **Fórmula**:
  $$S_{\text{Hazard}} = 1 - (1 - \lambda)^g$$
  donde $\lambda = 5 / 43 \approx 0.116$ para balotas principales.

## 6. Entropía de Shannon (Dispersión y Aleatoriedad) – Peso: 10%
- **Objetivo**: Medir la dispersión entre números ordenados consecutivos $d_i = b_{i+1} - b_i$.
- **Fórmula**:
  $$S_{\text{Entropía}} = -\frac{\sum p_i \log_2(p_i)}{\log_2(K)}$$
- Penaliza secuencias consecutivas continuas (ej. 1-2-3-4-5) o aglomeraciones en una misma decena.

---

## Insignias y Calificaciones
- **🏆 Top #1 Recomendación**: La combinación con mayor Índice Compuesto del sorteo.
- **🌟 Perfil Óptimo**: Índice Compuesto $\ge 70.0 / 100$.
- **🧬 ADN Ganador**: Score JAX $\ge \text{score\_meta}$ de ganadores reales históricos.
