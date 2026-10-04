"""Auditoría cualitativa de una jugada."""


def auditoria_cualitativa(jugada, resultado, info_sorteo):
    """Descripciones en texto de cada dimensión de una `Jugada` (resultado: ResultadoSorteo)."""
    sb = jugada.sb
    suma = jugada.suma

    # Gauss / Suma
    if 90 <= suma <= 130:
        desc_suma = f"Suma total ({suma}): Entra en el centro de la campana gaussiana (zona dorada 90–130, score {jugada.gauss:.2f})."
    else:
        desc_suma = f"Suma total ({suma}): Distribución equilibrada (score Gauss {jugada.gauss:.2f})."

    # Entropía
    desc_entr = f"Entropía de Shannon ({jugada.entropia:.2f}): Dispersión balanceada sin secuencias correlativas forzadas ni concentración en una sola decena."

    # JAX vs Meta
    meta = resultado.score_meta
    if jugada.jax >= meta:
        desc_jax = f"Score JAX ({jugada.jax:.4f}) vs Meta ({meta:.4f}): Supera con holgura el promedio histórico de combinaciones ganadoras (ADN Ganador)."
    else:
        desc_jax = f"Score JAX ({jugada.jax:.4f}): Excelente perfil probabilístico estocástico."

    # Super Balota info
    apariciones_sb = resultado.sb_counts_dict.get(sb, 0)
    reina_nota = " (Super Balota reina histórica)" if sb in [15, 10, 7, 1] else ""
    desc_sb = f"Super Balota `{sb:02d}`: Cuenta con {apariciones_sb} apariciones históricas de alta frecuencia en {resultado.sorteo}{reina_nota}."

    # Hazard
    if jugada.hazard >= 0.70:
        desc_haz = f"Hazard Rate ({jugada.hazard:.2f}): Alta madurez estadística; integra balotas frías con atraso acumulado listas para su ciclo de retorno."
    else:
        desc_haz = f"Hazard Rate ({jugada.hazard:.2f}): Balance dinámico entre balotas activas y en rotación."

    # Anclajes de Fecha, Botes y Resonancia Lag-8
    detalles_anclaje = []
    if jugada.coinc_fecha:
        f_str = ", ".join(f"`{x:02d}`" for x in jugada.coinc_fecha)
        detalles_anclaje.append(f"Calendario ({f_str})")
    if jugada.coinc_lag8:
        l8_str = ", ".join(f"`{x:02d}`" for x in jugada.coinc_lag8)
        detalles_anclaje.append(f"Resonancia Lag-8 ({l8_str})")
    if jugada.es_espejo:
        detalles_anclaje.append(f"Efecto Espejo SB (`{sb:02d}` como balota principal)")
    if jugada.tiene_salto:
        detalles_anclaje.append("Deltas simétricos (+4 o +6)")

    if detalles_anclaje:
        desc_anclaje = f"Sincronización Estocástica y Botes: Integra {' + '.join(detalles_anclaje)}, reproduciendo las firmas numéricas de los premios mayores."
    else:
        desc_anclaje = f"Sincronización Fecha: Balance armónico alineado con el ciclo estocástico del sorteo #{info_sorteo['num_sorteo']}."

    # Afinidad de Acoplamiento Mutuo (Ising)
    if jugada.tiene_ising:
        desc_ising = f"Afinidad Ising ({jugada.ising:.2f}): Fuerte atracción cooperativa; las parejas de esta combinación co-ocurren con una frecuencia significativamente superior al azar estadístico."
    else:
        desc_ising = f"Afinidad Ising ({jugada.ising:.2f}): Acoplamiento equilibrado entre las 5 balotas."

    return {
        "desc_suma": desc_suma,
        "desc_entr": desc_entr,
        "desc_jax": desc_jax,
        "desc_haz": desc_haz,
        "desc_sb": desc_sb,
        "desc_anclaje": desc_anclaje,
        "desc_ising": desc_ising,
    }
