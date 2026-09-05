#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI para evaluar y diagnosticar una jugada manual de Baloto o Revancha
utilizando los 6 modelos estadísticos estocásticos de GanaBaloto.
"""

import sys
import os
import argparse
import json
import pandas as pd
import numpy as np

# Asegurar que el directorio raíz del proyecto esté en sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import ganabaloto as gb

try:
    import jax
    import jax.numpy as jnp
except ImportError:
    import numpy as jnp


def parse_args():
    parser = argparse.ArgumentParser(
        description="Evalúa una combinación personalizada (5 balotas + SB) usando los 6 modelos de GanaBaloto."
    )
    parser.add_argument(
        "--sorteo",
        type=str,
        default="Baloto",
        choices=["Baloto", "Revancha"],
        help="Tipo de sorteo a analizar (default: Baloto).",
    )
    parser.add_argument(
        "--numeros",
        type=int,
        nargs=5,
        required=True,
        metavar=("N1", "N2", "N3", "N4", "N5"),
        help="5 números principales entre 1 y 43 (ej: --numeros 4 8 15 23 42).",
    )
    parser.add_argument(
        "--sb",
        type=int,
        required=True,
        metavar="SB",
        help="Super Balota entre 1 y 16 (ej: --sb 7).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Retorna el resultado en formato JSON en lugar de texto plano.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Validaciones de entrada
    numeros = sorted(args.numeros)
    if len(set(numeros)) != 5:
        print("❌ Error: Los 5 números principales deben ser distintos.", file=sys.stderr)
        sys.exit(1)

    for n in numeros:
        if n < 1 or n > gb.N_MAIN_BALLS:
            print(f"❌ Error: El número {n} está fuera de rango (1-{gb.N_MAIN_BALLS}).", file=sys.stderr)
            sys.exit(1)

    if args.sb < 1 or args.sb > gb.N_SUPER_BALOTA:
        print(f"❌ Error: La Super Balota {args.sb} está fuera de rango (1-{gb.N_SUPER_BALOTA}).", file=sys.stderr)
        sys.exit(1)

    # Cargar datos
    json_path = os.path.join(PROJECT_ROOT, gb.FILE_PATH)
    if not os.path.exists(json_path):
        print(f"❌ Error: No se encontró la base de datos {json_path}", file=sys.stderr)
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data_json = json.load(f)

    if args.sorteo not in data_json:
        print(f"❌ Error: Sorteo {args.sorteo} no encontrado en {json_path}", file=sys.stderr)
        sys.exit(1)

    df = pd.DataFrame(data_json[args.sorteo])
    r = gb.analizar_sorteo(args.sorteo, df)

    # Cálculos estadísticos
    score = float(
        gb.calculate_frequency_score_jax(
            jnp.array(numeros),
            jnp.array(args.sb),
            r["b_cols_jax"],
            r["sb_col_jax"],
            r["total_draws_jax_val"],
        )
    )
    prob_m = float(gb.calculate_sequence_probability(numeros, r["df_transition_matrix"]))
    prob_pos = 0.0
    if "positional_matrices" in r:
        prob_pos = float(
            gb.calculate_positional_markov_probability(
                numeros,
                args.sb,
                r["positional_matrices"],
                r["last_combination"],
                r["last_sb"],
            )
        )

    score_gauss = float(gb.calculate_sum_gaussian_score(numeros))
    score_entropy = float(gb.calculate_shannon_entropy(numeros))
    score_bayes = float(
        gb.calculate_bayesian_dirichlet_score(
            numeros,
            args.sb,
            r.get("main_counts_dict", {}),
            r.get("sb_counts_dict", {}),
            r.get("total_draws", 0),
        )
    )
    score_hazard = float(
        gb.calculate_gap_hazard_score(numeros, args.sb, r.get("df_gap_analysis", pd.DataFrame()))
    )
    composite = float(
        gb.calculate_composite_score(
            score, prob_m, prob_pos, score_gauss, score_entropy, score_bayes, score_hazard
        )
    )

    df_ganadores = gb.analizar_ganadores_historicos(r)
    score_mediana = float(df_ganadores["Score JAX"].median()) if not df_ganadores.empty else 0.1450
    score_meta = float(df_ganadores["Score JAX"].mean()) if not df_ganadores.empty else 0.1450

    veredicto_lines = gb.obtener_veredicto_cualitativo(
        numeros, args.sb, composite, score, score_gauss, score_entropy, score_bayes, score_hazard, score_mediana
    )

    es_optimo = composite >= 70.0
    tiene_adn = score >= score_meta

    if args.json:
        resultado = {
            "sorteo": args.sorteo,
            "numeros": numeros,
            "sb": args.sb,
            "suma_balotas": sum(numeros),
            "indice_compuesto": round(composite, 2),
            "es_perfil_optimo": es_optimo,
            "tiene_adn_ganador": tiene_adn,
            "desglose_scores": {
                "score_jax": round(score, 6),
                "score_gauss": round(score_gauss, 4),
                "score_entropia": round(score_entropy, 4),
                "score_bayes": round(score_bayes, 4),
                "score_hazard": round(score_hazard, 4),
                "prob_markov_global": round(prob_m, 8),
                "prob_markov_posicional": round(prob_pos, 8),
            },
            "referencias_historicas": {
                "score_meta_promedio": round(score_meta, 4),
                "score_mediana": round(score_mediana, 4),
                "ultimo_sorteo": [int(x) for x in r["last_combination"]],
                "ultima_sb": int(r["last_sb"]),
            },
            "veredicto": veredicto_lines,
        }
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        badge_optimo = "🌟 [Perfil Óptimo]" if es_optimo else ""
        badge_adn = "🧬 [ADN Ganador]" if tiene_adn else ""
        print("\n" + "=" * 65)
        print(f"🎱 DIAGNÓSTICO DE JUGADA - {args.sorteo.upper()}")
        print(f"Combinación: {numeros} + SB({args.sb})  {badge_optimo} {badge_adn}")
        print("=" * 65)
        print(f"🏆 ÍNDICE COMPUESTO GLOBAL : {composite:.1f} / 100")
        print(f"   1. Score JAX (Frecuencia Histórica) : {score:.6f} (Meta: {score_meta:.4f})")
        print(f"   2. Distribución Gauss (Suma = {sum(numeros)}) : {score_gauss:.4f} (Zona: 90-130)")
        print(f"   3. Entropía de Shannon (Dispersión)  : {score_entropy:.4f}")
        print(f"   4. Inferencia Bayesiana Dirichlet    : {score_bayes:.4f}")
        print(f"   5. Presión Hazard Rate (Atrasos)    : {score_hazard:.4f}")
        print(f"   6. Markov Global / Posicional        : {prob_m:.8f} / {prob_pos:.8f}")
        print("-" * 65)
        print("📋 VEREDICTO CUALITATIVO:")
        for line in veredicto_lines:
            print(f"  {line}")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
