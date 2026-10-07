"""Salida del pronóstico: reporte Markdown estandarizado y JSON."""

import json

import jax


def _fmt(nums):
    return "-".join(f"{x:02d}" for x in nums)


def insignias_de(j, i):
    ins = []
    if i == 1:
        ins.append("**Top #1**")
    if j.es_optimo:
        ins.append("**Perfil Óptimo**" if i > 1 and not j.tiene_adn else "**Óptimo**")
    if j.tiene_adn:
        ins.append("**ADN**")
    if j.coinc_fecha:
        ins.append("**Fecha**")
    if j.coinc_lag8:
        ins.append("**Lag-8**")
    if j.es_espejo:
        ins.append("**Espejo**")
    if j.tiene_salto:
        ins.append("**Delta**")
    if j.tiene_ising:
        ins.append("**Ising**")
    return " ".join(ins)


def imprimir_tabla(titulo, res):
    """Sección con la tabla del Top de un sorteo (Baloto o Revancha)."""
    print(titulo)
    print(f"* **Meta histórica de ganadores (Score JAX):** $\\ge {res.score_meta:.4f}$")
    print(r"* **Criterio de Perfil Óptimo:** Índice Compuesto $\ge 70.0$" + "\n")
    print("| # | Combinación | Suma | Índice | Ajustado | Similitud | Popul. | JAX | Gauss | Entropía | Bayes | Hazard | Insignias |")
    print("|---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|")
    for i, j in enumerate(res.jugadas, 1):
        comb_str = f"**`{_fmt(j.comb)}`** + **`[{j.sb:02d}]`**"
        print(f"| **{i}** | {comb_str} | {j.suma} | **{j.indice:.1f}** | **{j.indice_ajustado:.1f}** | {j.similitud:.0f} | {j.popularidad:.0f} | {j.jax:.4f} | {j.gauss:.2f} | {j.entropia:.2f} | {j.bayes:.2f} | {j.hazard:.2f} | {insignias_de(j, i)} |")
    print()


def imprimir_cabecera(info_sorteo, res_baloto, res_revancha):
    dev = jax.devices()[0]
    print(f"Motor estocástico multimodal: JAX ({dev.platform.upper()} detectada: {getattr(dev, 'device_kind', dev)})")
    print(f"Base de datos histórica: baloto.json ({res_baloto.total_sorteos} sorteos de Baloto, {res_revancha.total_sorteos} sorteos de Revancha)")
    print(f"Sorteo Objetivo: {info_sorteo['fecha_legible']} (Sorteo Oficial #{info_sorteo['num_sorteo']})")
    reg_b = res_baloto.regime_info
    reg_r = res_revancha.regime_info
    reg_b_name = reg_b.get("current_regime", "Equilibrio Central")
    reg_r_name = reg_r.get("current_regime", "Equilibrio Central")
    print(f"Régimen Dinámico (HMM): Baloto en '{reg_b_name}' (P_persistencia={reg_b.get('transition_prob', 0):.2f}) | Revancha en '{reg_r_name}'")
    lag_b = info_sorteo["lag_8_data"]["Baloto"]
    lag_b_str = ", ".join(f"{x:02d}" for x in lag_b["balotas"]) if lag_b["balotas"] else "N/A"
    print(f"Anclajes de Fecha: Día {info_sorteo['dia']:02d} | Mes {info_sorteo['mes']:02d} | Suma Sorteo {info_sorteo['suma_sorteo']:02d} | Suma Día+Mes: {info_sorteo['suma_dia_mes']:02d}")
    print(f"Resonancia Cíclica Lag-8 (Sorteo #{lag_b.get('sorteo')}): Balotas [{lag_b_str}] | SB [{lag_b.get('sb', 0):02d}]")
    pb = ", ".join(f"{x:02d}" for x in info_sorteo["pivotes_botes"]["Baloto"][:6])
    sbr = ", ".join(f"{x:02d}" for x in info_sorteo["sbs_reinas"]["Baloto"])
    print(f"Pivotes Históricos de Botes (calculados): {pb} | SB Reinas: {sbr}\n")


