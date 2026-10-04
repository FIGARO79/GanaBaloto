#!/usr/bin/env python3
"""Valida si la relación ganadores-fechas supera al azar.

Uso: ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/validar_fechas.py [Baloto|Revancha] [N_PERM]

1. Métricas de fecha calculadas sobre TODOS los sorteos (línea base empírica).
2. Prueba de permutación: subconjuntos aleatorios del mismo tamaño que los botes.
3. Corrección de Bonferroni por número de métricas probadas.
4. Backtesting walk-forward: ¿"día del mes" mejora el acierto promedio?
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
JUEGO = sys.argv[1] if len(sys.argv) > 1 else "Baloto"
N_PERM = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
rng = np.random.default_rng(42)

datos = json.load(open(RAIZ / "baloto.json"))[JUEGO]
datos = [s for s in datos if s.get("B5")]
fechas = [datetime.strptime(s["Fecha"], "%Y-%m-%d") for s in datos]
bolas = np.array([[s[f"B{i}"] for i in range(1, 6)] for s in datos])
sb = np.array([s["SB"] for s in datos])
es_bote = np.array([(s.get("Premios 5+1") or 0) > 0 for s in datos])
n, nb = len(datos), int(es_bote.sum())

dia = np.array([f.day for f in fechas])
mes = np.array([f.month for f in fechas])

metricas = {
    "día del mes en balotas": np.array([dia[i] in bolas[i] for i in range(n)]),
    "mes en balotas": np.array([mes[i] in bolas[i] for i in range(n)]),
    "día y mes en balotas": np.array([dia[i] in bolas[i] and mes[i] in bolas[i] for i in range(n)]),
    "SB == mes": sb == mes,
    "SB == día (si <=16)": (sb == dia),
    "algún número <=31 (fecha)": np.array([(b <= 31).all() for b in bolas]),
}

print(f"Juego: {JUEGO} | sorteos: {n} | botes 5+1: {nb} | permutaciones: {N_PERM}\n")
k = len(metricas)
print(f"{'Métrica':<28}{'Base':>8}{'Botes':>8}{'p-perm':>10}{'p-Bonf':>10}  Veredicto")
for nombre, v in metricas.items():
    base = v.mean()
    obs = v[es_bote].mean() if nb else 0
    idx = np.array([rng.choice(n, nb, replace=False) for _ in range(N_PERM)])
    sim = v[idx].mean(axis=1)
    p = (np.sum(sim >= obs) + 1) / (N_PERM + 1)
    pb = min(1.0, p * k)
    ver = "SIGNIFICATIVO" if pb < 0.05 else "ruido (no supera al azar)"
    print(f"{nombre:<28}{base:>8.3f}{obs:>8.3f}{p:>10.4f}{pb:>10.4f}  {ver}")

# Backtesting walk-forward: ¿las balotas de "día del mes" repiten más que el azar?
print("\nBacktesting walk-forward (aciertos promedio de balotas por sorteo, top-5 candidatos):")
ini = max(200, n // 3)
res = {"azar": [], "frecuencia": [], "frecuencia + día del mes": []}
for t in range(ini, n):
    hist = bolas[:t].ravel()
    frec = np.bincount(hist, minlength=44)[1:].astype(float)
    reales = set(bolas[t])
    azar = rng.choice(np.arange(1, 44), 5, replace=False)
    top = np.argsort(-frec)[:5] + 1
    f2 = frec.copy()
    if dia[t] <= 43:
        f2[dia[t] - 1] += f2.max()
    top2 = np.argsort(-f2)[:5] + 1
    res["azar"].append(len(reales & set(azar)))
    res["frecuencia"].append(len(reales & set(top)))
    res["frecuencia + día del mes"].append(len(reales & set(top2)))
for kx, v in res.items():
    print(f"  {kx:<28} media={np.mean(v):.4f}  (esperado azar = {5*5/43:.4f})")

print("\nConclusión: solo considerar una señal real si p-Bonf < 0.05 Y el backtest supera consistentemente al azar.")
