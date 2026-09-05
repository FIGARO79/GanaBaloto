#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para auditar y validar la integridad y consistencia del dataset baloto.json.
Comprueba rangos, duplicados, orden cronológico y tipos de datos.
"""

import sys
import os
import argparse
import json
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
FILE_PATH = os.path.join(PROJECT_ROOT, "baloto.json")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Audita la integridad y coherencia de baloto.json."
    )
    parser.add_argument(
        "--file",
        type=str,
        default=FILE_PATH,
        help=f"Ruta al archivo JSON (default: {FILE_PATH}).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Salida en formato JSON para herramientas automatizadas.",
    )
    return parser.parse_args()


def auditar_dataset(file_path):
    errores = []
    advertencias = []
    reporte = {}

    if not os.path.exists(file_path):
        errores.append(f"El archivo no existe: {file_path}")
        return {"valido": False, "errores": errores, "advertencias": advertencias, "reporte": reporte}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        errores.append(f"Error al parsear archivo JSON: {e}")
        return {"valido": False, "errores": errores, "advertencias": advertencias, "reporte": reporte}

    for sorteo in ["Baloto", "Revancha"]:
        if sorteo not in data:
            errores.append(f"Falta la clave principal '{sorteo}' en el JSON.")
            continue

        registros = data[sorteo]
        total = len(registros)
        if total == 0:
            errores.append(f"La lista de sorteos para '{sorteo}' está vacía.")
            continue

        fechas_vistas = set()
        ultima_fecha = None
        sorteo_stats = {
            "total_sorteos": total,
            "primer_sorteo": None,
            "ultimo_sorteo": None,
            "ultimos_numeros": None,
            "ultima_sb": None,
            "premios_mayores_registrados": 0,
        }

        for idx, item in enumerate(registros):
            fila_id = f"{sorteo} fila #{idx + 1}"

            # Validar campos requeridos
            campos_esperados = ["Fecha", "B1", "B2", "B3", "B4", "B5", "SB"]
            faltantes = [c for c in campos_esperados if c not in item]
            if faltantes:
                errores.append(f"{fila_id}: Faltan campos requeridos: {faltantes}")
                continue

            # Validar Fecha
            fecha_str = str(item["Fecha"]).strip()
            try:
                fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                errores.append(f"{fila_id}: Formato de fecha inválido '{fecha_str}' (debe ser YYYY-MM-DD).")
                continue

            if idx == 0:
                sorteo_stats["primer_sorteo"] = fecha_str

            if fecha_str in fechas_vistas:
                errores.append(f"{fila_id}: Fecha duplicada detectada '{fecha_str}'.")
            fechas_vistas.add(fecha_str)

            if ultima_fecha and fecha_dt < ultima_fecha:
                errores.append(
                    f"{fila_id}: Fecha fuera de orden cronológico ({fecha_str} es menor que {ultima_fecha.strftime('%Y-%m-%d')})."
                )
            ultima_fecha = fecha_dt

            # Validar Balotas principales B1..B5
            balotas = []
            for col in ["B1", "B2", "B3", "B4", "B5"]:
                val = item[col]
                if not isinstance(val, int) or val < 1 or val > 43:
                    errores.append(f"{fila_id}: Balota {col}={val} inválida (debe ser entero entre 1 y 43).")
                balotas.append(val)

            if len(set(balotas)) != 5:
                errores.append(f"{fila_id}: Balotas principales duplicadas en la misma jugada: {balotas}")

            # Validar Super Balota
            sb = item["SB"]
            if not isinstance(sb, int) or sb < 1 or sb > 16:
                errores.append(f"{fila_id}: Super Balota SB={sb} inválida (debe ser entero entre 1 y 16).")

            # Premios
            p51 = item.get("Premios 5+1", 0)
            if p51 and p51 > 0:
                sorteo_stats["premios_mayores_registrados"] += 1

            if idx == total - 1:
                sorteo_stats["ultimo_sorteo"] = fecha_str
                sorteo_stats["ultimos_numeros"] = balotas
                sorteo_stats["ultima_sb"] = sb

        reporte[sorteo] = sorteo_stats

    # Comparar sincronía entre Baloto y Revancha
    if "Baloto" in reporte and "Revancha" in reporte:
        b_count = reporte["Baloto"]["total_sorteos"]
        r_count = reporte["Revancha"]["total_sorteos"]
        if b_count != r_count:
            advertencias.append(
                f"Discrepancia en cantidad de sorteos: Baloto tiene {b_count} y Revancha tiene {r_count}."
            )
        b_ult = reporte["Baloto"]["ultimo_sorteo"]
        r_ult = reporte["Revancha"]["ultimo_sorteo"]
        if b_ult != r_ult:
            advertencias.append(
                f"Discrepancia en fecha del último sorteo: Baloto={b_ult} vs Revancha={r_ult}."
            )

    valido = len(errores) == 0
    return {
        "valido": valido,
        "errores": errores,
        "advertencias": advertencias,
        "reporte": reporte,
    }


def main():
    args = parse_args()
    resultado = auditar_dataset(args.file)

    if args.json:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 65)
        print("🔍 AUDITORÍA DE INTEGRIDAD: baloto.json")
        print("=" * 65)

        if resultado["valido"]:
            print("✅ ESTADO: BASE DE DATOS ÍNTEGRA Y VÁLIDA")
        else:
            print(f"❌ ESTADO: SE DETECTARON {len(resultado['errores'])} ERRORES CRÍTICOS")

        for s, stats in resultado["reporte"].items():
            print(f"\n📊 Resumen {s}:")
            print(f"   • Total sorteos registrados : {stats['total_sorteos']}")
            print(f"   • Rango histórico           : {stats['primer_sorteo']}  -->  {stats['ultimo_sorteo']}")
            print(f"   • Último resultado          : {stats['ultimos_numeros']} + SB({stats['ultima_sb']})")
            print(f"   • Sorteos con premio mayor  : {stats['premios_mayores_registrados']}")

        if resultado["advertencias"]:
            print("\n⚠️ ADVERTENCIAS:")
            for adv in resultado["advertencias"]:
                print(f"   • {adv}")

        if resultado["errores"]:
            print("\n❌ ERRORES DETECTADOS:")
            for err in resultado["errores"]:
                print(f"   • {err}")

        print("=" * 65 + "\n")

    sys.exit(0 if resultado["valido"] else 1)


if __name__ == "__main__":
    main()
