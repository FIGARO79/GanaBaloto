#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente Refinador de Pronósticos GanaBaloto
Ejecuta el ciclo multi-agente:
1. Agente Muestreador Estocástico (JAX / Markov)
2. Agente Auditor Heurístico y Estadístico
3. Agente Optimizador de Portafolio y Cobertura
"""

import sys
import os
import json
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import ganabaloto as gb

def auditar_candidata(comb, sb, r, ultimo_sorteo, score_meta):
    c = sorted(comb)
    suma = sum(c)
    
    # 1. Filtro de Paridad
    pares = sum(1 for x in c if x % 2 == 0)
    impares = 5 - pares
    paridad_valida = (pares in (2, 3))
    
    # 2. Consecutivos (máximo 1 pareja, jamás trío o más)
    diffs = [c[i+1] - c[i] for i in range(4)]
    consecutivos = sum(1 for d in diffs if d == 1)
    hay_trio_consecutivo = any(diffs[i] == 1 and diffs[i+1] == 1 for i in range(3))
    
    # 3. Decenas (1-9, 10-19, 20-29, 30-39, 40-43)
    def decena(n):
        if n < 10: return 0
        elif n < 20: return 1
        elif n < 30: return 2
        elif n < 40: return 3
        else: return 4
    decenas_counts = {}
    for x in c:
        d = decena(x)
        decenas_counts[d] = decenas_counts.get(d, 0) + 1
    
    max_en_decena = max(decenas_counts.values())
    decenas_cubiertas = len(decenas_counts)
    
    # 4. Superposición con último sorteo (máximo 1 balota repetida)
    repetidas_ultimo = len(set(c).intersection(set(ultimo_sorteo)))
    
    # 5. Suma en zona Gaussiana
    suma_optima = (85 <= suma <= 135)
    
    if hay_trio_consecutivo:
        return False, "Rechazada por trío consecutivo"
    if consecutivos > 1:
        return False, "Rechazada por más de 1 pareja consecutiva"
    if max_en_decena > 2:
        return False, f"Rechazada por concentración excesiva en decena ({max_en_decena} números)"
    if decenas_cubiertas < 3:
        return False, "Rechazada por baja dispersión de decenas (<3 decenas)"
    if repetidas_ultimo > 1:
        return False, f"Rechazada por {repetidas_ultimo} números repetidos del sorteo anterior"
    if not paridad_valida:
        return False, f"Rechazada por paridad desbalanceada ({pares}P/{impares}I)"
    if not suma_optima:
        return False, f"Rechazada por suma fuera de rango ({suma})"
        
    return True, {
        "paridad": f"{pares}P/{impares}I",
        "consecutivos": consecutivos,
        "decenas_cubiertas": decenas_cubiertas,
        "repetidas_ultimo": repetidas_ultimo,
        "suma": suma
    }

def refinar_sorteo(sorteo_nombre, data_json, num_jugadas_finales=3):
    df = pd.DataFrame(data_json[sorteo_nombre])
    r = gb.analizar_sorteo(sorteo_nombre, df)
    weights = gb.get_number_weights(r, gb.N_MAIN_BALLS, gb.N_SUPER_BALOTA)
    
    df_ganadores = gb.analizar_ganadores_historicos(r)
    score_meta = float(df_ganadores["Score JAX"].mean()) if not df_ganadores.empty else 0.1450
    score_mediana = float(df_ganadores["Score JAX"].median()) if not df_ganadores.empty else 0.1450
    ultimo_sorteo = r.get("last_combination", [])
    ultima_sb = r.get("last_sb", 0)
    
    candidatos_brutos = gb.generate_probable_combinations(400, r, weights)
    
    candidatos_auditados = []
    for item in candidatos_brutos:
        if len(item) == 8:
            comb, sb, score, composite, score_gauss, score_entropy, score_bayes, score_hazard = item
        else:
            continue
            
        pasa, audit_info = auditar_candidata(comb, sb, r, ultimo_sorteo, score_meta)
        if not pasa:
            continue
            
        prob_m = float(gb.calculate_sequence_probability(comb, r["df_transition_matrix"]))
        prob_pos = float(gb.calculate_positional_markov_probability(
            comb, sb, r.get("positional_matrices", {}), ultimo_sorteo, ultima_sb
        )) if "positional_matrices" in r else 0.0
        
        candidatos_auditados.append({
            "combinacion": [int(x) for x in sorted(comb)],
            "sb": int(sb),
            "suma": sum(comb),
            "composite": float(composite),
            "score_jax": float(score),
            "score_gauss": float(score_gauss),
            "score_entropy": float(score_entropy),
            "score_bayes": float(score_bayes),
            "score_hazard": float(score_hazard),
            "prob_m": prob_m,
            "prob_pos": prob_pos,
            "audit": audit_info,
            "es_optimo": composite >= 70.0,
            "tiene_adn": score >= score_meta
        })
    
    # 1. Estrategia A: ADN Ganador & Score Compuesto Top
    candidatos_adn = [c for c in candidatos_auditados if c["tiene_adn"] and c["es_optimo"]]
    if not candidatos_adn:
        candidatos_adn = [c for c in candidatos_auditados if c["es_optimo"]]
    if not candidatos_adn:
        candidatos_adn = candidatos_auditados
        
    candidatos_adn.sort(key=lambda x: x["composite"], reverse=True)
    jugada_adn = candidatos_adn[0] if candidatos_adn else None
    
    # 2. Estrategia B: Entropía y Balance Gaussiano Puro
    candidatos_entropia = sorted(
        [c for c in candidatos_auditados if c != jugada_adn and (jugada_adn is None or c["sb"] != jugada_adn["sb"])],
        key=lambda x: (x["score_entropy"] * 0.45 + x["score_gauss"] * 0.45 + x["composite"] * 0.01),
        reverse=True
    )
    jugada_entropia = candidatos_entropia[0] if candidatos_entropia else (candidatos_auditados[1] if len(candidatos_auditados) > 1 else None)
    
    # 3. Estrategia C: Rotación por Atraso (Hazard Rate)
    usadas_sb = {j["sb"] for j in [jugada_adn, jugada_entropia] if j}
    candidatos_hazard = sorted(
        [c for c in candidatos_auditados if c not in (jugada_adn, jugada_entropia) and c["sb"] not in usadas_sb],
        key=lambda x: (x["score_hazard"] * 0.7 + x["composite"] * 0.01),
        reverse=True
    )
    if not candidatos_hazard:
        candidatos_hazard = sorted(
            [c for c in candidatos_auditados if c not in (jugada_adn, jugada_entropia)],
            key=lambda x: x["score_hazard"],
            reverse=True
        )
    jugada_hazard = candidatos_hazard[0] if candidatos_hazard else (candidatos_auditados[2] if len(candidatos_auditados) > 2 else None)
    
    seleccion = []
    if jugada_adn:
        jugada_adn["estrategia"] = "ADN Ganador & Score Top"
        seleccion.append(jugada_adn)
    if jugada_entropia:
        jugada_entropia["estrategia"] = "Dispersión & Entropía Equilibrada"
        seleccion.append(jugada_entropia)
    if jugada_hazard:
        jugada_hazard["estrategia"] = "Rotación Atraso & Presión Hazard"
        seleccion.append(jugada_hazard)
        
    for j in seleccion:
        j["veredicto"] = gb.obtener_veredicto_cualitativo(
            j["combinacion"], j["sb"], j["composite"], j["score_jax"],
            j["score_gauss"], j["score_entropy"], j["score_bayes"],
            j["score_hazard"], score_mediana
        )
        
    return {
        "sorteo": sorteo_nombre,
        "score_meta": round(score_meta, 4),
        "ultimo_sorteo": [int(x) for x in ultimo_sorteo],
        "ultima_sb": int(ultima_sb),
        "total_candidatos_generados": len(candidatos_brutos),
        "total_auditados_validos": len(candidatos_auditados),
        "portafolio": seleccion
    }

def main():
    json_path = os.path.join(PROJECT_ROOT, gb.FILE_PATH)
    with open(json_path, "r", encoding="utf-8") as f:
        data_json = json.load(f)
        
    resultados = {
        "Baloto": refinar_sorteo("Baloto", data_json),
        "Revancha": refinar_sorteo("Revancha", data_json)
    }
    
    print(json.dumps(resultados, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
