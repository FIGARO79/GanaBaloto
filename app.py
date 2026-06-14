# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import pandas as pd
try:
    import jax
except ImportError:
    import types
    jax = types.ModuleType("jax")
    jax.numpy = np
from flask import Flask, jsonify, request, send_from_directory

# Evitar preasignación de JAX
os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"

import ganabaloto as gb

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')

FILE_PATH = 'baloto.json'
resultados_cache = {}
mtime_cache = 0

def load_and_analyze():
    global resultados_cache, mtime_cache
    mtime = os.path.getmtime(FILE_PATH) if os.path.exists(FILE_PATH) else 0
    if not resultados_cache or mtime != mtime_cache:
        if os.path.exists(FILE_PATH):
            try:
                with open(FILE_PATH, 'r', encoding='utf-8') as f:
                    data_json = json.load(f)
                resultados_cache = {}
                for s in ['Baloto', 'Revancha']:
                    if s in data_json:
                        df = pd.DataFrame(data_json[s])
                        resultados_cache[s] = gb.analizar_sorteo(s, df)
                mtime_cache = mtime
                print("[SISTEMA] Base de datos analizada e indexada en memoria.")
            except Exception as e:
                print(f"[ERROR] Al cargar/analizar baloto.json: {e}")

# Asegurar carga inicial
try:
    load_and_analyze()
except Exception as e:
    print(f"[ERROR] Error en carga inicial: {e}")

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/sorteo/<tipo>', methods=['GET'])
def get_sorteo(tipo):
    load_and_analyze()
    if tipo not in resultados_cache:
        return jsonify({"error": f"Sorteo {tipo} no encontrado"}), 404
    
    r = resultados_cache[tipo]
    
    # Calcular Score JAX y Probabilidad Markov del último sorteo
    last_score = 0.0
    if r.get('historical_data_valid_for_jax', False):
        try:
            last_score = float(gb.calculate_frequency_score_jax(
                jax.numpy.array(r['last_combination']),
                jax.numpy.array(r['last_sb']),
                r['b_cols_jax'],
                r['sb_col_jax'],
                r['total_draws_jax_val']
            ))
        except Exception as e:
            print(f"[ERROR] Al calcular last_score: {e}")
            
    last_markov = float(gb.calculate_sequence_probability(r['last_combination'], r['df_transition_matrix']))

    # Calcular umbrales históricos
    df_ganadores_ref = gb.analizar_ganadores_historicos(r)
    if not df_ganadores_ref.empty:
        scores_ganadores = df_ganadores_ref['Score JAX'].astype(float).values
        score_meta = float(scores_ganadores.mean())
        score_mediana = float(np.median(scores_ganadores))
        score_p75 = float(np.percentile(scores_ganadores, 75))
    else:
        score_meta = 0.1450
        score_mediana = 0.1450
        score_p75 = 0.1550

    # Hot/Cold numbers convert to dict records
    hot = r['df_hot_numbers'].reset_index().rename(columns={'index': 'Balota'}).to_dict(orient='records')
    cold = r['df_cold_numbers'].reset_index().rename(columns={'index': 'Balota'}).to_dict(orient='records')
    chi2 = r['df_chi2'].to_dict(orient='records')
    
    # Parity list of dicts
    parity = []
    for idx, row in r['df_parity_frequencies'].iterrows():
        parity.append({
            'Pares_Impares': f"{idx[0]} Pares - {idx[1]} Impares",
            'Frecuencia': int(row['Frecuencia'])
        })
        
    # Low/High list of dicts
    low_high = []
    for idx, row in r['df_low_high_frequencies'].iterrows():
        low_high.append({
            'Bajos_Altos': f"{idx[0]} Bajos - {idx[1]} Altos",
            'Frecuencia': int(row['Frecuencia'])
        })

    # Decade frequencies list of dicts
    decade = []
    for idx, row in r['df_decade_frequencies'].iterrows():
        decade.append({
            'Decena': idx,
            'Frecuencia': int(row['Frecuencia'])
        })

    # Positional Markov predictions
    pos_top_data = []
    if 'positional_matrices' in r:
        for idx, col in enumerate(gb.COLUMNS_TO_ANALYZE):
            matrix = r['positional_matrices'][col]
            last_val = r['last_combination'][idx]
            if last_val in matrix.index:
                probs = matrix.loc[last_val].sort_values(ascending=False).head(3)
                for dest, prob in probs.items():
                    if prob > 0:
                        pos_top_data.append({
                            'Posicion': col,
                            'Ultimo': int(last_val),
                            'Siguiente': int(dest),
                            'Probabilidad': float(prob)
                        })
        # SB posicional
        sb_matrix = r['positional_matrices'].get(gb.SUPER_BALOTA_COLUMN)
        if sb_matrix is not None and r['last_sb'] in sb_matrix.index:
            sb_probs = sb_matrix.loc[r['last_sb']].sort_values(ascending=False).head(3)
            for dest, prob in sb_probs.items():
                if prob > 0:
                    pos_top_data.append({
                        'Posicion': 'SB',
                        'Ultimo': int(r['last_sb']),
                        'Siguiente': int(dest),
                        'Probabilidad': float(prob)
                    })

    # Winners ADN records
    winners_adn = df_ganadores_ref.to_dict(orient='records') if not df_ganadores_ref.empty else []

    # clean float types from winners_adn (Score JAX might be numpy float)
    for record in winners_adn:
        if 'Score JAX' in record:
            record['Score JAX'] = float(record['Score JAX'])
        if 'Prob. Markov' in record:
            record['Prob. Markov'] = float(record['Prob. Markov'])

    return jsonify({
        "sorteo": tipo,
        "last_combination": [int(x) for x in r['last_combination']],
        "last_sb": int(r['last_sb']),
        "total_combinations": int(r['total_combinations']),
        "score_meta": score_meta,
        "score_mediana": score_mediana,
        "score_p75": score_p75,
        "last_score": last_score,
        "last_markov": last_markov,
        "hot_numbers": hot,
        "cold_numbers": cold,
        "chi2": chi2,
        "parity": parity,
        "low_high": low_high,
        "decade": decade,
        "pos_top_data": pos_top_data,
        "winners_adn": winners_adn
    })

