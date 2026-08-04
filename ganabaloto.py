# @title Calcular probabilidades del juego con Cadenas de Markov
# -*- coding: utf-8 -*-
"""ganabaloto_v2_markov.ipynb

Este script realiza un análisis estadístico de sorteos de lotería (Baloto y Revancha)
para generar combinaciones con mayor probabilidad histórica, incorporando
diversas métricas, ponderaciones dinámicas y análisis de Cadenas de Markov.
"""

import os

# --- Configuración de Hardware (DEBE IR ANTES DE LOS IMPORTS) ---
# Evitar que JAX reserve toda la VRAM por defecto
os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"
# Silenciar advertencias de hardware (GPU/TPU)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["JAX_PLATFORMS"] = (
    ""  # Permite que JAX elija la mejor disponible sin forzar errores
)

# Importar librerías necesarias
import pandas as pd
import random
from itertools import combinations

try:
    import jax
    import jax.numpy as jnp

    HAS_JAX = True
except ImportError:
    import numpy as jnp

    # Crear un mock de jax.jit que actúe como pasarela
    class MockJax:
        def jit(self, fn):
            return fn

        def devices(self):
            raise Exception("No JAX")

    jax = MockJax()
    HAS_JAX = False

import math
from collections import defaultdict
from scipy import stats
import re
import html
from datetime import datetime

# Reportar dispositivo en uso
if HAS_JAX:
    try:
        dispositivos = jax.devices()
        tipo_dispositivo = dispositivos[0].device_kind.upper()
        print(f"\n[SISTEMA] Motor de cálculo: JAX ({tipo_dispositivo} detectada)")
    except Exception:
        print("\n[SISTEMA] Motor de cálculo: JAX (CPU detectada)")
else:
    print("\n[SISTEMA] Motor de cálculo: NumPy (Respaldo sin JAX activo)")
print("-" * 50)

try:
    from IPython.display import display, HTML
    from IPython import get_ipython

    # Detectar si estamos en un entorno interactivo (Jupyter/Colab)
    if get_ipython() is None:
        IN_NOTEBOOK = False
    else:
        IN_NOTEBOOK = True
except ImportError:
    IN_NOTEBOOK = False

# --- Configuración Global ---
FILE_PATH = "baloto.json"
COLUMNS_TO_ANALYZE = ["B1", "B2", "B3", "B4", "B5"]
SUPER_BALOTA_COLUMN = "SB"
PRIZE_COLUMN = "Premios 5+1"
NUM_COMBINATIONS_TO_GENERATE = 10

# Parámetros para cálculo de probabilidad teórica (Baloto estándar)
N_MAIN_BALLS = 43
K_MAIN_BALLS = 5
N_SUPER_BALOTA = 16

# Parámetros para "Números Calientes" y "Números Fríos"
RECENT_DRAWS_THRESHOLD = 50

# Parámetros para análisis de números Bajos/Altos
LOW_HIGH_SPLIT_POINT = N_MAIN_BALLS // 2


def mostrar_resultado(obj, titulo="", sorteo=""):
    """Muestra el resultado dependiendo de si es Notebook o Terminal."""
    if hasattr(obj, "data"):
        obj = obj.data

    prefix = f"[{sorteo.upper()}] " if sorteo else ""
    if titulo:
        print(f"\n>>> {prefix}{titulo.upper()} <<<")

    if IN_NOTEBOOK:
        if isinstance(obj, pd.DataFrame):
            display(HTML(obj.to_html(classes="table table-striped", border=0)))
        else:
            display(HTML(str(obj)))
    else:
        if isinstance(obj, pd.DataFrame):
            print(obj.to_string())
        else:
            # Limpiar etiquetas HTML para la consola
            texto = str(obj)
            texto = re.sub(r"<br\s*/?>", "\n", texto)
            texto = re.sub(r"</p>", "\n", texto)
            texto_limpio = re.sub(r"<[^<]+?>", "", texto)
            print(html.unescape(texto_limpio).strip())


@jax.jit
def calculate_frequency_score_jax(
    combination_jax, sb_jax, b_cols_jax, sb_col_jax, total_draws_jax
):
    """Calcula un puntaje de frecuencia usando JAX."""
    score = 0.0
    all_main_balls_flat = jnp.concatenate(b_cols_jax)
    for number in combination_jax:
        frequency = jnp.sum(all_main_balls_flat == number)
        score += frequency
    sb_frequency = jnp.sum(sb_col_jax == sb_jax)
    score += sb_frequency * K_MAIN_BALLS
    denominator = total_draws_jax * (K_MAIN_BALLS + 1)
    return jnp.where(denominator == 0, 0.0, score / denominator)


def calculate_sequence_probability(sequence, transition_matrix):
    """Calcula la probabilidad de una secuencia de números basada en Markov."""
    if not sequence or len(sequence) < 2:
        return 1.0
    probability = 1.0
    for i in range(len(sequence) - 1):
        current_num = sequence[i]
        next_num = sequence[i + 1]
        if (
            current_num in transition_matrix.index
            and next_num in transition_matrix.columns
        ):
            transition_prob = transition_matrix.loc[current_num, next_num]
            probability *= transition_prob
        else:
            return 0.0
    return probability


def calculate_positional_markov_probability(
    combination, sb, positional_matrices, last_combination, last_sb
):
    """Calcula la probabilidad usando cadenas de Markov posicionales (B1→B1, B2→B2, etc.)."""
    probability = 1.0
    all_cols = COLUMNS_TO_ANALYZE + [SUPER_BALOTA_COLUMN]
    current_vals = list(combination) + [sb]
    previous_vals = list(last_combination) + [last_sb]

    for i, col in enumerate(all_cols):
        matrix = positional_matrices.get(col)
        if matrix is None or matrix.empty:
            continue
        prev_num = previous_vals[i]
        curr_num = current_vals[i]
        if prev_num in matrix.index and curr_num in matrix.columns:
            prob = matrix.loc[prev_num, curr_num]
            if prob > 0:
                probability *= prob
            else:
                probability *= 1e-10
        else:
            probability *= 1e-10

    return probability


def calculate_sum_gaussian_score(combination, mean_sum=110.0, std_sum=26.4):
    """Calcula un puntaje de campana de Gauss (0 a 1) para la suma de la combinación."""
    c_sum = sum(combination)
    score = math.exp(-((c_sum - mean_sum) ** 2) / (2 * (std_sum ** 2)))
    return max(0.0, min(1.0, score))


def calculate_shannon_entropy(combination):
    """Calcula la entropía de Shannon (0 a 1) basada en las diferencias entre números ordenados."""
    if len(combination) < 2:
        return 1.0
    sorted_c = sorted(combination)
    diffs = [sorted_c[i + 1] - sorted_c[i] for i in range(len(sorted_c) - 1)]
    total_diff = sum(diffs)
    if total_diff == 0:
        return 0.0
    probs = [d / total_diff for d in diffs if d > 0]
    entropy = -sum(p * math.log(p) for p in probs)
    max_entropy = math.log(len(diffs))
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0
    return max(0.0, min(1.0, normalized_entropy))


