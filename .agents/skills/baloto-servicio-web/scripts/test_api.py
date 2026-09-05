#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de pruebas automatizadas para la API REST de GanaBaloto (Flask).
Verifica endpoints de consulta, generación, auditoría manual, ruedas y recarga de caché.
"""

import sys
import os
import json
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app


def run_tests():
    client = app.test_client()
    pruebas = []
    inicio_total = time.time()

    def registrar(nombre, exitoso, detalle="", duracion_ms=0):
        pruebas.append({
            "nombre": nombre,
            "exitoso": exitoso,
            "detalle": detalle,
            "duracion_ms": round(duracion_ms, 1),
        })
        icono = "✅ PASS" if exitoso else "❌ FAIL"
        print(f"[{icono}] {nombre} ({duracion_ms:.1f} ms)")
        if not exitoso and detalle:
            print(f"        Detalle: {detalle}")

    print("\n" + "=" * 65)
    print("🧪 INICIANDO SUITE DE PRUEBAS - API REST GANABALOTO")
    print("=" * 65)

    # 1. GET /api/sorteo/Baloto
    t0 = time.time()
    res = client.get("/api/sorteo/Baloto")
    dt = (time.time() - t0) * 1000
    if res.status_code == 200:
        data = res.get_json()
        if "last_combination" in data and "score_meta" in data:
            registrar("GET /api/sorteo/Baloto", True, duracion_ms=dt)
        else:
            registrar("GET /api/sorteo/Baloto", False, "Faltan claves esperadas en JSON", duracion_ms=dt)
    else:
        registrar("GET /api/sorteo/Baloto", False, f"Status HTTP {res.status_code}", duracion_ms=dt)

    # 2. GET /api/sorteo/Revancha
    t0 = time.time()
    res = client.get("/api/sorteo/Revancha")
    dt = (time.time() - t0) * 1000
    if res.status_code == 200:
        data = res.get_json()
        if "last_combination" in data:
            registrar("GET /api/sorteo/Revancha", True, duracion_ms=dt)
        else:
            registrar("GET /api/sorteo/Revancha", False, "Faltan claves esperadas en JSON", duracion_ms=dt)
    else:
        registrar("GET /api/sorteo/Revancha", False, f"Status HTTP {res.status_code}", duracion_ms=dt)

    # 3. GET /api/sorteo/Inexistente (Manejo de error 404)
    t0 = time.time()
    res = client.get("/api/sorteo/LoteríaFicticia")
    dt = (time.time() - t0) * 1000
    registrar("GET /api/sorteo/Inexistente (404 esperado)", res.status_code == 404, duracion_ms=dt)

    # 4. POST /api/generar (Sugerencias multimodelo)
    t0 = time.time()
    res = client.post(
        "/api/generar",
        data=json.dumps({"sorteo": "Baloto", "cantidad": 3}),
        content_type="application/json",
    )
    dt = (time.time() - t0) * 1000
    if res.status_code == 200:
        data = res.get_json()
        combs = data.get("combinaciones", [])
        if len(combs) == 3 and "composite" in combs[0]:
            registrar("POST /api/generar (3 jugadas)", True, duracion_ms=dt)
        else:
            registrar("POST /api/generar (3 jugadas)", False, f"Se esperaban 3 combinaciones, recibidas {len(combs)}", duracion_ms=dt)
    else:
        registrar("POST /api/generar (3 jugadas)", False, f"Status HTTP {res.status_code}", duracion_ms=dt)

    # 5. POST /api/analizar (Diagnóstico manual válido)
    t0 = time.time()
    res = client.post(
        "/api/analizar",
        data=json.dumps({"sorteo": "Baloto", "numeros": [4, 8, 15, 23, 42], "sb": 7}),
        content_type="application/json",
    )
    dt = (time.time() - t0) * 1000
    if res.status_code == 200:
        data = res.get_json()
        if "composite" in data and "veredicto" in data and isinstance(data["veredicto"], list):
            registrar("POST /api/analizar (Jugada válida)", True, duracion_ms=dt)
        else:
            registrar("POST /api/analizar (Jugada válida)", False, "Respuesta incompleta", duracion_ms=dt)
    else:
        registrar("POST /api/analizar (Jugada válida)", False, f"Status HTTP {res.status_code}", duracion_ms=dt)

    # 6. POST /api/analizar (Validación de error 400 con parámetros faltantes)
    t0 = time.time()
    res = client.post(
        "/api/analizar",
        data=json.dumps({"sorteo": "Baloto", "numeros": [4, 8, 15]}),  # Faltan números y SB
        content_type="application/json",
    )
    dt = (time.time() - t0) * 1000
    registrar("POST /api/analizar (Error 400 esperado)", res.status_code == 400, duracion_ms=dt)

    # 7. POST /api/rueda (Sistema reducido de 7 números)
    t0 = time.time()
    res = client.post(
        "/api/rueda",
        data=json.dumps({
            "sorteo": "Baloto",
            "numeros": [4, 8, 15, 23, 31, 38, 42],
            "garantia": 3,
            "sbs": [7],
        }),
        content_type="application/json",
    )
    dt = (time.time() - t0) * 1000
    if res.status_code == 200:
        data = res.get_json()
        if "tiquetes_finales" in data and data.get("total_tiquetes", 0) > 0:
            registrar("POST /api/rueda (Garantía 3 aciertos)", True, duracion_ms=dt)
        else:
            registrar("POST /api/rueda (Garantía 3 aciertos)", False, "Sin tiquetes generados", duracion_ms=dt)
    else:
        registrar("POST /api/rueda (Garantía 3 aciertos)", False, f"Status HTTP {res.status_code}", duracion_ms=dt)

    # 8. POST /api/recargar (Refresco de caché)
    t0 = time.time()
    res = client.post("/api/recargar")
    dt = (time.time() - t0) * 1000
    registrar("POST /api/recargar", res.status_code == 200, duracion_ms=dt)

    # Resumen
    tiempo_total = (time.time() - inicio_total) * 1000
    total_pruebas = len(pruebas)
    aprobadas = sum(1 for p in pruebas if p["exitoso"])
    fallidas = total_pruebas - aprobadas

    print("-" * 65)
    print(f"📊 RESUMEN: {aprobadas}/{total_pruebas} pruebas exitosas ({fallidas} fallidas) en {tiempo_total:.1f} ms.")
    print("=" * 65 + "\n")

    return fallidas == 0


if __name__ == "__main__":
    exito = run_tests()
    sys.exit(0 if exito else 1)