@app.route('/api/generar', methods=['POST'])
def generar():
    load_and_analyze()
    data = request.get_json() or {}
    tipo = data.get('sorteo', 'Baloto')
    cantidad = int(data.get('cantidad', 10))
    
    if tipo not in resultados_cache:
        return jsonify({"error": f"Sorteo {tipo} no encontrado"}), 404
        
    r = resultados_cache[tipo]
    weights = gb.get_number_weights(r, gb.N_MAIN_BALLS, gb.N_SUPER_BALOTA)
    combinaciones = gb.generate_probable_combinations(cantidad, r, weights)

    data_res = []
    has_pos_markov = 'positional_matrices' in r
    for comb, sb, score in combinaciones:
        prob_m = gb.calculate_sequence_probability(comb, r['df_transition_matrix'])
        prob_pos = gb.calculate_positional_markov_probability(
            comb, sb, r['positional_matrices'], r['last_combination'], r['last_sb']
        ) if has_pos_markov else 0.0
        
        data_res.append({
            "combinacion": [int(x) for x in comb],
            "sb": int(sb),
            "score": float(score),
            "prob_m": float(prob_m),
            "prob_pos": float(prob_pos)
        })
        
    return jsonify({
        "combinaciones": data_res
    })

@app.route('/api/analizar', methods=['POST'])
def analizar():
    load_and_analyze()
    data = request.get_json() or {}
    tipo = data.get('sorteo', 'Baloto')
    numeros = data.get('numeros', [])
    sb = data.get('sb', None)
    
    if tipo not in resultados_cache:
        return jsonify({"error": f"Sorteo {tipo} no encontrado"}), 404
        
    if len(numeros) != 5 or sb is None:
        return jsonify({"error": "Parámetros inválidos. Se requieren 5 números principales y una Super Balota."}), 400
        
    r = resultados_cache[tipo]
    jugada_ordenada = sorted([int(x) for x in numeros])
    sb = int(sb)
    
    score = float(gb.calculate_frequency_score_jax(
        jax.numpy.array(jugada_ordenada), jax.numpy.array(sb),
        r['b_cols_jax'], r['sb_col_jax'], r['total_draws_jax_val']
    ))
    
    prob_m = float(gb.calculate_sequence_probability(jugada_ordenada, r['df_transition_matrix']))
    
    prob_pos = 0.0
    if 'positional_matrices' in r:
        prob_pos = float(gb.calculate_positional_markov_probability(
            jugada_ordenada, sb, r['positional_matrices'], r['last_combination'], r['last_sb']
        ))
        
    return jsonify({
        "combinacion": jugada_ordenada,
        "sb": sb,
        "score": score,
        "prob_m": prob_m,
        "prob_pos": prob_pos
    })

@app.route('/api/recargar', methods=['POST'])
def recargar():
    global resultados_cache
    resultados_cache = {}
    try:
        load_and_analyze()
        return jsonify({"status": "ok", "message": "Base de datos recargada con éxito."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Ruta catch-all para servir index.html ante cualquier ruta desconocida (para soporte de React Router si se requiere)
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
