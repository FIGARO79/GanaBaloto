"""Carga de datos históricos e información del sorteo objetivo."""

import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta

from .config import RUTA_JSON, PROJECT_ROOT  # noqa: F401  (garantiza sys.path)

import ganabaloto as gb

DIAS_JUEGO = {0, 2, 5}  # Lunes, Miércoles, Sábado


def cargar_datos(ruta=RUTA_JSON):
    """Lee baloto.json; termina con error claro si no existe."""
    if not os.path.exists(ruta):
        print(f"Error: No se encontró {ruta}", file=sys.stderr)
        sys.exit(1)
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def contar_dias_sorteo(fecha_inicio, fecha_fin):
    """Cuenta sorteos oficiales entre dos fechas (Lunes=0, Miércoles=2, Sábado=5)."""
    actual = fecha_inicio + timedelta(days=1)
    sorteos = 0
    while actual <= fecha_fin:
        if actual.weekday() in DIAS_JUEGO:
            sorteos += 1
        actual += timedelta(days=1)
    return sorteos


def botes_de(data_json, nombre):
    """Registros donde cayó el premio mayor 5+1."""
    return [s for s in data_json.get(nombre, []) if (s.get("Premios 5+1") or 0) > 0 and s.get("B5")]


def extraer_botes_ganadores(data_json, sorteo_nombre):
    """Devuelve lista de (balotas, sb) de los sorteos donde cayó el premio mayor 5+1."""
    return [
        ([int(s[f"B{i}"]) for i in range(1, 6)], int(s["SB"]))
        for s in botes_de(data_json, sorteo_nombre)
    ]


def top_balotas_botes(data_json, nombre, k=10):
    """Las k balotas más frecuentes en los botes 5+1 reales (calculadas, no fijas)."""
    c = Counter(int(s[f"B{i}"]) for s in botes_de(data_json, nombre) for i in range(1, 6))
    return [n for n, _ in c.most_common(k)]


def top_sb_botes(data_json, nombre, k=4):
    """Las k Super Balotas más frecuentes en los botes 5+1 reales."""
    c = Counter(int(s["SB"]) for s in botes_de(data_json, nombre))
    return [n for n, _ in c.most_common(k)]


def obtener_info_sorteo(data_json, fecha_str=None):
    """Calcula la información del sorteo objetivo: número, fecha, anclajes y pivotes."""
    ultimo_registro = data_json["Baloto"][-1]
    f_base = datetime.strptime(ultimo_registro["Fecha"], "%Y-%m-%d")
    num_base = int(ultimo_registro.get("Sorteo", 2717))

    if fecha_str:
        dt = datetime.strptime(fecha_str, "%Y-%m-%d")
    else:
        dt = datetime.now()
        # Si la fecha actual ya se jugó o no es día de sorteo oficial, avanzar al próximo sorteo
        if dt.strftime("%Y-%m-%d") <= ultimo_registro["Fecha"] or dt.weekday() not in DIAS_JUEGO:
            cand = dt + timedelta(days=1)
            while cand.weekday() not in DIAS_JUEGO or cand.strftime("%Y-%m-%d") <= ultimo_registro["Fecha"]:
                cand += timedelta(days=1)
            dt = cand

    diff = contar_dias_sorteo(f_base, dt)
    num_sorteo = num_base + diff

    dia = dt.day
    mes = dt.month
    suma_sorteo = sum(int(c) for c in str(num_sorteo))
    suma_dia_mes = dia + mes

    dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses_nombres = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    ]
    fecha_legible = f"{dias_nombres[dt.weekday()]}, {dia:02d} de {meses_nombres[mes - 1]} de {dt.year}"

    # Resonancia Cíclica Lag-8 (sorteo oficial de hace 8 sorteos)
    lag_8_data = {}
    for s_nombre in ["Baloto", "Revancha"]:
        arr = data_json.get(s_nombre, [])
        if len(arr) >= 8:
            row_lag = arr[-8]
            lag_8_data[s_nombre] = {
                "sorteo": row_lag.get("Sorteo"),
                "fecha": row_lag.get("Fecha"),
                "balotas": [int(row_lag[f"B{i}"]) for i in range(1, 6)],
                "sb": int(row_lag.get("SB")),
            }
        else:
            lag_8_data[s_nombre] = {"sorteo": None, "fecha": None, "balotas": [], "sb": None}

    return {
        "fecha": dt.strftime("%Y-%m-%d"),
        "fecha_legible": fecha_legible,
        "dia": dia,
        "mes": mes,
        "anio": dt.year,
        "num_sorteo": num_sorteo,
        "suma_sorteo": suma_sorteo,
        "suma_dia_mes": suma_dia_mes,
        "anclajes_principales": [x for x in [dia, mes, suma_sorteo, suma_dia_mes] if 1 <= x <= gb.N_MAIN_BALLS],
        "pivotes_botes": {n: top_balotas_botes(data_json, n) for n in ("Baloto", "Revancha")},
        "sbs_reinas": {n: top_sb_botes(data_json, n) for n in ("Baloto", "Revancha")},
        "lag_8_data": lag_8_data,
    }
