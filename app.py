# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import pandas as pd
import ganabaloto as gb

try:
    import jax
except ImportError:
    import types

    jax = types.ModuleType("jax")
    jax.numpy = np

from flask import Flask, jsonify, request, send_from_directory

# Configuración de la aplicación
app_config = {"static_folder": "frontend/dist", "static_url_path": ""}

app = Flask(__name__, **app_config)
run_config = {"host": "0.0.0.0", "port": 5000, "debug": True}
FILE_PATH = "baloto.json"
resultados_cache = {}
mtime_cache = 0


def load_and_analyze():
    global resultados_cache, mtime_cache
    mtime = os.path.getmtime(FILE_PATH) if os.path.exists(FILE_PATH) else 0
    if not resultados_cache or mtime != mtime_cache:
        if os.path.exists(FILE_PATH):
            try:
                with open(FILE_PATH, "r", encoding="utf-8") as f:
                    data_json = json.load(f)
                resultados_cache = {}
                for s in ["Baloto", "Revancha"]:
                    if s in data_json:
                        df = pd.DataFrame(data_json[s])
                        resultados_cache[s] = gb.analizar_sorteo(s, df)
                mtime_cache = mtime
                print("[SISTEMA] Base de datos analizada e indexada en memoria.")
            except Exception as e:
                app.logger.error(f"Error al cargar/analizar baloto.json: {e}")


# Asegurar carga inicial
try:
    load_and_analyze()
except Exception as e:
    app.logger.error(f"Error en carga inicial: {e}")


