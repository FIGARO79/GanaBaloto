#!/usr/bin/env python3
"""Factibilidad de Cadenas de Markov de orden superior (k = 0..4) con validacion walk-forward.

Uso:
  ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/markov_orden_superior.py [Baloto|Revancha] [--kmax 4] [--prior 20]

Modelo: para cada numero n (1..43) la serie binaria x_t = 1 si n salio en el sorteo t.
Estado de orden k = los ultimos k valores de ESA serie (2^k estados).
  * 'pooled'    : tabla de transicion compartida por los 43 numeros (mas datos por estado).
  * 'por numero': una tabla por numero (mas flexible, mucho mas ruidosa).
P(x_t=1 | estado) = (c1 + prior * p0) / (c + prior), con p0 = 5/43 (encogimiento al azar).

Evaluacion: log-loss (cross-entropy) fuera de muestra, expandiendo la ventana, frente al
modelo nulo constante p0=5/43. Delta = loss_nulo - loss_modelo (>0 => el Markov ayuda).
IC95% por bootstrap sobre sorteos. Si el IC incluye 0, no hay evidencia de memoria.
"""
import argparse
import json
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
ap = argparse.ArgumentParser()
ap.add_argument("juego", nargs="?", default="Baloto")
ap.add_argument("--kmax", type=int, default=4)
ap.add_argument("--prior", type=float, default=20.0)
ap.add_argument("--calentamiento", type=int, default=300, help="sorteos iniciales solo para entrenar")
ap.add_argument("--seed", type=int, default=42)
a = ap.parse_args()
rng = np.random.default_rng(a.seed)

datos = [s for s in json.load(open(RAIZ / "baloto.json"))[a.juego] if s.get("B5")]
T, N = len(datos), 43
X = np.zeros((T, N), dtype=np.int8)
for t, s in enumerate(datos):
    for i in range(1, 6):
        X[t, int(s[f"B{i}"]) - 1] = 1
P0 = 5.0 / N


def codigo_estado(X, t, k):
    """Estado (entero 0..2^k-1) de cada numero a partir de los k sorteos previos a t."""
    if k == 0:
        return np.zeros(N, dtype=np.int64)
    c = np.zeros(N, dtype=np.int64)
    for j in range(1, k + 1):
        c = c * 2 + X[t - j]
    return c


def ll(p, y):
    p = np.clip(p, 1e-9, 1 - 1e-9)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p)).sum()


def evaluar(k, modo):
    S = 2 ** k
    c1 = np.zeros((N, S)) if modo == "numero" else np.zeros((1, S))
    c0 = np.zeros_like(c1)
    perdidas_modelo, perdidas_nulo = [], []
    for t in range(k, T):
        est = codigo_estado(X, t, k)
        fila = np.arange(N) if modo == "numero" else np.zeros(N, dtype=np.int64)
        if t >= a.calentamiento:
            n1, n0 = c1[fila, est], c0[fila, est]
            p = (n1 + a.prior * P0) / (n1 + n0 + a.prior)
            y = X[t]
            perdidas_modelo.append(ll(p, y))
            perdidas_nulo.append(ll(np.full(N, P0), y))
        # actualizar conteos DESPUES de predecir (sin fuga)
        np.add.at(c1, (fila, est), X[t])
        np.add.at(c0, (fila, est), 1 - X[t])
    d = np.array(perdidas_nulo) - np.array(perdidas_modelo)
    boot = [rng.choice(d, len(d)).mean() for _ in range(2000)]
    return d.mean(), np.percentile(boot, 2.5), np.percentile(boot, 97.5), len(d)

print(f"Juego: {a.juego} | sorteos: {T} | prior (fuerza de encogimiento): {a.prior}")
print(f"Delta log-loss por sorteo vs azar constante (>0 = mejora). Sorteos evaluados: {T - a.calentamiento}\n")
print(f"{'Orden k':<9}{'Estados':<9}{'Modo':<11}{'Delta':>12}{'IC95%':>28}  Veredicto")
for k in range(0, a.kmax + 1):
    for modo in (("pooled",) if k == 0 else ("pooled", "numero")):
        m, lo, hi, n = evaluar(k, modo)
        ver = "MEJORA" if lo > 0 else ("EMPEORA" if hi < 0 else "sin evidencia")
        print(f"{k:<9}{2**k:<9}{modo:<11}{m:>12.5f}{f'[{lo:.5f}, {hi:.5f}]':>28}  {ver}")

# Orden 1 clasico entre balotas dentro del sorteo vs entre sorteos: tamano de la tabla
print("\nDensidad de datos: transiciones por estado (orden 2 sobre balotas completas):")
print(f"  estados posibles = {N}x{N} = {N*N}; transiciones disponibles = {T-2}; ~{(T-2)/(N*N):.2f} obs/estado -> inviable sin agrupar")
