"""Rueda combinatoria reducida (wheeling)."""

import itertools

import pandas as pd

from . import config  # noqa: F401  (garantiza sys.path)
import ganabaloto as gb

# Patrón de cobertura: 5 bloques de 5 sobre 7 números
BLOQUES_INDICES = [
    [0, 1, 2, 3, 4],
    [0, 1, 2, 5, 6],
    [0, 3, 4, 5, 6],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 6],
]


def verificar_garantia(bloques=BLOQUES_INDICES, n_numeros=7, garantia=3):
    """Cubre toda terna de los n números en algún bloque? (garantía de `garantia` aciertos si salen `garantia` o más)."""
    ternas = set(itertools.combinations(range(n_numeros), garantia))
    cubiertas = set()
    for b in bloques:
        cubiertas.update(itertools.combinations(sorted(b), garantia))
    return ternas <= cubiertas, len(ternas - cubiertas)


def construir_rueda_optima(data_json, info_sorteo):
    """Construye una selección inteligente de 7 números y 2 SBs para Rueda Reducida sincronizada."""
    df_b = pd.DataFrame(data_json["Baloto"])
    r_b = gb.analizar_sorteo("Baloto", df_b)
    weights = gb.get_number_weights(r_b, gb.N_MAIN_BALLS, gb.N_SUPER_BALOTA)

    # 1. Balotas líderes por peso estocástico JAX / Markov / Bayes
    top_jax = sorted(range(1, gb.N_MAIN_BALLS + 1), key=lambda x: weights[("main", x)], reverse=True)

    # 2. Balotas con mayor madurez estadística por Hazard Rate Weibull / Atrasadas
    df_gaps = r_b.get("df_gap_analysis", pd.DataFrame())
    mas_atrasadas = []
    if not df_gaps.empty:
        main_gaps = df_gaps[df_gaps["Tipo"] == "Main"].sort_values("Brecha (Sorteos)", ascending=False)
        mas_atrasadas = [int(x) for x in main_gaps["Número"].head(6).tolist()]

    # 3. Anclajes y resonancia cíclica
    anclajes = [x for x in info_sorteo["anclajes_principales"] if 1 <= x <= gb.N_MAIN_BALLS]
    lag_8_balotas = info_sorteo.get("lag_8_data", {}).get("Baloto", {}).get("balotas", [])

    # Construcción balanceada del pool de 7 números clave:
    # - 3 balotas líderes absolutas en peso estocástico JAX (máximo momentum actual)
    # - 2 balotas líderes en madurez por Hazard Rate (alta probabilidad de retorno)
    # - 1 balota de resonancia cíclica Lag-8 o anclaje de fecha
    # - 1 balota complementaria de alto peso JAX
    pool = set()

    # Top 3 momentum JAX
    for num in top_jax:
        pool.add(num)
        if len(pool) >= 3:
            break

    # Top 2 Hazard Weibull
    for num in mas_atrasadas:
        if num not in pool:
            pool.add(num)
            if len(pool) >= 5:
                break

    # 1 de resonancia cíclica o anclaje
    for num in lag_8_balotas + anclajes:
        if num not in pool:
            pool.add(num)
            break

    # Complementar hasta 7 con las siguientes líderes de JAX
    for num in top_jax:
        if num not in pool:
            pool.add(num)
            if len(pool) >= 7:
                break

    pool = sorted(list(pool))

    # Super Balotas líderes: seleccionar las 2 con mayor peso estocástico JAX
    top_sbs = sorted(range(1, gb.N_SUPER_BALOTA + 1), key=lambda x: weights[("sb", x)], reverse=True)[:2]

    tiquetes = []
    for b in BLOQUES_INDICES:
        combo = [pool[i] for i in b]
        for sb in top_sbs:
            tiquetes.append({
                "comb": combo,
                "sb": sb,
                "texto": f"{'-'.join(f'{x:02d}' for x in combo)} + SB [{sb:02d}]",
            })

    return {
        "numeros_pool": pool,
        "super_balotas": top_sbs,
        "garantia": 3,
        "total_tiquetes": len(tiquetes),
        "tiquetes": tiquetes,
    }