@app.route("/ads.txt")
def ads_txt():
    return send_from_directory(app.static_folder, "ads.txt")


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/sorteo/<tipo>", methods=["GET"])
def get_sorteo(tipo):
    load_and_analyze()
    if tipo not in resultados_cache:
        return jsonify({"error": f"Sorteo {tipo} no encontrado"}), 404

    r = resultados_cache[tipo]

    # Calcular Score JAX y Probabilidad Markov del último sorteo
    last_score = 0.0
    if r.get("historical_data_valid_for_jax", False):
        try:
            last_score = float(
                gb.calculate_frequency_score_jax(
                    jax.numpy.array(r["last_combination"]),
                    jax.numpy.array(r["last_sb"]),
                    r["b_cols_jax"],
                    r["sb_col_jax"],
                    r["total_draws_jax_val"],
                )
            )
        except Exception as e:
            app.logger.error(f"Error al calcular last_score: {e}")

    last_markov = float(
        gb.calculate_sequence_probability(
            r["last_combination"], r["df_transition_matrix"]
        )
    )

    # Calcular umbrales históricos
    df_ganadores_ref = gb.analizar_ganadores_historicos(r)
    if not df_ganadores_ref.empty:
        scores_ganadores = df_ganadores_ref["Score JAX"].astype(float).values
        score_meta = float(scores_ganadores.mean())
        score_mediana = float(np.median(scores_ganadores))
        score_p75 = float(np.percentile(scores_ganadores, 75))
    else:
        score_meta = 0.1450
        score_mediana = 0.1450
        score_p75 = 0.1550

    # Hot/Cold numbers convert to dict records
    hot = (
        r["df_hot_numbers"]
        .reset_index()
        .rename(columns={"index": "Balota"})
        .to_dict(orient="records")
    )
    cold = (
        r["df_cold_numbers"]
        .reset_index()
        .rename(columns={"index": "Balota"})
        .to_dict(orient="records")
    )
    chi2 = r["df_chi2"].to_dict(orient="records")

    # Parity list of dicts
    parity = []
    for idx, row in r["df_parity_frequencies"].iterrows():
        parity.append(
            {
                "Pares_Impares": f"{idx[0]} Pares - {idx[1]} Impares",
                "Frecuencia": int(row["Frecuencia"]),
            }
        )

    # Low/High list of dicts
    low_high = []
    for idx, row in r["df_low_high_frequencies"].iterrows():
        low_high.append(
            {
                "Bajos_Altos": f"{idx[0]} Bajos - {idx[1]} Altos",
                "Frecuencia": int(row["Frecuencia"]),
            }
        )

    # Decade frequencies list of dicts
    decade = []
    for idx, row in r["df_decade_frequencies"].iterrows():
        decade.append({"Decena": idx, "Frecuencia": int(row["Frecuencia"])})

    # Positional Markov predictions
    pos_top_data = []
    if "positional_matrices" in r:
        for idx, col in enumerate(gb.COLUMNS_TO_ANALYZE):
            matrix = r["positional_matrices"][col]
            last_val = r["last_combination"][idx]
            if last_val in matrix.index:
                probs = matrix.loc[last_val].sort_values(ascending=False).head(3)
                for dest, prob in probs.items():
                    if prob > 0:
                        pos_top_data.append(
                            {
                                "Posicion": col,
                                "Ultimo": int(last_val),
                                "Siguiente": int(dest),
                                "Probabilidad": float(prob),
                            }
                        )
        # SB posicional
        sb_matrix = r["positional_matrices"].get(gb.SUPER_BALOTA_COLUMN)
        if sb_matrix is not None and r["last_sb"] in sb_matrix.index:
            sb_probs = sb_matrix.loc[r["last_sb"]].sort_values(ascending=False).head(3)
            for dest, prob in sb_probs.items():
                if prob > 0:
                    pos_top_data.append(
                        {
                            "Posicion": "SB",
                            "Ultimo": int(r["last_sb"]),
                            "Siguiente": int(dest),
                            "Probabilidad": float(prob),
                        }
                    )

    # Winners ADN records
    winners_adn = (
        df_ganadores_ref.to_dict(orient="records") if not df_ganadores_ref.empty else []
    )

    # clean float types from winners_adn (Score JAX might be numpy float)
    for record in winners_adn:
        if "Score JAX" in record:
            record["Score JAX"] = float(record["Score JAX"])
        if "Prob. Markov" in record:
            record["Prob. Markov"] = float(record["Prob. Markov"])

    regime_info = r.get("regime_info", {})
    lag_8_comb = r.get("lag_8_combination", [])
    lag_8_sb = r.get("lag_8_sb", 0)

    return jsonify(
        {
            "sorteo": tipo,
            "last_combination": [int(x) for x in r["last_combination"]],
            "last_sb": int(r["last_sb"]),
            "total_combinations": int(r["total_combinations"]),
            "total_draws": int(len(r.get("df", []))),
            "score_meta": score_meta,
            "score_mediana": score_mediana,
            "score_p75": score_p75,
            "last_score": last_score,
            "last_markov": last_markov,
            "regime_info": regime_info,
            "lag_8_combination": [int(x) for x in lag_8_comb],
            "lag_8_sb": int(lag_8_sb) if lag_8_sb else 0,
            "hot_numbers": hot,
            "cold_numbers": cold,
            "chi2": chi2,
            "parity": parity,
            "low_high": low_high,
            "decade": decade,
            "pos_top_data": pos_top_data,
            "winners_adn": winners_adn,
        }
    )