def imprimir_leyenda(cfg):
    print("> **Leyenda de Insignias:**")
    print("> * **Top #1:** Mayor Índice Ajustado del sorteo.")
    if cfg.peso_pop > 0:
        print(f"> * **Ajustado:** Índice + {cfg.peso_sim:.2f}×Similitud − {cfg.peso_pop:.2f}×Popularidad (criterio de orden final).")
        print("> * **Popul. (0-100):** Probabilidad de compartir premio (todo ≤31, consecutivos, progresión, números de suerte). Menor es mejor.")
    else:
        print(f"> * **Ajustado:** Índice + {cfg.peso_sim:.2f}×Similitud (criterio de orden final enfocado en maximizar aciertos).")
        print("> * **Popul. (0-100):** Grado de concurrencia pública en fechas ≤31 (informativo, sin penalizar jugadas para priorizar aciertos).")
    print(r"> * **Perfil Óptimo:** Calificación $\ge 70.0/100$ en la escala global multidimensional.")
    print("> * **ADN Ganador:** Supera el umbral promedio histórico de combinaciones ganadoras del premio mayor.")
    print("> * **Fecha:** Integra anclajes de calendario (día, mes o suma de dígitos del sorteo).")
    print("> * **Lag-8:** Resonancia con el sorteo de hace 8 fechas (patrón cíclico observado en botes millonarios).")
    print("> * **Espejo:** Coincidencia de número principal con la Super Balota (como en el bote #2717 de $61.600M).")
    print("> * **Delta:** Saltos aritméticos simétricos de $+4$ o $+6$ observados en los botes ganadores.")
    print("> * **Ising:** Co-ocurrencia por acoplamiento mutuo de pares ($J_{ij}$ estadísticamente significativo).\n")


def imprimir_auditoria_top(nombre, top, audit):
    print(f"#### Top #1 {nombre}: `{_fmt(top.comb)}` + `[{top.sb:02d}]` (Índice: {top.indice:.1f})")
    for clave in ("desc_suma", "desc_entr", "desc_jax", "desc_sb", "desc_anclaje", "desc_haz"):
        print(f"* **{audit[clave]}**")
    print(f"* **{audit['desc_ising']}**\n")


def imprimir_rueda(rueda):
    nums_str = ", ".join(f"{x:02d}" for x in rueda["numeros_pool"])
    sbs_str = " y ".join(f"`[{x:02d}]`" for x in rueda["super_balotas"])
    print("### 4. Estrategia Avanzada: Rueda Combinatoria Reducida (Wheeling System)")
    print(f"Selección de {len(rueda['numeros_pool'])} números clave sincronizados (`{nums_str}`) cruzados con las Super Balotas líderes ({sbs_str}), con **garantía matemática de {rueda['garantia']} aciertos**:\n")
    for i, t in enumerate(rueda["tiquetes"], 1):
        c_str = " - ".join(f"{x:02d}" for x in t["comb"])
        print(f"* **Tiquete {i:02d}:** `{c_str}` + SB `[{t['sb']:02d}]`")
    print(f"\n*(Con solo {rueda['total_tiquetes']} apuestas se cubren matemáticamente {rueda['garantia']} aciertos si {rueda['garantia']} o más de los 7 números seleccionados salen sorteados).*")


def imprimir_reporte(info_sorteo, res_baloto, res_revancha, audit_b, audit_r, rueda, cfg):
    imprimir_cabecera(info_sorteo, res_baloto, res_revancha)
    imprimir_tabla("### 1. Pronósticos Recomendados: Baloto", res_baloto)
    imprimir_tabla("### 2. Pronósticos Recomendados: Revancha", res_revancha)
    imprimir_leyenda(cfg)
    print("### 3. Auditoría Detallada de las Jugadas Estrella\n")
    imprimir_auditoria_top("Baloto", res_baloto.jugadas[0], audit_b)
    imprimir_auditoria_top("Revancha", res_revancha.jugadas[0], audit_r)
    imprimir_rueda(rueda)


def imprimir_json(info_sorteo, res_baloto, res_revancha, audit_b, audit_r, rueda):
    salida = {
        "sorteo_info": info_sorteo,
        "baloto": res_baloto.to_dict(),
        "revancha": res_revancha.to_dict(),
        "auditoria_top1": {"baloto": audit_b, "revancha": audit_r},
        "rueda_reducida": rueda,
    }
    print(json.dumps(salida, indent=2, ensure_ascii=False))
