#!/usr/bin/env python3
"""Backtesting walk-forward SIN fuga de datos de Similitud y Popularidad.

Uso:
  ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/backtest_ajustado.py [Baloto|Revancha] [--n-pool 500] [--seed 42]

Dos pruebas, ambas usando solo informacion anterior a cada sorteo evaluado:

A) Percentil de la combinacion REAL: para cada sorteo t (con >= 8 botes previos),
   se calcula la Similitud (con botes < t) de la combinacion que salio y se compara contra
   n_pool combinaciones aleatorias. Bajo el azar el percentil medio es 50 %.
   Se reporta para BOTES (premio mayor) y para el RESTO de sorteos (control).

B) Aciertos del Top-5 de un pool aleatorio rankeado por Ajustado (sim/pop) vs 5 al azar.
   Esperado por azar: 25/43 = 0.581 aciertos por combinacion.

Limitacion: solo evalua Similitud y Popularidad (rapidas). El indice compuesto completo
(JAX/Markov/...) requiere recalcular el motor por sorteo y no esta incluido.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
sys.path.insert(0, str(RAIZ))

# Importa las funciones de scoring del script principal sin ejecutarlo
spec = importlib.util.spec_from_file_location("epc", AQUI / "ejecutar_pronostico_completo.py")
epc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(epc)

ap = argparse.ArgumentParser()
ap.add_argument("juego", nargs="?", default="Baloto")
ap.add_argument("--n-pool", type=int, default=500)
ap.add_argument("--max-sorteos", type=int, default=400, help="ultimos N sorteos a evaluar")
ap.add_argument("--peso-sim", type=float, default=0.20)
ap.add_argument("--peso-pop", type=float, default=0.10)
ap.add_argument("--seed", type=int, default=42)
a = ap.parse_args()
rng = np.random.default_rng(a.seed)

datos = [s for s in json.load(open(RAIZ / "baloto.json"))[a.juego] if s.get("B5")]
n = len(datos)
comb_de = lambda s: sorted(int(s[f"B{i}"]) for i in range(1, 6))
es_bote = [(s.get("Premios 5+1") or 0) > 0 for s in datos]
botes_idx = [i for i, b in enumerate(es_bote) if b]

def pool_aleatorio(k):
    return [(sorted(rng.choice(np.arange(1, 44), 5, replace=False).tolist()), int(rng.integers(1, 17))) for _ in range(k)]

inicio = max(n - a.max_sorteos, botes_idx[7] + 1 if len(botes_idx) > 8 else 0)
pct_bote, pct_resto, hits_ajust, hits_azar, hits_sim = [], [], [], [], []

for t in range(inicio, n):
    previos = [(comb_de(datos[i]), int(datos[i]["SB"])) for i in botes_idx if i < t]
    if len(previos) < 8:
        continue
    real, sb_real = comb_de(datos[t]), int(datos[t]["SB"])
    pool = pool_aleatorio(a.n_pool)
    sims = np.array([epc.calcular_similitud_botes(c, s, previos) for c, s in pool])
    pops = np.array([epc.calcular_popularidad(c, s) for c, s in pool])
    sim_real = epc.calcular_similitud_botes(real, sb_real, previos)
    pct = 100.0 * (np.sum(sims < sim_real) + 0.5 * np.sum(sims == sim_real)) / len(sims)
    (pct_bote if es_bote[t] else pct_resto).append(pct)
    # B) Top-5 por ajustado vs 5 al azar vs 5 solo por similitud
    aj = a.peso_sim * sims - a.peso_pop * pops
    for lista, orden in ((hits_ajust, np.argsort(-aj)[:5]), (hits_sim, np.argsort(-sims)[:5]),
                         (hits_azar, rng.choice(len(pool), 5, replace=False))):
        lista.append(np.mean([len(set(pool[j][0]) & set(real)) for j in orden]))

def resumen(x):
    x = np.array(x)
    if len(x) < 2:
        return "n/a"
    boot = [rng.choice(x, len(x)).mean() for _ in range(2000)]
    return f"{x.mean():.2f}  IC95% [{np.percentile(boot, 2.5):.2f}, {np.percentile(boot, 97.5):.2f}]  (n={len(x)})"

print(f"Juego: {a.juego} | sorteos evaluados: {len(hits_azar)} | botes entre ellos: {len(pct_bote)} | pool: {a.n_pool}\n")
print("A) Percentil de Similitud de la combinacion real (azar = 50.00):")
print(f"   BOTES : {resumen(pct_bote)}")
print(f"   RESTO : {resumen(pct_resto)}\n")
print("B) Aciertos medios de balotas por combinacion (azar teorico = 0.581):")
print(f"   Top-5 por Ajustado  : {resumen(hits_ajust)}")
print(f"   Top-5 por Similitud : {resumen(hits_sim)}")
print(f"   5 al azar           : {resumen(hits_azar)}\n")
print("Lectura: hay senal solo si el IC95% excluye el valor del azar (50 / 0.581) de forma consistente.")