def calculate_bayesian_dirichlet_score(
    combination, sb, main_counts_dict, sb_counts_dict, total_draws, alpha=1.0
):
    """Calcula la probabilidad a posteriori Dirichlet-Multinomial normalizada (0 a 1)."""
    if total_draws <= 0:
        return 0.5
    prior_prob = 1.0 / N_MAIN_BALLS
    main_score = 0.0
    for num in combination:
        count = main_counts_dict.get(num, 0)
        post_prob = (count + alpha) / (K_MAIN_BALLS * total_draws + N_MAIN_BALLS * alpha)
        main_score += post_prob / (prior_prob * 2.0)

    prior_sb_prob = 1.0 / N_SUPER_BALOTA
    sb_count = sb_counts_dict.get(sb, 0)
    post_sb_prob = (sb_count + alpha) / (total_draws + N_SUPER_BALOTA * alpha)
    sb_score = post_sb_prob / (prior_sb_prob * 2.0)

    total_score = (main_score / K_MAIN_BALLS) * 0.8 + (sb_score) * 0.2
    return max(0.0, min(1.0, total_score))


def calculate_gap_hazard_score(combination, sb, df_gap_analysis):
    """Calcula la presión estadística acumulada (Poisson Hazard Rate) según el atraso de cada número (0 a 1)."""
    if df_gap_analysis.empty:
        return 0.5
    lambda_main = K_MAIN_BALLS / N_MAIN_BALLS
    lambda_sb = 1.0 / N_SUPER_BALOTA

    hazard_scores = []
    gap_map = {}
    for _, row in df_gap_analysis.iterrows():
        tipo = row.get("Tipo")
        num = row.get("Número")
        gap_val = row.get("Brecha (Sorteos)")
        if gap_val != "N/A" and pd.notna(gap_val):
            gap_map[(tipo, int(num))] = float(gap_val)

    for num in combination:
        g = gap_map.get(("Main", num), 0.0)
        cum_p = 1.0 - math.pow(1.0 - lambda_main, g)
        hazard_scores.append(cum_p)

    sb_g = gap_map.get(("SB", sb), 0.0)
    sb_cum_p = 1.0 - math.pow(1.0 - lambda_sb, sb_g)

    avg_main_hazard = sum(hazard_scores) / len(hazard_scores) if hazard_scores else 0.5
    total_hazard = avg_main_hazard * 0.8 + sb_cum_p * 0.2
    return max(0.0, min(1.0, total_hazard))


def calculate_composite_score(
    score_jax,
    prob_markov_global,
    prob_markov_pos,
    score_gauss,
    score_entropy,
    score_bayes,
    score_hazard,
):
    """Calcula un Índice Predictivo Compuesto Global (0 a 100)."""
    norm_jax = min(1.0, score_jax / 0.20)
    norm_markov_g = min(1.0, prob_markov_global * 1e5)
    norm_markov_p = (
        min(1.0, prob_markov_pos * 1e5) if prob_markov_pos > 0 else norm_markov_g
    )
    markov_combined = 0.5 * norm_markov_g + 0.5 * norm_markov_p

    composite = (
        0.25 * norm_jax
        + 0.20 * markov_combined
        + 0.20 * score_gauss
        + 0.15 * score_bayes
        + 0.10 * score_hazard
        + 0.10 * score_entropy
    ) * 100.0

    return round(max(0.0, min(100.0, composite)), 2)


def generate_wheeling_system(selected_numbers, target_guarantee=3):
    """Genera un sistema de ruedas combinatorias reducidas (Wheeling System)."""
    selected_numbers = sorted(list(set(selected_numbers)))
    if len(selected_numbers) < K_MAIN_BALLS:
        raise ValueError(f"Se requieren al menos {K_MAIN_BALLS} números seleccionados.")
    if len(selected_numbers) == K_MAIN_BALLS:
        return [selected_numbers]

    all_combinations = list(combinations(selected_numbers, K_MAIN_BALLS))
    if len(selected_numbers) <= 8 and target_guarantee >= 4:
        return [list(c) for c in all_combinations]

    uncovered_subsets = set(combinations(selected_numbers, target_guarantee))
    selected_wheels = []

    while uncovered_subsets and len(selected_wheels) < len(all_combinations):
        best_comb = None
        best_covered = set()
        for comb in all_combinations:
            if comb in selected_wheels:
                continue
            comb_subsets = set(combinations(comb, target_guarantee))
            covered = comb_subsets.intersection(uncovered_subsets)
            if len(covered) > len(best_covered):
                best_covered = covered
                best_comb = comb

        if not best_comb:
            break

        selected_wheels.append(list(best_comb))
        uncovered_subsets -= best_covered

    return selected_wheels


