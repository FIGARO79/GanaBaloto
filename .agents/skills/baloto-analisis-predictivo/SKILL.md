---
name: baloto-analisis-predictivo
description: >-
  Use this skill when the user wants to analyze, evaluate, audit, or generate lottery combinations for Baloto and Revancha using the 6-dimension stochastic statistical engine (Score JAX, Markov chains, Gaussian sum, Bayesian Dirichlet, Hazard rate gaps, Shannon entropy), or when calculating reduced wheeling systems (ruedas combinatorias) with mathematical hit guarantees.
---

# Análisis Predictivo y Generación de Jugadas (Baloto & Revancha)

Esta skill proporciona herramientas y procedimientos automatizados para auditar combinaciones de lotería, generar pronósticos basados en el **Índice Compuesto Global (0 a 100)** y construir **Ruedas Combinatorias Reducidas**.

Para profundizar en la formulación matemática de los 6 modelos estocásticos, consulta la referencia:
[Modelos Matemáticos y Métricas Estadísticas](./references/modelos_matematicos.md).

---

## Capacidades y Flujos de Trabajo

### 1. Diagnóstico y Auditoría de una Jugada Manual
Evalúa cualquier boleto de 5 balotas principales (1-43) y 1 Super Balota (1-16) contra el histórico completo y los 6 modelos predictivos.

**Comando:**
```bash
./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/evaluar_jugada.py \
  --sorteo Baloto \
  --numeros 4 8 15 23 42 \
  --sb 7
```

**Salida generada:**
* **Índice Compuesto Global (0-100)** y desglose de cada score.
* Detección de distintivos: **🌟 [Perfil Óptimo]** ($\ge 70$) y **🧬 [ADN Ganador]** ($\ge \text{score\_meta}$).
* Veredicto cualitativo con recomendaciones sobre suma (zona dorada 90-130), dispersión/entropía y rotación por atraso (Hazard rate).
* Soporta la opción `--json` para integración programática.

---

### 2. Generación Automática de Jugadas Recomendadas
Genera un lote de combinaciones candidatas con la máxima eficiencia estadística, aplicando filtros de calidad.

**Comandos habituales:**

* **Generar Top 10 para Baloto:**
  ```bash
  ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/generar_recomendadas.py --sorteo Baloto --cantidad 10
  ```

* **Generar combinaciones para Revancha con Perfil Óptimo ($\ge 70$):**
  ```bash
  ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/generar_recomendadas.py --sorteo Revancha --cantidad 5 --min-indice 70.0
  ```

* **Generar solo jugadas con ADN Ganador 🧬 para ambos sorteos:**
  ```bash
  ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/generar_recomendadas.py --sorteo Ambos --cantidad 5 --solo-adn
  ```

* **Modo JSON:**
  Agrega `--json` para obtener el resultado estructurado.

---

### 3. Ruedas Combinatorias Reducidas (Wheeling System)
Permite al usuario seleccionar entre 5 y 12 números favoritos y generar un conjunto reducido de tiquetes optimizados que garantiza matemáticamente 3 o 4 aciertos (si los números ganadores están dentro de la selección).

**Comandos:**

* **Garantía 3 aciertos (Recomendado para presupuesto ajustado):**
  ```bash
  ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/generar_rueda.py \
    --numeros 4 8 15 23 31 38 42 \
    --sbs 7 11 \
    --garantia 3
  ```

* **Garantía 4 aciertos:**
  ```bash
  ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/generar_rueda.py \
    --numeros 2 11 19 24 30 36 41 \
    --garantia 4
  ```

---

## Verificación y Diagnóstico Rápido
Para comprobar que el motor predictivo y JAX funcionan adecuadamente:
```bash
./.venv/bin/python -c "import ganabaloto as gb; print('JAX Activo:', gb.HAS_JAX)"
```
Si detecta GPU NVIDIA, aprovechará aceleración por hardware; de lo contrario, conmutará fluidamente a CPU.
