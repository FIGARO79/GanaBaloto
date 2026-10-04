"""Generación, ranking y selección diversa de jugadas candidatas."""

import itertools
import random

import pandas as pd

from . import config  # noqa: F401  (garantiza sys.path)
import ganabaloto as gb

from .config import Config
from .datos import extraer_botes_ganadores
from .modelos import Jugada, ResultadoSorteo
from .scoring import evaluar_jugada_directa, calcular_similitud_botes, calcular_popularidad


def generar_candidatas_ancladas(r, info_sorteo, sorteo_nombre, n_generar=100):
    """Genera combinaciones candidatas que integran anclajes de fecha, pivotes de botes y resonancia Lag-8."""
    anclajes = info_sorteo["anclajes_principales"]
    pivotes = info_sorteo["pivotes_botes"].get(sorteo_nombre, [8, 4])
    sbs = list(info_sorteo["sbs_reinas"].get(sorteo_nombre, [15, 10]))
    lag_8_info = info_sorteo.get("lag_8_data", {}).get(sorteo_nombre, {})
    balotas_lag_8 = lag_8_info.get("balotas", [])
    sb_lag_8 = lag_8_info.get("sb")
    if sb_lag_8 and sb_lag_8 not in sbs:
        sbs.append(sb_lag_8)

    # Núcleos de 2 elementos cruzando anclajes de calendario, pivotes de bote y resonancia cíclica
    pool_nucleos = list(set(anclajes + pivotes + balotas_lag_8))
    nucleos = list(itertools.combinations(pool_nucleos, 2))
    random.shuffle(nucleos)

    candidatas = []
    intentos = 0
    max_intentos = n_generar * 25

    for nuc in itertools.cycle(nucleos):
        if len(candidatas) >= n_generar or intentos >= max_intentos:
            break
        intentos += 1
        sb = random.choice(sbs)

        restantes = [x for x in range(1, gb.N_MAIN_BALLS + 1) if x not in nuc]
        trio = []

        # Salto aritmético +4 o +6 (firma observada en botes ganadores)
        if random.random() < 0.35 and restantes:
            base_n = random.choice(nuc)
            salto = random.choice([4, 6])
            candidato_salto = base_n + salto if base_n + salto <= gb.N_MAIN_BALLS else base_n - salto
            if 1 <= candidato_salto <= gb.N_MAIN_BALLS and candidato_salto not in nuc and candidato_salto in restantes:
                trio.append(candidato_salto)
                restantes.remove(candidato_salto)

        # Efecto Espejo Bote (SB coincide con balota principal)
        if sb <= gb.N_MAIN_BALLS and random.random() < 0.25 and sb not in nuc and sb in restantes and len(trio) < 3:
            trio.append(sb)
            restantes.remove(sb)

        # Completar hasta 3 números
        faltan = 3 - len(trio)
        if faltan > 0 and len(restantes) >= faltan:
            trio.extend(random.sample(restantes, faltan))

        comb = sorted(list(nuc) + trio)
        # Rango de suma calibrado para régimen de botes (75 a 125)
        if 75 <= sum(comb) <= 125:
            item = evaluar_jugada_directa(comb, sb, r)
            if item[3] >= 65.0:  # Índice compuesto viable
                candidatas.append(item)

    return candidatas


def seleccion_diversa(candidatas, n_top, max_solape):
    """Selección voraz: máx. `max_solape` balotas compartidas entre jugadas elegidas.

    Devuelve las candidatas reordenadas: primero las diversas; el resto completa sin restricción.
    """
    diversas, resto = [], []
    for it in candidatas:
        if len(diversas) < n_top and all(len(set(it[0]) & set(d[0])) <= max_solape for d in diversas):
            diversas.append(it)
        else:
            resto.append(it)
    return diversas + resto


