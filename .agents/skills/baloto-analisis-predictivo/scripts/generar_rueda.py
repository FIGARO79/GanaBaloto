#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI para generar Ruedas Combinatorias Reducidas (Wheeling Systems)
garantizando matemáticamente condiciones de acierto con presupuesto optimizado.
"""

import sys
import os
import argparse
import json
import re

# Asegurar que el directorio raíz del proyecto esté en sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

_is_json = "--json" in sys.argv
if _is_json:
    _old_stdout = sys.stdout
    sys.stdout = sys.stderr

import ganabaloto as gb

if _is_json:
    sys.stdout = _old_stdout


def parse_args():
    parser = argparse.ArgumentParser(
        description="Genera una Rueda Combinatoria Reducida (Wheeling System) para Baloto o Revancha."
    )
    parser.add_argument(
        "--numeros",
        type=int,
        nargs="+",
        required=True,
        help="Entre 5 y 12 números principales (1-43), separados por espacio (ej: --numeros 4 8 15 23 31 38 42).",
    )
    parser.add_argument(
        "--sbs",
        type=int,
        nargs="*",
        default=[],
        help="Una o varias Super Balotas (1-16). Si no se especifica, se toma la última SB del histórico.",
    )
    parser.add_argument(
        "--garantia",
        type=int,
        default=3,
        choices=[3, 4],
        help="Nivel de garantía de aciertos matemáticos si los números ganadores están en tu selección (3 o 4. Default: 3).",
    )
    parser.add_argument(
        "--sorteo",
        type=str,
        default="Baloto",
        choices=["Baloto", "Revancha"],
        help="Sorteo de referencia para Super Balota sugerida si no se indica (default: Baloto).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Retornar resultados en formato JSON.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Validaciones
    nums = sorted(list(set(args.numeros)))
    if len(nums) < 5 or len(nums) > 12:
        print(f"❌ Error: Debes ingresar entre 5 y 12 números únicos (ingresados: {len(nums)}).", file=sys.stderr)
        sys.exit(1)

    for n in nums:
        if n < 1 or n > gb.N_MAIN_BALLS:
            print(f"❌ Error: El número {n} está fuera de rango (1-{gb.N_MAIN_BALLS}).", file=sys.stderr)
            sys.exit(1)

    sbs = sorted(list(set(args.sbs)))
    if not sbs:
        # Cargar última SB del histórico si no se proveyó
        json_path = os.path.join(PROJECT_ROOT, gb.FILE_PATH)
        sb_def = 7
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data_json = json.load(f)
                if args.sorteo in data_json and len(data_json[args.sorteo]) > 0:
                    sb_def = int(data_json[args.sorteo][-1]["SB"])
            except Exception:
                pass
        sbs = [sb_def]

    for sb_val in sbs:
        if sb_val < 1 or sb_val > gb.N_SUPER_BALOTA:
            print(f"❌ Error: La Super Balota {sb_val} está fuera de rango (1-{gb.N_SUPER_BALOTA}).", file=sys.stderr)
            sys.exit(1)

    # Generar rueda combinatoria base (combinaciones de 5 balotas)
    ruedas_base = gb.generate_wheeling_system(nums, target_guarantee=args.garantia)

    # Expandir con Super Balotas
    tiquetes = []
    for comb in ruedas_base:
        for sb_val in sbs:
            tiquetes.append({
                "combinacion": [int(x) for x in comb],
                "sb": int(sb_val),
            })

    if args.json:
        resultado = {
            "sorteo_referencia": args.sorteo,
            "numeros_seleccionados": nums,
            "super_balotas": sbs,
            "garantia_aciertos": args.garantia,
            "combinaciones_base_5": len(ruedas_base),
            "total_tiquetes": len(tiquetes),
            "tiquetes": tiquetes,
        }
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 70)
        print("⚙️ SISTEMA DE RUEDAS COMBINATORIAS REDUCIDAS (WHEELING SYSTEM)")
        print("=" * 70)
        print(f"🎯 Números seleccionados ({len(nums)}): {nums}")
        print(f"🔮 Super Balota(s) ({len(sbs)}): {sbs}")
        print(f"🛡️ Nivel de Garantía: {args.garantia} Aciertos garantizados si los ganadores están en tu selección")
        print(f"📦 Combinaciones base de 5 números: {len(ruedas_base)}")
        print(f"🎟️ Total de Tiquetes a jugar: {len(tiquetes)}")
        print("-" * 70)
        print("📋 TIQUETES GENERADOS:")
        for idx, t in enumerate(tiquetes, 1):
            comb_str = "-".join(f"{n:02d}" for n in t["combinacion"])
            print(f"  Tiquete #{idx:02d}:  {comb_str}  +  SB [{t['sb']:02d}]")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