def get_number_weights(results, n_main_balls, n_super_balota):
    """Asigna pesos a los números basados en las métricas calculadas."""
    weights = defaultdict(float)
    for i in range(1, n_main_balls + 1):
        weights[("main", i)] = 1.0
    for i in range(1, n_super_balota + 1):
        weights[("sb", i)] = 1.0

    # Ponderar por frecuencia en ganadores
    if not results["df_refined_predictions"].empty:
        for col in COLUMNS_TO_ANALYZE:
            if col in results["refined_predictions"]:
                for num in results["refined_predictions"][col]:
                    weights[("main", num)] += 0.5
        if "Super Balota" in results["refined_predictions"]:
            for num in results["refined_predictions"]["Super Balota"]:
                weights[("sb", num)] += 0.5

    # Ponderar por frecuencia general
    if results["all_draws_frequencies"]:
        for col_name, nums in results["all_draws_frequencies"].items():
            if col_name == "Super Balota":
                for num in nums:
                    weights[("sb", num)] += 0.2
            else:
                for num in nums:
                    weights[("main", num)] += 0.2

    # Ponderar por calientes
    if results["hot_numbers"]:
        for col, nums in results["hot_numbers"].items():
            key = "sb" if col == "Super Balota" else "main"
            for num in nums:
                weights[(key, num)] += 0.3

    # Ponderar por fríos
    if results["cold_numbers"]:
        for col, nums in results["cold_numbers"].items():
            key = "sb" if col == "Super Balota" else "main"
            for num in nums:
                weights[(key, num)] += 0.1

    # Pares
    if results["pair_frequencies"]:
        max_pair_freq = max(results["pair_frequencies"].values())
        for (n1, n2), freq in results["pair_frequencies"].items():
            normalized_freq = freq / max_pair_freq
            weights[("main", n1)] += normalized_freq * 0.4
            weights[("main", n2)] += normalized_freq * 0.4

    # Gap
    if not results["df_gap_analysis"].empty:
        df_gap = results["df_gap_analysis"]
        valid_gaps = df_gap[df_gap["Brecha (Sorteos)"] != "N/A"].copy()
        valid_gaps["Brecha (Sorteos)"] = pd.to_numeric(valid_gaps["Brecha (Sorteos)"])
        top_cold = valid_gaps.sort_values(by="Brecha (Sorteos)", ascending=False).head(
            5
        )
        for _, row in top_cold.iterrows():
            num = row["Número"]
            key = "sb" if row.get("Tipo") == "SB" else "main"
            weights[(key, num)] += 0.25

    # Inferencia Bayesiana
    if "main_counts_dict" in results and "total_draws" in results:
        main_counts = results["main_counts_dict"]
        tot = results["total_draws"]
        if tot > 0:
            for num in range(1, n_main_balls + 1):
                post_prob = (main_counts.get(num, 0) + 1.0) / (
                    5 * tot + n_main_balls * 1.0
                )
                weights[("main", num)] += post_prob * 10.0
        sb_counts = results.get("sb_counts_dict", {})
        if tot > 0:
            for num in range(1, n_super_balota + 1):
                post_sb_prob = (sb_counts.get(num, 0) + 1.0) / (
                    tot + n_super_balota * 1.0
                )
                weights[("sb", num)] += post_sb_prob * 5.0

    # Markov Global
    if not results["df_transition_matrix"].empty:
        incoming_sum = results["df_transition_matrix"].sum(axis=0)
        max_incoming = incoming_sum.max() if incoming_sum.max() > 0 else 1
        for num, prob_sum in incoming_sum.items():
            weights[("main", num)] += (prob_sum / max_incoming) * 0.3

    # Markov Posicional: pondera según transiciones del último sorteo por posición
    if "positional_matrices" in results and results.get("last_combination"):
        last_combo = results["last_combination"]
        last_sb_val = results["last_sb"]
        for i, col in enumerate(COLUMNS_TO_ANALYZE):
            matrix = results["positional_matrices"].get(col)
            if matrix is not None and not matrix.empty:
                prev_num = last_combo[i]
                if prev_num in matrix.index:
                    probs = matrix.loc[prev_num]
                    max_prob = probs.max() if probs.max() > 0 else 1
                    for num in range(1, n_main_balls + 1):
                        if num in probs.index and probs[num] > 0:
                            weights[("main", num)] += (probs[num] / max_prob) * 0.25
        # SB posicional
        sb_matrix = results["positional_matrices"].get(SUPER_BALOTA_COLUMN)
        if sb_matrix is not None and not sb_matrix.empty:
            if last_sb_val in sb_matrix.index:
                sb_probs = sb_matrix.loc[last_sb_val]
                max_sb_prob = sb_probs.max() if sb_probs.max() > 0 else 1
                for num in range(1, n_super_balota + 1):
                    if num in sb_probs.index and sb_probs[num] > 0:
                        weights[("sb", num)] += (sb_probs[num] / max_sb_prob) * 0.25

    return weights



def generate_probable_combinations(num_combinations, results, weights):
    """Genera combinaciones probables para un sorteo específico."""
    if not results["historical_data_valid_for_jax"]:
        return []

    generated = []
    attempts = 0
    max_attempts = num_combinations * 200

    main_numbers = list(range(1, N_MAIN_BALLS + 1))
    main_weights = [weights[("main", i)] for i in main_numbers]
    sb_numbers = list(range(1, N_SUPER_BALOTA + 1))
    sb_weights = [weights[("sb", i)] for i in sb_numbers]

    top_sums = (
        results["df_sum_frequencies"].head(5).index.tolist()
        if not results["df_sum_frequencies"].empty
        else []
    )
    top_parity = (
        set(results["df_parity_frequencies"].head(3).index.tolist())
        if not results["df_parity_frequencies"].empty
        else set()
    )
    top_low_high = (
        set(results["df_low_high_frequencies"].head(3).index.tolist())
        if not results["df_low_high_frequencies"].empty
        else set()
    )

    transition_matrix = results["df_transition_matrix"]
    all_main_numbers_list = results["all_main_numbers_list"]
    markov_possible = not transition_matrix.empty and len(all_main_numbers_list) > 0

    # Markov Posicional
    positional_matrices = results.get("positional_matrices", {})
    last_combination = results.get("last_combination", [])
    last_sb_val = results.get("last_sb", 0)
    positional_markov_possible = (
        bool(positional_matrices) and len(last_combination) == K_MAIN_BALLS
    )

    while len(generated) < num_combinations and attempts < max_attempts:
        attempts += 1
        combination = []
        sb = None

        roll = random.random()

        # Markov Posicional (40%): genera cada posición basándose en el último sorteo
        if positional_markov_possible and roll < 0.4:
            try:
                combo = []
                for i, col in enumerate(COLUMNS_TO_ANALYZE):
                    matrix = positional_matrices[col]
                    prev_num = last_combination[i]
                    if prev_num in matrix.index:
                        probs = matrix.loc[prev_num].copy()
                        # Excluir números ya elegidos para evitar duplicados
                        for chosen in combo:
                            if chosen in probs.index:
                                probs[chosen] = 0
                        if probs.sum() > 0:
                            next_num = random.choices(
                                probs.index.tolist(), weights=probs.values.tolist(), k=1
                            )[0]
                            combo.append(next_num)
                        else:
                            break
                    else:
                        break

                if len(combo) == K_MAIN_BALLS:
                    combination = sorted(combo)
                    # SB posicional
                    sb_matrix = positional_matrices.get(SUPER_BALOTA_COLUMN)
                    if sb_matrix is not None and last_sb_val in sb_matrix.index:
                        sb_probs = sb_matrix.loc[last_sb_val]
                        if sb_probs.sum() > 0:
                            sb = random.choices(
                                sb_probs.index.tolist(),
                                weights=sb_probs.values.tolist(),
                                k=1,
                            )[0]
                    if sb is None:
                        sb = random.choices(sb_numbers, weights=sb_weights, k=1)[0]
            except Exception:
                positional_markov_possible = False

        # Markov Global (30%): camina por la cadena de transiciones globales
        elif markov_possible and roll < 0.7:
            try:
                current_num = random.choice(all_main_numbers_list)
                seq = [current_num]
                while len(seq) < K_MAIN_BALLS:
                    if current_num in transition_matrix.index:
                        probs = transition_matrix.loc[current_num]
                        if not probs[probs > 0].empty:
                            next_num = random.choices(
                                probs.index, weights=probs.values, k=1
                            )[0]
                            if next_num not in seq:
                                seq.append(next_num)
                                current_num = next_num
                            else:
                                break
                        else:
                            break
                    else:
                        break
                if len(seq) < K_MAIN_BALLS:
                    remaining = K_MAIN_BALLS - len(seq)
                    avail = [n for n in main_numbers if n not in seq]
                    avail_w = [weights[("main", n)] for n in avail]
                    seq.extend(random.choices(avail, weights=avail_w, k=remaining))
                combination = sorted(seq)
                sb = random.choices(sb_numbers, weights=sb_weights, k=1)[0]
            except Exception:
                markov_possible = False

        if not combination or len(combination) != K_MAIN_BALLS:
            chosen = set()
            while len(chosen) < K_MAIN_BALLS:
                chosen.add(random.choices(main_numbers, weights=main_weights, k=1)[0])
            combination = sorted(list(chosen))
            sb = random.choices(sb_numbers, weights=sb_weights, k=1)[0]

        # Validaciones de Gauss y Entropía
        score_gauss = calculate_sum_gaussian_score(combination)
        if score_gauss < 0.20:
            continue

        score_entropy = calculate_shannon_entropy(combination)
        if score_entropy < 0.35:
            continue

        evens = sum(1 for x in combination if x % 2 == 0)
        if top_parity and (evens, K_MAIN_BALLS - evens) not in top_parity:
            continue

        lows = sum(1 for x in combination if x <= LOW_HIGH_SPLIT_POINT)
        if top_low_high and (lows, K_MAIN_BALLS - lows) not in top_low_high:
            continue

        if any(c[0] == combination and c[1] == sb for c in generated):
            continue

        score = float(
            calculate_frequency_score_jax(
                jnp.array(combination),
                jnp.array(sb),
                results["b_cols_jax"],
                results["sb_col_jax"],
                results["total_draws_jax_val"],
            )
        )

        prob_m = float(calculate_sequence_probability(combination, transition_matrix))
        prob_pos = float(
            calculate_positional_markov_probability(
                combination,
                sb,
                results.get("positional_matrices", {}),
                last_combination,
                last_sb_val,
            )
            if positional_markov_possible
            else 0.0
        )

        score_bayes = calculate_bayesian_dirichlet_score(
            combination,
            sb,
            results.get("main_counts_dict", {}),
            results.get("sb_counts_dict", {}),
            results.get("total_draws", 0),
        )
        score_hazard = calculate_gap_hazard_score(
            combination, sb, results.get("df_gap_analysis", pd.DataFrame())
        )

        composite = calculate_composite_score(
            score, prob_m, prob_pos, score_gauss, score_entropy, score_bayes, score_hazard
        )

        generated.append(
            (
                combination,
                sb,
                score,
                composite,
                score_gauss,
                score_entropy,
                score_bayes,
                score_hazard,
            )
        )

    generated.sort(key=lambda x: x[3], reverse=True)
    return generated


