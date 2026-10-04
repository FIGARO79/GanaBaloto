#!/usr/bin/env python3
"""Backtest walk-forward de CADA componente del indice compuesto (sin fuga de datos).

Uso:
  ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/backtest_componentes.py [Baloto|Revancha] [--n-tests 60] [--pool 200]

Para cada sorteo de prueba t: se recalcula el motor SOLO con sorteos < t y se puntua la
combinacion real de t junto con `pool` combinaciones aleatorias. Se guarda el percentil
de la real dentro del pool para cada componente. Bajo el azar el percentil medio es 50.
Un componente "aporta" solo si el IC95% (bootstrap) excluye 50 hacia arriba.
Se aplica Bonferroni implicito: el veredicto exige que el limite inferior del IC al
nivel 1 - 0.05/k (k = componentes) sea > 50.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
sys.path.insert(0, str(RAIZ))
spec = importlib.util.spec_from_file_location("epc", AQUI / "ejecutar_pronostico_completo.py")
epc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(epc)
gb, jax = epc.gb, epc.jax

ap = argparse.ArgumentParser()
ap.add_argument("juego", nargs="?", default="Baloto")
ap.add_argument("--n-tests", type=int, default=60)
ap.add_argument("--pool", type=int, default=200)
ap.add_argument("--ventana", type=int, default=500, help="ultimos N sorteos de donde tomar los de prueba")
ap.add_argument("--seed", type=int, default=42)
a = ap.parse_args()
rng = np.random.default_rng(a.seed)

datos = [s for s in json.load(open(RAIZ / "baloto.json"))[a.juego] if s.get("B5")]
n = len(datos)
tests = np.linspace(n - a.ventana, n - 1, a.n_tests).astype(int)
NOMBRES = ["Frecuencia (JAX)", "Gauss (suma)", "Entropia", "Bayes", "Hazard", "Ising", "Markov (orden 1)",
           "Markov posicional", "Compuesto"]
percentiles = {k: [] for k in NOMBRES}


def rand_comb():
    return sorted(rng.choice(np.arange(1, 44), 5, replace=False).tolist()), int(rng.integers(1, 17))


def puntuar(comb, sb, r):
    comb, sb, score, comp, gauss, ent, bayes, haz, ising = epc.evaluar_jugada_directa(comb, sb, r)
    pm = float(gb.calculate_sequence_probability(comb, r["df_transition_matrix"]))
    pp = 0.0
    if "positional_matrices" in r:
        pp = float(gb.calculate_positional_markov_probability(
            comb, sb, r["positional_matrices"], r["last_combination"], r["last_sb"]))
    return [score, gauss, ent, bayes, haz, ising, pm, pp, comp]


for idx, t in enumerate(tests, 1):
    r = gb.analizar_sorteo(a.juego, pd.DataFrame(datos[:t]))
    real = puntuar(sorted(int(datos[t][f"B{i}"]) for i in range(1, 6)), int(datos[t]["SB"]), r)
    pool = np.array([puntuar(*rand_comb(), r) for _ in range(a.pool)])
    for j, nom in enumerate(NOMBRES):
        pct = 100.0 * (np.sum(pool[:, j] < real[j]) + 0.5 * np.sum(pool[:, j] == real[j])) / a.pool
        percentiles[nom].append(pct)
    if idx % 10 == 0:
        print(f"  ... {idx}/{len(tests)} sorteos evaluados", file=sys.stderr)

k = len(NOMBRES)
alfa = 0.05 / k
print(f"\nJuego: {a.juego} | sorteos de prueba: {len(tests)} | pool por sorteo: {a.pool}")
print("Percentil medio de la combinacion REAL (azar = 50). Veredicto con correccion de Bonferroni.\n")
print(f"{'Componente':<20}{'Media':>8}{'IC (1-0.05/k)':>22}  Veredicto")
for nom in NOMBRES:
    x = np.array(percentiles[nom])
    boot = np.array([rng.choice(x, len(x)).mean() for _ in range(3000)])
    lo, hi = np.percentile(boot, 100 * alfa / 2), np.percentile(boot, 100 * (1 - alfa / 2))
    ver = "APORTA" if lo > 50 else ("PERJUDICA" if hi < 50 else "sin evidencia")
    print(f"{nom:<20}{x.mean():>8.2f}{f'[{lo:.1f}, {hi:.1f}]':>22}  {ver}")
print("\nSi ningun componente APORTA, el indice compuesto no distingue la combinacion real de una aleatoria.")
