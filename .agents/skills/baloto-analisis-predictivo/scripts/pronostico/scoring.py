"""Funciones de puntuación de una jugada: motor JAX, similitud con botes y popularidad."""

import jax
import numpy as np
import pandas as pd

from . import config  # noqa: F401  (garantiza sys.path)
import ganabaloto as gb


def evaluar_jugada_directa(comb, sb, r):
    """Evalúa una combinación de 5 balotas y Super Balota usando el motor JAX de 7 dimensiones (incluye Weibull e Ising)."""
    comb = sorted(list(comb))
    sb = int(sb)
    score = float(gb.calculate_frequency_score_jax(
        jax.numpy.array(comb), jax.numpy.array(sb),
        r["b_cols_jax"], r["sb_col_jax"], r["total_draws_jax_val"]
    ))
    score_gauss = float(gb.calculate_sum_gaussian_score(comb))
    score_entropy = float(gb.calculate_shannon_entropy(comb))
    score_bayes = float(gb.calculate_bayesian_dirichlet_score(
        comb, sb, r.get("main_counts_dict", {}), r.get("sb_counts_dict", {}), r.get("total_draws", 0)
    ))
    score_hazard = float(gb.calculate_gap_hazard_score(
        comb, sb, r.get("df_gap_analysis", pd.DataFrame())
    ))
    score_ising = float(gb.calculate_ising_energy_score(
        comb, r.get("ising_matrix")
    ))
    prob_m = float(gb.calculate_sequence_probability(comb, r["df_transition_matrix"]))
    prob_pos = 0.0
    if "positional_matrices" in r:
        prob_pos = gb.calculate_positional_markov_probability(
            comb, sb, r["positional_matrices"], r["last_combination"], r["last_sb"]
        )
    composite = float(gb.calculate_composite_score(
        score, prob_m, prob_pos, score_gauss, score_entropy, score_bayes, score_hazard, score_ising
    ))
    return comb, sb, score, composite, score_gauss, score_entropy, score_bayes, score_hazard, score_ising


def calcular_similitud_botes(comb, sb, botes):
    """Similitud 0-100 con el perfil histórico de botes: frecuencia en botes, perfil y solape máximo."""
    if not botes:
        return 0.0
    frec = {}
    for b, _ in botes:
        for x in b:
            frec[x] = frec.get(x, 0) + 1
    # 1. Frecuencia de cada balota dentro de los botes (normalizada por la máxima posible)
    max_f = max(frec.values())
    freq_norm = sum(frec.get(x, 0) for x in comb) / (5 * max_f)
    # 2. Perfil: suma, bajos y SB alta frente a los botes
    sumas = np.array([sum(b) for b, _ in botes], dtype=float)
    mu, sd = sumas.mean(), max(sumas.std(), 1e-6)
    p_suma = float(np.exp(-0.5 * ((sum(comb) - mu) / sd) ** 2))
    bajos_b = np.mean([sum(1 for x in b if x <= 21) for b, _ in botes])
    p_bajos = 1.0 - min(abs(sum(1 for x in comb if x <= 21) - bajos_b) / 5.0, 1.0)
    sb_alta = float(np.mean([s >= 11 for _, s in botes]))
    p_sb = sb_alta if sb >= 11 else 1.0 - sb_alta
    perfil = 0.5 * p_suma + 0.25 * p_bajos + 0.25 * p_sb
    # 3. Solape máximo con algún bote concreto (0 a 5 balotas)
    solape = max(len(set(comb) & set(b)) for b, _ in botes) / 5.0
    return round(100.0 * (0.4 * freq_norm + 0.35 * perfil + 0.25 * solape), 1)


def calcular_popularidad(comb, sb):
    """Popularidad 0-100: cuanto más alta, más probable que otros jueguen la misma combinación."""
    comb = sorted(comb)
    pop = 0.0
    if all(x <= 31 for x in comb):
        pop += 35  # patrón de cumpleaños / fechas
    elif sum(1 for x in comb if x <= 31) == 4:
        pop += 12
    pop += 12 * sum(1 for k in range(4) if comb[k + 1] - comb[k] == 1)  # consecutivos
    if len({comb[k + 1] - comb[k] for k in range(4)}) == 1:
        pop += 30  # progresión aritmética (5-10-15-20-25)
    pop += 4 * sum(1 for x in comb if x in (3, 7, 11, 13))  # números de la suerte
    if sb <= 12:
        pop += 5  # SB como mes de nacimiento
    return round(min(pop, 100.0), 1)