def analizar_sorteo(nombre_hoja, df):
    """Realiza todo el análisis estadístico para una hoja de sorteo."""
    res = {"nombre": nombre_hoja}
    if df.empty:
        return res

    # Limpieza
    df = df.dropna(subset=[SUPER_BALOTA_COLUMN] + COLUMNS_TO_ANALYZE)
    df[SUPER_BALOTA_COLUMN] = df[SUPER_BALOTA_COLUMN].astype(int)
    for col in COLUMNS_TO_ANALYZE:
        df[col] = pd.to_numeric(df[col]).astype(int)
    res["df"] = df

    # Probabilidad teórica
    last_draw = df.iloc[-1]
    res["last_combination"] = sorted(
        [int(last_draw[col]) for col in COLUMNS_TO_ANALYZE]
    )
    res["last_sb"] = int(last_draw[SUPER_BALOTA_COLUMN])
    res["total_combinations"] = math.comb(N_MAIN_BALLS, K_MAIN_BALLS) * N_SUPER_BALOTA

    # Duplicados
    res["duplicates"] = df[
        df[COLUMNS_TO_ANALYZE + [SUPER_BALOTA_COLUMN]].duplicated(keep=False)
    ]

    # Frecuencias
    res["all_draws_frequencies"] = {
        col: df[col].value_counts().head(5).index.tolist() for col in COLUMNS_TO_ANALYZE
    }
    res["all_draws_frequencies"]["Super Balota"] = (
        df[SUPER_BALOTA_COLUMN].value_counts().head(5).index.tolist()
    )

    if PRIZE_COLUMN in df.columns:
        # Asegurarse de que PRIZE_COLUMN sea numérico
        df[PRIZE_COLUMN] = pd.to_numeric(df[PRIZE_COLUMN], errors="coerce").fillna(0)
        winners = df[df[PRIZE_COLUMN] > 0]
        res["refined_predictions"] = {
            col: winners[col].value_counts().head(5).index.tolist()
            for col in COLUMNS_TO_ANALYZE
        }
        res["refined_predictions"]["Super Balota"] = (
            winners[SUPER_BALOTA_COLUMN].value_counts().head(5).index.tolist()
        )
    else:
        res["refined_predictions"] = {
            col: [] for col in COLUMNS_TO_ANALYZE + ["Super Balota"]
        }

    res["df_all_draws"] = pd.DataFrame.from_dict(
        res["all_draws_frequencies"], orient="index"
    ).rename(columns={i: f"Top {i + 1}" for i in range(5)})
    res["df_refined_predictions"] = pd.DataFrame.from_dict(
        res["refined_predictions"], orient="index"
    ).rename(columns={i: f"Top {i + 1}" for i in range(5)})

    # Chi-cuadrado
    main_counts = df[COLUMNS_TO_ANALYZE].values.flatten()
    obs_main = (
        pd.Series(main_counts)
        .value_counts()
        .reindex(range(1, N_MAIN_BALLS + 1), fill_value=0)
    )
    total_obs_main = obs_main.sum()
    if total_obs_main > 0:
        chi2_m, p_m = stats.chisquare(
            obs_main, f_exp=[total_obs_main / N_MAIN_BALLS] * N_MAIN_BALLS
        )
    else:
        chi2_m, p_m = 0, 1.0

    obs_sb = (
        df[SUPER_BALOTA_COLUMN]
        .value_counts()
        .reindex(range(1, N_SUPER_BALOTA + 1), fill_value=0)
    )
    total_obs_sb = obs_sb.sum()
    if total_obs_sb > 0:
        chi2_s, p_s = stats.chisquare(
            obs_sb, f_exp=[total_obs_sb / N_SUPER_BALOTA] * N_SUPER_BALOTA
        )
    else:
        chi2_s, p_s = 0, 1.0

    res["main_counts_dict"] = obs_main.to_dict()
    res["sb_counts_dict"] = obs_sb.to_dict()
    res["total_draws"] = len(df)

    res["df_chi2"] = pd.DataFrame(
        {
            "Métrica": ["Balotas Principales", "Super Balota"],
            "Chi2 Stat": [f"{chi2_m:.2f}", f"{chi2_s:.2f}"],
            "p-value": [f"{p_m:.4f}", f"{p_s:.4f}"],
            "Interpretación": [
                "No aleatorio" if p < 0.05 else "Aleatorio" for p in [p_m, p_s]
            ],
        }
    )

    # Hot/Cold
    recent = df.tail(RECENT_DRAWS_THRESHOLD)
    res["hot_numbers"] = {
        col: recent[col].value_counts().head(5).index.tolist()
        for col in COLUMNS_TO_ANALYZE
    }
    res["hot_numbers"]["Super Balota"] = (
        recent[SUPER_BALOTA_COLUMN].value_counts().head(3).index.tolist()
    )

    res["cold_numbers"] = {}
    for col in COLUMNS_TO_ANALYZE:
        in_recent = set(recent[col].unique())
        cands = list(set(range(1, N_MAIN_BALLS + 1)) - in_recent)
        res["cold_numbers"][col] = sorted(
            cands,
            key=lambda x: df[df[col] == x].index.max() if x in df[col].unique() else -1,
        )[:5]

    in_recent_sb = set(recent[SUPER_BALOTA_COLUMN].unique())
    cands_sb = list(set(range(1, N_SUPER_BALOTA + 1)) - in_recent_sb)
    res["cold_numbers"]["Super Balota"] = sorted(
        cands_sb,
        key=lambda x: (
            df[df[SUPER_BALOTA_COLUMN] == x].index.max()
            if x in df[SUPER_BALOTA_COLUMN].unique()
            else -1
        ),
    )[:3]

    # Estandarizar longitud de listas para evitar decimales (floats) por NaN
    for k in res["hot_numbers"]:
        while len(res["hot_numbers"][k]) < 5:
            res["hot_numbers"][k].append("")
    for k in res["cold_numbers"]:
        while len(res["cold_numbers"][k]) < 5:
            res["cold_numbers"][k].append("")

    res["df_hot_numbers"] = pd.DataFrame.from_dict(
        res["hot_numbers"], orient="index"
    ).rename(columns={i: f"Caliente {i + 1}" for i in range(5)})
    res["df_cold_numbers"] = pd.DataFrame.from_dict(
        res["cold_numbers"], orient="index"
    ).rename(columns={i: f"Frío {i + 1}" for i in range(5)})

    # Pares
    pair_freqs = defaultdict(int)
    for _, row in df.iterrows():
        for pair in combinations(sorted([row[col] for col in COLUMNS_TO_ANALYZE]), 2):
            pair_freqs[tuple(sorted(pair))] += 1
    res["pair_frequencies"] = pair_freqs

    # Sumas
    sums = df[COLUMNS_TO_ANALYZE].sum(axis=1).value_counts().sort_index()
    res["df_sum_frequencies"] = (
        pd.DataFrame(sums)
        .rename(columns={"count": "Frecuencia"})
        .sort_values(by="Frecuencia", ascending=False)
        .head(10)
    )

    # Paridad y Bajos/Altos
    parities, low_highs = defaultdict(int), defaultdict(int)
    for _, row in df.iterrows():
        m = [row[col] for col in COLUMNS_TO_ANALYZE]
        evens = sum(1 for x in m if x % 2 == 0)
        parities[(evens, K_MAIN_BALLS - evens)] += 1
        lows = sum(1 for x in m if x <= LOW_HIGH_SPLIT_POINT)
        low_highs[(lows, K_MAIN_BALLS - lows)] += 1
    res["df_parity_frequencies"] = pd.DataFrame.from_dict(
        parities, orient="index", columns=["Frecuencia"]
    ).sort_values(by="Frecuencia", ascending=False)
    res["df_low_high_frequencies"] = pd.DataFrame.from_dict(
        low_highs, orient="index", columns=["Frecuencia"]
    ).sort_values(by="Frecuencia", ascending=False)

    # Consecutivos
    cons = defaultdict(int)
    for _, row in df.iterrows():
        m = sorted([row[col] for col in COLUMNS_TO_ANALYZE])
        for i in range(len(m) - 1):
            if m[i + 1] == m[i] + 1:
                cons["2 Consecutivos"] += 1
        for i in range(len(m) - 2):
            if m[i + 1] == m[i] + 1 and m[i + 2] == m[i + 1] + 1:
                cons["3 Consecutivos"] += 1
    res["df_consecutive_frequencies"] = pd.DataFrame.from_dict(
        cons, orient="index", columns=["Ocurrencias"]
    )

    # Gaps
    curr = df.index.max()
    gaps = []
    for n in range(1, N_MAIN_BALLS + 1):
        last = df.index[df[COLUMNS_TO_ANALYZE].isin([n]).any(axis=1)].max()
        gaps.append(
            {
                "Tipo": "Main",
                "Número": n,
                "Última Aparición": last,
                "Brecha (Sorteos)": curr - last if pd.notna(last) else "N/A",
            }
        )
    for n in range(1, N_SUPER_BALOTA + 1):
        last = df.index[df[SUPER_BALOTA_COLUMN] == n].max()
        gaps.append(
            {
                "Tipo": "SB",
                "Número": n,
                "Última Aparición": last,
                "Brecha (Sorteos)": curr - last if pd.notna(last) else "N/A",
            }
        )
    res["df_gap_analysis"] = pd.DataFrame(gaps)

    # Decenas
    decades = defaultdict(int)
    for v in df[COLUMNS_TO_ANALYZE].values.flatten():
        d = (v - 1) // 10
        decades[f"Decena {d * 10 + 1}-{d * 10 + 10}"] += 1
    res["df_decade_frequencies"] = pd.DataFrame.from_dict(
        decades, orient="index", columns=["Frecuencia"]
    ).sort_values(by="Frecuencia", ascending=False)

    # Markov
    trans = defaultdict(lambda: defaultdict(int))
    all_nums = []
    for _, row in df.iterrows():
        m = sorted([row[col] for col in COLUMNS_TO_ANALYZE])
        all_nums.extend(m)
    res["all_main_numbers_list"] = all_nums
    for i in range(len(all_nums) - 1):
        trans[all_nums[i]][all_nums[i + 1]] += 1

    matrix = {}
    for cur, nexts in trans.items():
        tot = sum(nexts.values())
        matrix[cur] = {n: c / tot for n, c in nexts.items()}
    res["df_transition_matrix"] = (
        pd.DataFrame(matrix)
        .T.reindex(index=range(1, N_MAIN_BALLS + 1), columns=range(1, N_MAIN_BALLS + 1))
        .fillna(0)
    )

    # Markov Posicional (B1→B1, B2→B2, etc.)
    positional_matrices = {}
    for col in COLUMNS_TO_ANALYZE + [SUPER_BALOTA_COLUMN]:
        pos_trans = defaultdict(lambda: defaultdict(int))
        col_values = df[col].values
        for i in range(len(col_values) - 1):
            pos_trans[int(col_values[i])][int(col_values[i + 1])] += 1

        pos_matrix = {}
        for cur, nexts in pos_trans.items():
            tot = sum(nexts.values())
            pos_matrix[cur] = {n: c / tot for n, c in nexts.items()}

        max_range = N_SUPER_BALOTA if col == SUPER_BALOTA_COLUMN else N_MAIN_BALLS
        positional_matrices[col] = (
            pd.DataFrame(pos_matrix)
            .T.reindex(index=range(1, max_range + 1), columns=range(1, max_range + 1))
            .fillna(0)
        )

    res["positional_matrices"] = positional_matrices

    # JAX Prep
    try:
        res["b_cols_jax"] = [jnp.array(df[col].values) for col in COLUMNS_TO_ANALYZE]
        res["sb_col_jax"] = jnp.array(df[SUPER_BALOTA_COLUMN].values)
        res["total_draws_jax_val"] = jnp.array(len(df))
        res["historical_data_valid_for_jax"] = True
    except Exception:
        res["historical_data_valid_for_jax"] = False

    return res


