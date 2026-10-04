#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI para generar el Pronóstico Completo Estandarizado de GanaBaloto:
Incorpora el análisis de botes históricos, deltas simétricos y sincronización con el calendario:
1. Top 5 Baloto (Métricas, Insignias)
2. Top 5 Revancha (Métricas, Insignias)
3. Auditoría detallada de las jugadas #1 (incluye análisis de anclajes de fecha y botes)
4. Rueda combinatoria reducida optimizada (7 números clave sincronizados, garantía 3 aciertos)

La lógica vive en el paquete `pronostico/` (config, datos, scoring, candidatas, auditoria,
rueda, reporte). Este archivo es solo el punto de entrada y reexporta las funciones usadas
por los scripts de backtesting.
"""

import argparse
import os
import random
import sys

import numpy as np

# Permite `from pronostico import ...` aunque se cargue este archivo por ruta (backtests)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pronostico.config import Config, PROJECT_ROOT  # noqa: E402,F401
import ganabaloto as gb  # noqa: E402,F401
import jax  # noqa: E402,F401
from pronostico.datos import cargar_datos, obtener_info_sorteo  # noqa: E402,F401
from pronostico.scoring import (  # noqa: E402,F401
    evaluar_jugada_directa,
    calcular_similitud_botes,
    calcular_popularidad,
)
from pronostico.candidatas import obtener_mejores_jugadas  # noqa: E402
from pronostico.auditoria import auditoria_cualitativa  # noqa: E402
from pronostico.rueda import construir_rueda_optima  # noqa: E402
from pronostico.reporte import imprimir_reporte, imprimir_json  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(
        description="Genera el reporte estandarizado de pronóstico completo para Baloto y Revancha con seguimiento de fechas y botes."
    )
    parser.add_argument("--json", action="store_true", help="Salida estructurada en JSON en lugar de Markdown.")
    parser.add_argument(
        "--fecha", type=str, default=None,
        help="Fecha objetivo del sorteo en formato YYYY-MM-DD (por defecto hoy o próximo sorteo).",
    )
    parser.add_argument("--peso-sim", type=float, default=Config.peso_sim,
                        help="Peso (0-1) de la Similitud con botes ganadores en el ranking final.")
    parser.add_argument("--peso-pop", type=float, default=Config.peso_pop,
                        help="Peso (0-1) de la penalización por Popularidad en el ranking final.")
    parser.add_argument("--seed", type=int, default=None, help="Semilla para resultados reproducibles.")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)
    cfg = Config(peso_sim=args.peso_sim, peso_pop=args.peso_pop)

    data_json = cargar_datos()
    info_sorteo = obtener_info_sorteo(data_json, args.fecha)

    res_baloto = obtener_mejores_jugadas("Baloto", data_json, info_sorteo, cfg)
    res_revancha = obtener_mejores_jugadas("Revancha", data_json, info_sorteo, cfg)
    rueda = construir_rueda_optima(data_json, info_sorteo)

    audit_b = auditoria_cualitativa(res_baloto.jugadas[0], res_baloto, info_sorteo)
    audit_r = auditoria_cualitativa(res_revancha.jugadas[0], res_revancha, info_sorteo)

    if args.json:
        imprimir_json(info_sorteo, res_baloto, res_revancha, audit_b, audit_r, rueda)
    else:
        imprimir_reporte(info_sorteo, res_baloto, res_revancha, audit_b, audit_r, rueda, cfg)


if __name__ == "__main__":
    main()
