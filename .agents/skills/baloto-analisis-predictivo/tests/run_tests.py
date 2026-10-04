#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejecutor de la suite de pruebas unitarias para el motor de pronóstico de GanaBaloto.
"""

import os
import sys
import unittest
import time

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "../scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)


def main():
    print("\n" + "=" * 70)
    print("SUITE DE PRUEBAS UNITARIAS - MOTOR DE PRONÓSTICO GANABALOTO")
    print("=" * 70)

    t0 = time.time()
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=TESTS_DIR, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    elapsed = time.time() - t0

    print("=" * 70)
    print(f"Total pruebas: {result.testsRun} | Exitosas: {result.testsRun - len(result.failures) - len(result.errors)} | Fallidas: {len(result.failures)} | Errores: {len(result.errors)}")
    print(f"Tiempo de ejecución: {elapsed:.2f} s")
    print("=" * 70 + "\n")

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
