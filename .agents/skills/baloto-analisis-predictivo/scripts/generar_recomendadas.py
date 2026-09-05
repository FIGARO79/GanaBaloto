#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI para generar combinaciones recomendadas de Baloto o Revancha
utilizando los 6 modelos estadísticos estocásticos de GanaBaloto.
"""

import sys
import os
import argparse
import json
import io
import pandas as pd
import numpy as np

# Asegurar que el directorio raíz del proyecto esté en sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Silenciar salida de banner en import si se solicita JSON
_is_json = "--json" in sys.argv
if _is_json:
    _old_stdout = sys.stdout
    sys.stdout = sys.stderr

import ganabaloto as gb

try:
    import jax
    import jax.numpy as jnp
except ImportError:
    import numpy as jnp

if _is_json:
    sys.stdout = _old_stdout


def parse_args():
    parser = argparse.ArgumentParser(
        description="Genera combinaciones candidatas con alto perfil probabilístico para Baloto o Revancha."
    )
    parser.add_argument(
        "--sorteo",
        type=str,
        default="Baloto",
        choices=["Baloto", "Revancha", "Ambos"],
        help="Tipo de sorteo (Baloto, Revancha o Ambos. Default: Baloto).",
    )
    parser.add_argument(
        "--cantidad",
        type=int,
        default=10,
        help="Número de combinaciones a generar por sorteo (default: 10).",
    )
    parser.add_argument(
        "--min-indice",
        type=float,
        default=0.0,
        help="Filtrar jugadas con un Índice Compuesto mínimo (ej: 70.0).",
    )
    parser.add_argument(
        "--solo-adn",
        action="store_true",
        help="Filtrar y mostrar únicamente jugadas que alcancen el score promedio histórico de ganadores (ADN 🧬).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Retornar resultados en formato JSON.",
    )
    return parser.parse_args()


def procesar_sorteo(sorteo_nombre, data_json, cantidad, min_indice=0.0, solo_adn=False):
    df = pd.DataFrame(data_json[sorteo_nombre])
    r = gb.analizar_sorteo(sorteo_nombre, df)
    weights = gb.get_number_weights(r, gb.N_MAIN_BALLS, gb.N_SUPER_BALOTA)

    # Generamos un margen extra si hay filtros para garantizar la cantidad deseada
    extra_generar = cantidad * 3 if (min_indice > 0 or solo_adn) else cantidad
    combinaciones = gb.generate_probable_combinations(extra_generar, r, weights)

    df_ganadores = gb.analizar_ganadores_historicos(r)
    score_meta = float(df_ganadores["Score JAX"].mean()) if not df_ganadores.empty else 0.1450
    has_pos_markov = "positional_matrices" in r

    resultados = []
    for item in combinaciones:
        if len(item) == 8:
            comb, sb, score, composite, score_gauss, score_entropy, score_bayes, score_hazard = item
        else:
            comb, sb, score = item[0], item[1], item[2]
            composite, score_gauss, score_entropy, score_bayes, score_hazard = 50.0, 0.5, 0.5, 0.5, 0.5

        if composite < min_indice:
            continue
        if solo_adn and score < score_meta:
            continue

        prob_m = float(gb.calculate_sequence_probability(comb, r["df_transition_matrix"]))
        prob_pos = (
            float(
                gb.calculate_positional_markov_probability(
                    comb, sb, r["positional_matrices"], r["last_combination"], r["last_sb"]
                )
            )
            if has_pos_markov
            else 0.0
        )

        es_optimo = composite >= 70.0
        tiene_adn = score >= score_meta

        resultados.append({
            "combinacion": [int(x) for x in comb],
            "sb": int(sb),
            "suma": sum(comb),
            "indice_compuesto": round(float(composite), 2),
            "score_jax": round(float(score), 4),
            "score_gauss": round(float(score_gauss), 2),
            "score_entropia": round(float(score_entropy), 2),
            "score_bayes": round(float(score_bayes), 2),
            "score_hazard": round(float(score_hazard), 2),
            "prob_m": float(prob_m),
            "prob_pos": float(prob_pos),
            "es_optimo": es_optimo,
            "tiene_adn": tiene_adn,
        })

        if len(resultados) >= cantidad:
            break

    # Asignar distintivo top 1
    for idx, res in enumerate(resultados):
        res["es_top1"] = (idx == 0)

    return {
        "sorteo": sorteo_nombre,
        "score_meta_ganadores": round(score_meta, 4),
        "total_generadas": len(resultados),
        "jugadas": resultados,
    }


def main():
    args = parse_args()

    json_path = os.path.join(PROJECT_ROOT, gb.FILE_PATH)
    if not os.path.exists(json_path):
        print(f"❌ Error: No se encontró la base de datos {json_path}", file=sys.stderr)
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data_json = json.load(f)

    sorteos_a_procesar = ["Baloto", "Revancha"] if args.sorteo == "Ambos" else [args.sorteo]

    todos_los_resultados = {}
    for s in sorteos_a_procesar:
        if s in data_json:
            todos_los_resultados[s] = procesar_sorteo(
                s, data_json, args.cantidad, args.min_indice, args.solo_adn
            )

    if args.json:
        print(json.dumps(todos_los_resultados, indent=2, ensure_ascii=False))
    else:
        for s, datos in todos_los_resultados.items():
            print("\n" + "=" * 80)
            print(f"🎱 SUGERENCIAS MULTIMODELO RECOMENDADAS - {s.upper()}")
            print(f"Meta histórica de ganadores (Score JAX): {datos['score_meta_ganadores']}")
            print("=" * 80)

            filas = []
            for idx, jugada in enumerate(datos["jugadas"], 1):
                badge = ""
                if jugada["es_top1"]:
                    badge += "🏆 Top#1 "
                if jugada["es_optimo"]:
                    badge += "🌟 "
                if jugada["tiene_adn"]:
                    badge += "🧬 ADN"

                comb_str = "-".join(f"{n:02d}" for n in jugada["combinacion"])
                filas.append({
                    "#": idx,
                    "Combinación": f"{comb_str} + [{jugada['sb']:02d}]",
                    "Suma": jugada["suma"],
                    "Índice": f"{jugada['indice_compuesto']:.1f}",
                    "JAX": f"{jugada['score_jax']:.4f}",
                    "Gauss": f"{jugada['score_gauss']:.2f}",
                    "Entropía": f"{jugada['score_entropia']:.2f}",
                    "Bayes": f"{jugada['score_bayes']:.2f}",
                    "Hazard": f"{jugada['score_hazard']:.2f}",
                    "Insignias": badge.strip(),
                })

            df_tabla = pd.DataFrame(filas)
            if not df_tabla.empty:
                print(df_tabla.to_markdown(index=False))
            else:
                print("⚠️ No se encontraron combinaciones que cumplan los filtros solicitados.")
            print("-" * 80)
            print("Leyenda: 🏆 = Máximo Índice | 🌟 = Perfil Óptimo (≥70.0) | 🧬 = ADN Ganador (≥ Score Meta)\n")


if __name__ == "__main__":
    main()