@app.route("/api/generar", methods=["POST"])
def generar():
    load_and_analyze()
    data = request.get_json() or {}
    tipo = data.get("sorteo", "Baloto")
    cantidad = int(data.get("cantidad", 10))

    if tipo not in resultados_cache:
        return jsonify({"error": f"Sorteo {tipo} no encontrado"}), 404

    r = resultados_cache[tipo]
    weights = gb.get_number_weights(r, gb.N_MAIN_BALLS, gb.N_SUPER_BALOTA)
    combinaciones = gb.generate_probable_combinations(cantidad, r, weights)

    # Anclajes de fecha y lag-8 para badges
    import datetime
    ahora = datetime.datetime.now()
    dia = ahora.day
    mes = ahora.month
    suma_dia_mes = dia + mes
    anclajes_fecha = {dia, mes, suma_dia_mes}
    lag_8_set = set(r.get("lag_8_combination", []))
    df_ganadores = gb.analizar_ganadores_historicos(r)
    score_meta = float(df_ganadores["Score JAX"].mean()) if not df_ganadores.empty else 0.1450

    data_res = []
    has_pos_markov = "positional_matrices" in r
    for item in combinaciones:
        if len(item) == 8:
            comb, sb, score, composite, score_gauss, score_entropy, score_bayes, score_hazard = item
        else:
            comb, sb, score = item[0], item[1], item[2]
            composite, score_gauss, score_entropy, score_bayes, score_hazard = 50.0, 0.5, 0.5, 0.5, 0.5

        prob_m = gb.calculate_sequence_probability(comb, r["df_transition_matrix"])
        prob_pos = (
            gb.calculate_positional_markov_probability(
                comb, sb, r["positional_matrices"], r["last_combination"], r["last_sb"]
            )
            if has_pos_markov
            else 0.0
        )
        score_ising = float(gb.calculate_ising_energy_score(comb, r.get("ising_matrix")))

        # Insignias automáticas
        insignias = []
        if len(data_res) == 0:
            insignias.append("Top 1")
        if composite >= 70.0:
            insignias.append("Perfil Óptimo")
        if score >= score_meta:
            insignias.append("ADN Ganador")
        if any(x in anclajes_fecha for x in comb):
            insignias.append("Fecha")
        if any(x in lag_8_set for x in comb):
            insignias.append("Lag-8")
        if sb in comb:
            insignias.append("Espejo")
        if any(comb[k+1] - comb[k] in (4, 6) for k in range(len(comb)-1)):
            insignias.append("Delta")
        if score_ising >= 0.52:
            insignias.append("Ising")

        data_res.append(
            {
                "combinacion": [int(x) for x in comb],
                "sb": int(sb),
                "suma": int(sum(comb)),
                "score": float(score),
                "composite": float(composite),
                "score_gauss": float(score_gauss),
                "score_entropy": float(score_entropy),
                "score_bayes": float(score_bayes),
                "score_hazard": float(score_hazard),
                "score_ising": float(score_ising),
                "prob_m": float(prob_m),
                "prob_pos": float(prob_pos),
                "insignias": insignias,
            }
        )

    return jsonify({"combinaciones": data_res})


@app.route("/api/analizar", methods=["POST"])
def analizar():
    load_and_analyze()
    data = request.get_json() or {}
    tipo = data.get("sorteo", "Baloto")
    numeros = data.get("numeros", [])
    sb = data.get("sb", None)

    if tipo not in resultados_cache:
        return jsonify({"error": f"Sorteo {tipo} no encontrado"}), 404

    if len(numeros) != 5 or sb is None:
        return jsonify(
            {
                "error": "Parámetros inválidos. Se requieren 5 números principales y una Super Balota."
            }
        ), 400

    r = resultados_cache[tipo]
    jugada_ordenada = sorted([int(x) for x in numeros])
    sb = int(sb)

    score = float(
        gb.calculate_frequency_score_jax(
            jax.numpy.array(jugada_ordenada),
            jax.numpy.array(sb),
            r["b_cols_jax"],
            r["sb_col_jax"],
            r["total_draws_jax_val"],
        )
    )

    prob_m = float(
        gb.calculate_sequence_probability(jugada_ordenada, r["df_transition_matrix"])
    )

    prob_pos = 0.0
    if "positional_matrices" in r:
        prob_pos = gb.calculate_positional_markov_probability(
            jugada_ordenada,
            sb,
            r["positional_matrices"],
            r["last_combination"],
            r["last_sb"],
        )

    score_gauss = float(gb.calculate_sum_gaussian_score(jugada_ordenada))
    score_entropy = float(gb.calculate_shannon_entropy(jugada_ordenada))
    score_bayes = float(
        gb.calculate_bayesian_dirichlet_score(
            jugada_ordenada,
            sb,
            r.get("main_counts_dict", {}),
            r.get("sb_counts_dict", {}),
            r.get("total_draws", 0),
        )
    )
    score_hazard = float(
        gb.calculate_gap_hazard_score(
            jugada_ordenada, sb, r.get("df_gap_analysis", pd.DataFrame())
        )
    )
    score_ising = float(
        gb.calculate_ising_energy_score(jugada_ordenada, r.get("ising_matrix"))
    )
    composite = float(
        gb.calculate_composite_score(
            score, prob_m, prob_pos, score_gauss, score_entropy, score_bayes, score_hazard, score_ising
        )
    )

    df_ganadores_m = gb.analizar_ganadores_historicos(r)
    score_med_m = float(df_ganadores_m["Score JAX"].median()) if not df_ganadores_m.empty else 0.1450
    veredicto_lines = gb.obtener_veredicto_cualitativo(
        jugada_ordenada, sb, composite, score, score_gauss, score_entropy, score_bayes, score_hazard, score_med_m
    )

    return jsonify(
        {
            "combinacion": jugada_ordenada,
            "sb": sb,
            "suma": int(sum(jugada_ordenada)),
            "score": score,
            "composite": composite,
            "score_gauss": score_gauss,
            "score_entropy": score_entropy,
            "score_bayes": score_bayes,
            "score_hazard": score_hazard,
            "score_ising": score_ising,
            "prob_m": prob_m,
            "prob_pos": prob_pos,
            "veredicto": veredicto_lines,
        }
    )