def analizar_ganadores_historicos(results):
    """Analiza las combinaciones que han ganado el premio mayor (5+1)."""
    if "df" not in results or results["df"].empty:
        return pd.DataFrame()

    df = results["df"]
    if PRIZE_COLUMN not in df.columns:
        return pd.DataFrame()

    # Filtrar ganadores 5+1
    ganadores = df[df[PRIZE_COLUMN] > 0].copy()

    if ganadores.empty:
        return pd.DataFrame()

    reporte = []

    # Preparar datos JAX
    b_cols_jax = results["b_cols_jax"]
    sb_col_jax = results["sb_col_jax"]
    total_draws_jax_val = results["total_draws_jax_val"]
    transition_matrix = results["df_transition_matrix"]

    for _, row in ganadores.iterrows():
        combination = sorted([int(row[col]) for col in COLUMNS_TO_ANALYZE])
        sb = int(row[SUPER_BALOTA_COLUMN])
        prize_value = row[PRIZE_COLUMN]
        # Intentar obtener la fecha, si no existe usar 'N/A'
        fecha = row.get("Fecha", row.get("FECHA", "N/A"))

        # Calcular Score JAX
        score = float(
            calculate_frequency_score_jax(
                jnp.array(combination),
                jnp.array(sb),
                b_cols_jax,
                sb_col_jax,
                total_draws_jax_val,
            )
        )

        # Calcular Prob. Markov
        prob_markov = calculate_sequence_probability(combination, transition_matrix)

        reporte.append(
            {
                "Fecha": fecha,
                "Combinación": ", ".join(map(str, combination)),
                "SB": sb,
                "Valor Premio": f"{prize_value:,.0f}".replace(",", "."),
                "Score JAX": score,
                "Prob. Markov": prob_markov,
            }
        )

    return pd.DataFrame(reporte)