def obtener_mejores_jugadas(sorteo_nombre, data_json, info_sorteo, cfg=None):
    cfg = cfg or Config()
    df = pd.DataFrame(data_json[sorteo_nombre])
    r = gb.analizar_sorteo(sorteo_nombre, df)
    weights = gb.get_number_weights(r, gb.N_MAIN_BALLS, gb.N_SUPER_BALOTA)
    df_ganadores = gb.analizar_ganadores_historicos(r)
    score_meta = (
        float(df_ganadores["Score JAX"].mean())
        if not df_ganadores.empty
        else 0.1450
    )

    # 1. Candidatas estocásticas puras
    candidatas_puras = gb.generate_probable_combinations(cfg.n_pool, r, weights)

    # 2. Candidatas con anclajes de fecha, botes y resonancia Lag-8
    candidatas_ancladas = generar_candidatas_ancladas(r, info_sorteo, sorteo_nombre, n_generar=100)

    # 3. Unificar y ordenar por Índice Ajustado = Compuesto + w_sim*Similitud - w_pop*Popularidad
    botes_hist = extraer_botes_ganadores(data_json, sorteo_nombre)
    todas_candidatas = candidatas_puras + candidatas_ancladas
    sim_cache = {}

    def _extras(item):
        clave = (tuple(sorted(int(x) for x in item[0])), int(item[1]))
        if clave not in sim_cache:
            sim_cache[clave] = (
                calcular_similitud_botes(clave[0], clave[1], botes_hist),
                calcular_popularidad(clave[0], clave[1]),
            )
        return sim_cache[clave]

    def _clave_orden(item):
        sim, pop = _extras(item)
        return item[3] + cfg.peso_sim * sim - cfg.peso_pop * pop

    todas_candidatas.sort(key=_clave_orden, reverse=True)

    anclajes_fecha = set(info_sorteo["anclajes_principales"])
    pivotes_bote = set(info_sorteo["pivotes_botes"].get(sorteo_nombre, []))
    lag_8_info = info_sorteo.get("lag_8_data", {}).get(sorteo_nombre, {})
    balotas_lag_8 = set(lag_8_info.get("balotas", []))

    todas_candidatas = seleccion_diversa(todas_candidatas, cfg.n_top, cfg.max_solape)

    seleccionadas = []
    for item in todas_candidatas:
        comb, sb, score, composite, score_gauss, score_entropy, score_bayes, score_hazard = item[:8]
        score_ising = item[8] if len(item) > 8 else float(gb.calculate_ising_energy_score(comb, r.get("ising_matrix")))
        # Evitar duplicados exactos
        if any(set(comb) == set(s.comb) and sb == s.sb for s in seleccionadas):
            continue
        similitud, popularidad = _extras(item)

        # Detectar coincidencias específicas
        coinc_fecha = [x for x in comb if x in anclajes_fecha]
        coinc_pivote = [x for x in comb if x in pivotes_bote]
        coinc_lag8 = [x for x in comb if x in balotas_lag_8]
        es_espejo = (sb in comb)

        seleccionadas.append(Jugada(
            comb=[int(x) for x in comb],
            sb=int(sb),
            suma=int(sum(comb)),
            indice=round(float(composite), 1),
            similitud=similitud,
            popularidad=popularidad,
            indice_ajustado=round(float(composite) + cfg.peso_sim * similitud - cfg.peso_pop * popularidad, 1),
            jax=round(float(score), 4),
            gauss=round(float(score_gauss), 2),
            entropia=round(float(score_entropy), 2),
            bayes=round(float(score_bayes), 2),
            hazard=round(float(score_hazard), 2),
            ising=round(float(score_ising), 2),
            es_optimo=composite >= 70.0,
            tiene_adn=score >= score_meta,
            tiene_anclaje=(
                len(coinc_fecha) >= 1 or len(coinc_lag8) >= 1 or es_espejo or len(coinc_pivote) >= 2
            ),
            coinc_fecha=coinc_fecha,
            coinc_lag8=coinc_lag8,
            es_espejo=es_espejo,
            tiene_salto=any(comb[k + 1] - comb[k] in (4, 6) for k in range(len(comb) - 1)),
            tiene_ising=score_ising >= 0.52,
        ))
        if len(seleccionadas) == cfg.n_top:
            break

    return ResultadoSorteo(
        sorteo=sorteo_nombre,
        score_meta=round(score_meta, 4),
        total_sorteos=len(df),
        ultimo_sorteo=r.get("last_combination", []),
        ultima_sb=r.get("last_sb", 0),
        df_gap_analysis=r.get("df_gap_analysis", pd.DataFrame()),
        main_counts_dict=r.get("main_counts_dict", {}),
        sb_counts_dict=r.get("sb_counts_dict", {}),
        regime_info=r.get("regime_info", {}),
        jugadas=seleccionadas,
    )