@app.route("/api/rueda", methods=["POST"])
def rueda():
    data = request.get_json() or {}
    numeros = data.get("numeros", [])
    garantia = int(data.get("garantia", 3))
    raw_sbs = data.get("sbs", [])
    if not raw_sbs and "sb" in data and data["sb"] is not None:
        raw_sbs = [data["sb"]]
    if not raw_sbs:
        raw_sbs = [7]

    sbs = sorted(list(set([int(x) for x in raw_sbs if 1 <= int(x) <= 16])))
    if not sbs:
        sbs = [7]

    sorteo = data.get("sorteo", "Baloto")

    if len(numeros) < 5 or len(numeros) > 15:
        return jsonify({"error": "Debe seleccionar entre 5 y 15 números para la rueda."}), 400

    try:
        base_wheels = gb.generate_wheeling_system(numeros, target_guarantee=garantia)
        tiquetes_finales = []
        for comb in base_wheels:
            for sb_val in sbs:
                tiquetes_finales.append({
                    "combinacion": comb,
                    "sb": sb_val
                })

        return jsonify(
            {
                "ruedas": base_wheels,
                "tiquetes_finales": tiquetes_finales,
                "total_tiquetes": len(tiquetes_finales),
                "tiquetes_base": len(base_wheels),
                "superbalotas": sbs,
                "sorteo": sorteo,
                "numeros_seleccionados": sorted([int(x) for x in set(numeros)]),
                "garantia": garantia,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/recargar", methods=["POST"])
def recargar():
    global resultados_cache
    resultados_cache = {}
    try:
        load_and_analyze()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"status": "success"})


@app.route("/api/agente/trigger", methods=["POST"])
def agente_trigger():
    data = request.get_json() or {}
    comando = (data.get("trigger") or "").strip().upper()
    valid_triggers = ["PRONOSTICO", "PRONÓSTICO", "JUGADAS", "GANABALOTO", "EJECUTAR", "RUN"]

    if not any(t in comando for t in valid_triggers):
        return jsonify({
            "error": f"Trigger '{comando}' no reconocido. Usa 'PRONOSTICO', 'JUGADAS' o 'GANABALOTO'."
        }), 400

    try:
        import subprocess
        import sys

        script_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            ".agents/skills/baloto-analisis-predictivo/scripts/ejecutar_pronostico_completo.py"
        )

        # 1. Ejecutar para obtener el markdown estándar completo
        proc_md = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=90
        )

        # 2. Ejecutar con --json para obtener los datos estructurados
        proc_json = subprocess.run(
            [sys.executable, script_path, "--json"],
            capture_output=True,
            text=True,
            timeout=90
        )

        datos_json = {}
        if proc_json.returncode == 0:
            stdout_text = proc_json.stdout
            idx = stdout_text.find("{")
            if idx != -1:
                try:
                    datos_json = json.loads(stdout_text[idx:])
                except Exception as e:
                    app.logger.error(f"Error parsing agent json: {e}")

        return jsonify({
            "status": "success",
            "trigger_ejecutado": comando,
            "markdown": proc_md.stdout,
            "datos": datos_json,
            "stderr": proc_md.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "El motor estocástico excedió el tiempo límite de cálculo."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("[SISTEMA] Iniciando servidor Flask en http://localhost:5000...")
    app.run(**run_config)