def main():
    try:
        import json

        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data_json = json.load(f)
        sheets = [s for s in ["Baloto", "Revancha"] if s in data_json]
    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        return

    resultados = {}
    historial_sesion = []  # Acumula resultados para exportar a TXT

    for s in sheets:
        print(f"\nProcesando hoja: {s}...")
        df = pd.DataFrame(data_json[s])
        resultados[s] = analizar_sorteo(s, df)

    # Visualización
    for s in sheets:
        r = resultados[s]
        encabezado = f"{'=' * 20} RESULTADOS {s.upper()} {'=' * 20}"
        print(f"\n{encabezado}")
        historial_sesion.append(f"\n{encabezado}")

        # Reporte ADN de Ganadores
        df_adn = analizar_ganadores_historicos(r)
        if not df_adn.empty:
            mostrar_resultado(df_adn, "ADN DE GANADORES (Histórico 5+1)", s)
            historial_sesion.append(
                f"\n>>> [{s.upper()}] ADN DE GANADORES (HISTÓRICO 5+1) <<<"
            )
            historial_sesion.append(df_adn.to_string())

        # Calcular Score y Markov para la última combinación
        last_score = float(
            calculate_frequency_score_jax(
                jnp.array(r["last_combination"]),
                jnp.array(r["last_sb"]),
                r["b_cols_jax"],
                r["sb_col_jax"],
                r["total_draws_jax_val"],
            )
        )
        last_markov = calculate_sequence_probability(
            r["last_combination"], r["df_transition_matrix"]
        )
        print("\n")
        print(f"Última combinación: {r['last_combination']}, SB: {r['last_sb']}")
        print(f"   📊 Score JAX: {last_score:.4f}")
        print(f"   ⛓️ Prob. Markov: {last_markov:.8f}")
        print(f"Combinaciones posibles: {r['total_combinations']:,}")

        historial_sesion.append(
            f"\nÚltima combinación: {r['last_combination']}, SB: {r['last_sb']}"
        )
        historial_sesion.append(f"   Score JAX: {last_score:.4f}")
        historial_sesion.append(f"   Prob. Markov: {last_markov:.8f}")
        historial_sesion.append(f"Combinaciones posibles: {r['total_combinations']:,}")

        if not r["duplicates"].empty:
            mostrar_resultado(r["duplicates"], "Duplicados", s)

        mostrar_resultado(r["df_all_draws"], "Frecuencias Generales", s)
        historial_sesion.append(f"\n>>> [{s.upper()}] FRECUENCIAS GENERALES <<<")
        historial_sesion.append(r["df_all_draws"].to_string())

        mostrar_resultado(r["df_chi2"], "Prueba Chi-cuadrado", s)
        mostrar_resultado(r["df_hot_numbers"], "Números Calientes", s)
        historial_sesion.append(f"\n>>> [{s.upper()}] NÚMEROS CALIENTES <<<")
        historial_sesion.append(r["df_hot_numbers"].to_string())

        mostrar_resultado(r["df_cold_numbers"], "Números Fríos", s)
        historial_sesion.append(f"\n>>> [{s.upper()}] NÚMEROS FRÍOS <<<")
        historial_sesion.append(r["df_cold_numbers"].to_string())

        mostrar_resultado(r["df_sum_frequencies"], "Top Sumas", s)
        mostrar_resultado(r["df_parity_frequencies"], "Paridad", s)
        mostrar_resultado(r["df_gap_analysis"].head(10), "Gap Analysis (Top 10)", s)

        # Añadir Top Transiciones de Markov
        if not r["df_transition_matrix"].empty:
            melted = r["df_transition_matrix"].stack().reset_index()
            melted.columns = ["Origen", "Destino", "Probabilidad"]
            top_markov = (
                melted[melted["Probabilidad"] > 0]
                .sort_values(by="Probabilidad", ascending=False)
                .head(10)
            )
            mostrar_resultado(top_markov, "Top 10 Transiciones de Markov", s)
            historial_sesion.append(
                f"\n>>> [{s.upper()}] TOP 10 TRANSICIONES DE MARKOV <<<"
            )
            historial_sesion.append(top_markov.to_string(index=False))

        # Predicciones Markov Posicional para el próximo sorteo
        if "positional_matrices" in r:
            pos_top_data = []
            for idx, col in enumerate(COLUMNS_TO_ANALYZE):
                matrix = r["positional_matrices"][col]
                last_val = r["last_combination"][idx]
                if last_val in matrix.index:
                    probs = matrix.loc[last_val].sort_values(ascending=False).head(3)
                    for dest, prob in probs.items():
                        if prob > 0:
                            pos_top_data.append(
                                {
                                    "Posición": col,
                                    "Último": int(last_val),
                                    "Siguiente Probable": int(dest),
                                    "Probabilidad": f"{prob:.4f}",
                                }
                            )
            # SB posicional
            sb_matrix = r["positional_matrices"].get(SUPER_BALOTA_COLUMN)
            if sb_matrix is not None and r["last_sb"] in sb_matrix.index:
                sb_probs = (
                    sb_matrix.loc[r["last_sb"]].sort_values(ascending=False).head(3)
                )
                for dest, prob in sb_probs.items():
                    if prob > 0:
                        pos_top_data.append(
                            {
                                "Posición": "SB",
                                "Último": int(r["last_sb"]),
                                "Siguiente Probable": int(dest),
                                "Probabilidad": f"{prob:.4f}",
                            }
                        )
            if pos_top_data:
                df_pos = pd.DataFrame(pos_top_data)
                mostrar_resultado(
                    df_pos, "🔮 Predicciones Markov Posicional (próximo sorteo)", s
                )
                historial_sesion.append(
                    f"\n>>> [{s.upper()}] PREDICCIONES MARKOV POSICIONAL (PRÓXIMO SORTEO) <<<"
                )
                historial_sesion.append(df_pos.to_string(index=False))

    # Parte Interactiva
    while True:
        print("")
        print("--- MENÚ INTERACTIVO ---")
        print("1. Jugada Manual (Diagnóstico Multimodelo de 6 Dimensiones)")
        print("2. Generación Automática (Sugerencias Ponderadas)")
        print("3. Rueda Combinatoria Reducida (Wheeling System)")
        print("4. Salir")
        opc = input("Seleccione una opción: ")

        if opc in ["1", "2"]:
            print("\n¿Para qué sorteo?")
            print("1. Baloto")
            print("2. Revancha")
            print("3. Ambos")
            sorteo_opc = input("Seleccione: ")

            target_sheets = []
            if sorteo_opc == "1" and "Baloto" in resultados:
                target_sheets = ["Baloto"]
            elif sorteo_opc == "2" and "Revancha" in resultados:
                target_sheets = ["Revancha"]
            elif sorteo_opc == "3":
                target_sheets = sheets
            else:
                print("Opción no válida.")
                continue

            for ts in target_sheets:
                r = resultados[ts]
                if opc == "1":
                    print(f"\n--- Jugada Manual para {ts} ---")
                    try:
                        nums = []
                        while len(nums) < K_MAIN_BALLS:
                            try:
                                n = int(
                                    input(
                                        f"Ingrese número {len(nums) + 1} (1-{N_MAIN_BALLS}): "
                                    )
                                )
                                if n < 1 or n > N_MAIN_BALLS:
                                    print(
                                        f"❌ Error: El número debe estar entre 1 y {N_MAIN_BALLS}."
                                    )
                                elif n in nums:
                                    print(
                                        f"❌ Error: El número {n} ya fue ingresado. Elija uno diferente."
                                    )
                                else:
                                    nums.append(n)
                            except ValueError:
                                print(
                                    "❌ Error: Por favor, ingrese un número entero válido."
                                )

                        sb = -1
                        while sb < 1 or sb > N_SUPER_BALOTA:
                            try:
                                sb = int(
                                    input(
                                        f"Ingrese Super Balota (1-{N_SUPER_BALOTA}): "
                                    )
                                )
                                if sb < 1 or sb > N_SUPER_BALOTA:
                                    print(
                                        f"❌ Error: La Super Balota debe estar entre 1 y {N_SUPER_BALOTA}."
                                    )
                            except ValueError:
                                print(
                                    "❌ Error: Por favor, ingrese un número entero válido."
                                )

                        nums_sorted = sorted(nums)
                        score = float(
                            calculate_frequency_score_jax(
                                jnp.array(nums_sorted),
                                jnp.array(sb),
                                r["b_cols_jax"],
                                r["sb_col_jax"],
                                r["total_draws_jax_val"],
                            )
                        )
                        prob_m = float(
                            calculate_sequence_probability(
                                nums_sorted, r["df_transition_matrix"]
                            )
                        )
                        prob_pos_val = 0.0
                        if "positional_matrices" in r:
                            prob_pos_val = float(
                                calculate_positional_markov_probability(
                                    nums_sorted,
                                    sb,
                                    r["positional_matrices"],
                                    r["last_combination"],
                                    r["last_sb"],
                                )
                            )

                        score_gauss = calculate_sum_gaussian_score(nums_sorted)
                        score_entropy = calculate_shannon_entropy(nums_sorted)
                        score_bayes = calculate_bayesian_dirichlet_score(
                            nums_sorted,
                            sb,
                            r.get("main_counts_dict", {}),
                            r.get("sb_counts_dict", {}),
                            r.get("total_draws", 0),
                        )
                        score_hazard = calculate_gap_hazard_score(
                            nums_sorted, sb, r.get("df_gap_analysis", pd.DataFrame())
                        )
                        composite = calculate_composite_score(
                            score,
                            prob_m,
                            prob_pos_val,
                            score_gauss,
                            score_entropy,
                            score_bayes,
                            score_hazard,
                        )

                        print(f"\n✅ DIAGNÓSTICO DE JUGADA MANUAL ({ts}): {nums_sorted} + SB({sb})")
                        print(f"   🏆 ÍNDICE COMPUESTO GLOBAL: {composite:.1f} / 100")
                        print(f"   📊 1. Score JAX (Frecuencia): {score:.6f}")
                        print(f"   📈 2. Score Gaussiano (Suma={sum(nums_sorted)}): {score_gauss:.4f}")
                        print(f"   🔀 3. Entropía de Shannon (Aleatoriedad): {score_entropy:.4f}")
                        print(f"   🎲 4. Prob. Inferencia Bayesiana: {score_bayes:.4f}")
                        print(f"   ⏳ 5. Presión Poisson Hazard Rate (Atrasos): {score_hazard:.4f}")
                        print(f"   ⛓️ 6. Markov Global: {prob_m:.8f} | Markov Posicional: {prob_pos_val:.8f}")

                        historial_sesion.append(f"\n--- Jugada Manual {ts} ---")
                        historial_sesion.append(
                            f"Combinación: {nums_sorted} + SB({sb}) | ÍNDICE COMPUESTO: {composite:.1f}/100"
                        )
                        historial_sesion.append(
                            f"  JAX: {score:.6f} | Gauss: {score_gauss:.4f} | Entropía: {score_entropy:.4f} | Bayes: {score_bayes:.4f} | Hazard: {score_hazard:.4f} | M.Global: {prob_m:.8f} | M.Pos: {prob_pos_val:.8f}"
                        )
                    except Exception as e:
                        print(f"❌ Ocurrió un error inesperado: {e}")
                else:
                    print(f"\n--- Generando para {ts} ---")
                    weights = get_number_weights(r, N_MAIN_BALLS, N_SUPER_BALOTA)
                    combs = generate_probable_combinations(
                        NUM_COMBINATIONS_TO_GENERATE, r, weights
                    )

                    df_ganadores = analizar_ganadores_historicos(r)
                    score_meta = (
                        df_ganadores["Score JAX"].mean()
                        if not df_ganadores.empty
                        else 0.1450
                    )

                    print(
                        f"Nota: El Score promedio de los ganadores históricos de {ts} es: {score_meta:.4f}"
                    )

                    data_res = []
                    has_pos_markov = "positional_matrices" in r
                    for item in combs:
                        if len(item) == 8:
                            comb, sb, score, composite, score_gauss, score_entropy, score_bayes, score_hazard = item
                        else:
                            comb, sb, score = item[0], item[1], item[2]
                            composite, score_gauss, score_entropy, score_bayes, score_hazard = 50.0, 0.5, 0.5, 0.5, 0.5

                        prob_m = calculate_sequence_probability(
                            comb, r["df_transition_matrix"]
                        )
                        prob_pos = (
                            calculate_positional_markov_probability(
                                comb,
                                sb,
                                r["positional_matrices"],
                                r["last_combination"],
                                r["last_sb"],
                            )
                            if has_pos_markov
                            else 0.0
                        )
                        data_res.append(
                            (
                                ", ".join(map(str, comb)),
                                sb,
                                f"{composite:.1f}/100",
                                f"{score:.4f}",
                                f"{score_gauss:.2f}",
                                f"{score_entropy:.2f}",
                                f"{score_bayes:.2f}",
                                f"{score_hazard:.2f}",
                                f"{prob_m:.8f}",
                                f"{prob_pos:.8f}",
                                "⭐" if score >= score_meta else "",
                            )
                        )

                    df_res = pd.DataFrame(
                        data_res,
                        columns=[
                            "Combinación",
                            "SB",
                            "Índice Compuesto",
                            "Score JAX",
                            "Gauss",
                            "Entropía",
                            "Bayes",
                            "Hazard",
                            "M. Global",
                            "M. Posicional",
                            "ADN",
                        ],
                    )
                    mostrar_resultado(df_res, f"Sugerencias Multimodelo {ts}")
                    historial_sesion.append(
                        f"\n--- Generación Automática {ts} (Score meta: {score_meta:.4f}) ---"
                    )
                    historial_sesion.append(df_res.to_string(index=False))

        elif opc == "3":
            print("\n--- ⚙️ SISTEMA DE RUEDAS COMBINATORIAS REDUCIDAS (WHEELING SYSTEM) ---")
            try:
                print("¿Para qué sorteo deseas aplicar la rueda?")
                print("1. Baloto")
                print("2. Revancha")
                print("3. Ambos (Baloto + Revancha)")
                sorteo_rueda_opc = input("Seleccione (1-3): ").strip()
                sorteo_nombre = "Baloto y Revancha" if sorteo_rueda_opc == "3" else ("Revancha" if sorteo_rueda_opc == "2" else "Baloto")

                raw_nums = input("\nIngrese entre 5 y 12 números principales (1-43) separados por espacio o coma (ej: 4 8 15 23 31 38 42): ")
                nums_input = list(set([int(x) for x in re.split(r"[,\s]+", raw_nums.strip()) if x.isdigit() and 1 <= int(x) <= N_MAIN_BALLS]))
                if len(nums_input) < 5 or len(nums_input) > 12:
                    print(f"❌ Error: Debe ingresar entre 5 y 12 números válidos entre 1 y {N_MAIN_BALLS}.")
                    continue

                sb_input = input(f"Ingrese una o varias Super Balotas (1-{N_SUPER_BALOTA}) separadas por espacio/coma (ej: 3 7 11), o Enter para usar la favorita: ").strip()
                sbs_list = list(set([int(x) for x in re.split(r"[,\s]+", sb_input) if x.isdigit() and 1 <= int(x) <= N_SUPER_BALOTA]))
                if not sbs_list:
                    ref_key = "Revancha" if sorteo_rueda_opc == "2" else "Baloto"
                    sb_val = resultados[ref_key]["last_sb"] if ref_key in resultados else 7
                    sbs_list = [sb_val]
                    print(f"   ℹ️ Se usará Super Balota sugerida: {sb_val}")
                else:
                    sbs_list = sorted(sbs_list)

                garantia = 3
                raw_garantia = input("Seleccione nivel de garantía de aciertos [3 para 3 aciertos (recomendado), 4 para 4 aciertos]: ")
                if raw_garantia.strip() == "4":
                    garantia = 4

                ruedas_base = generate_wheeling_system(nums_input, target_guarantee=garantia)

                # Generar tiquetes finales combinando ruedas base x superbalotas
                tiquetes_finales = []
                for comb in ruedas_base:
                    for sb_val in sbs_list:
                        tiquetes_finales.append((comb, sb_val))

                print(f"\n🎉 ¡RUEDA GENERADA EXITOSAMENTE PARA {sorteo_nombre.upper()}!")
                print(f"   Números seleccionados ({len(nums_input)}): {sorted(nums_input)}")
                print(f"   Super Balotas fijadas ({len(sbs_list)}): {sbs_list}")
                print(f"   Nivel de garantía: {garantia} Aciertos")
                print(f"   Combinaciones base de 5 balotas: {len(ruedas_base)}")
                print(f"   Total de tiquetes de juego requeridos: {len(tiquetes_finales)}")
                print("\n📋 TIQUETES DE JUEGO SUGERIDOS:")
                for idx, (tiquete, sb_val) in enumerate(tiquetes_finales, 1):
                    print(f"   Tiquete #{idx}: {tiquete} + SB({sb_val}) [{sorteo_nombre}]")

                historial_sesion.append(f"\n--- Rueda Combinatoria ({sorteo_nombre}) ---")
                historial_sesion.append(f"Selección: {sorted(nums_input)} | SBs: {sbs_list} | Garantía: {garantia} aciertos | Total Tiquetes: {len(tiquetes_finales)}")
                for idx, (tiquete, sb_val) in enumerate(tiquetes_finales, 1):
                    historial_sesion.append(f"  Tiquete #{idx}: {tiquete} + SB({sb_val})")
            except Exception as e:
                print(f"❌ Error al procesar rueda combinatoria: {e}")

        elif opc == "4":
            guardar = input(
                "\n¿Deseas guardar los resultados en un archivo TXT? (s/n): "
            )
            if guardar.strip().lower() == "s":
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nombre_archivo = f"GanaBaloto_Resultados_{timestamp}.txt"
                    with open(nombre_archivo, "w", encoding="utf-8") as f:
                        f.write("=" * 60 + "\n")
                        f.write("  🎱 GanaBaloto - Reporte de Resultados\n")
                        f.write(
                            f"  Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                        )
                        f.write("=" * 60 + "\n")
                        f.write("\n".join(historial_sesion))
                        f.write("\n\n" + "=" * 60 + "\n")
                        f.write("  Fin del reporte\n")
                        f.write("=" * 60 + "\n")
                    print(f"\n✅ Resultados guardados en: {nombre_archivo}")
                except Exception as e:
                    print(f"\n❌ Error al guardar: {e}")

            print("\n¡Gracias por usar GanaBaloto! Saliendo...")
            input("Presione Enter para finalizar...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
