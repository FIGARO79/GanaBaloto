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

    counts = r_b.get("main_counts_dict", {})
    mas_frec = [num for num, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:4]]

    df_gaps = r_b.get("df_gap_analysis", pd.DataFrame())
    mas_atrasadas = []
    if not df_gaps.empty:
        main_gaps = df_gaps[df_gaps["Tipo"] == "Main"].sort_values("Brecha (Sorteos)", ascending=False)
        mas_atrasadas = [int(x) for x in main_gaps["Número"].head(4).tolist()]

    anclajes = [x for x in info_sorteo["anclajes_principales"] if 1 <= x <= gb.N_MAIN_BALLS]
    pivotes = [8, 4, 28, 10, 14]
    lag_8_balotas = info_sorteo.get("lag_8_data", {}).get("Baloto", {}).get("balotas", [])

    # Selección integrada de 7 números clave:
    # 2 de fecha/anclaje + 1 pivote histórico + 1 de resonancia Lag-8 + 2 frecuentes + 1 atrasada
    pool = set()
    for num in anclajes[:2]:
        pool.add(num)
    for num in pivotes:
        if num not in pool:
            pool.add(num)
            break
    for num in lag_8_balotas:
        if num not in pool:
            pool.add(num)
            break
    for num in mas_frec:
        if num not in pool:
            pool.add(num)
            if len(pool) >= 6:
                break
    for num in mas_atrasadas:
        if num not in pool:
            pool.add(num)
            if len(pool) == 7:
                break

    # Si faltan para 7, rellenar de frecuentes o atrasadas
    for num in mas_frec + mas_atrasadas:
        if len(pool) < 7:
            pool.add(num)

    pool = sorted(list(pool))

    # Super Balotas reinas según el análisis de botes
    top_sbs = [15, 10] if 15 in info_sorteo["sbs_reinas"]["Baloto"] else [11, 13]

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
