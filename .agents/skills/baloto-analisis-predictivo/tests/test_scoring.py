"""Pruebas unitarias para el módulo de scoring (popularidad, similitud con botes y JAX)."""

import os
import sys
import unittest

# Asegurar rutas
TESTS_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
SCRIPTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "../scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from pronostico.scoring import calcular_popularidad, calcular_similitud_botes


class TestScoring(unittest.TestCase):
    def test_popularidad_cumpleanos(self):
        """Combinación con todos <= 31 debe recibir penalización alta."""
        comb_fechas = [3, 7, 12, 21, 28]  # Todos <= 31, incluye 3 y 7 (suerte), SB 5 (mes)
        pop = calcular_popularidad(comb_fechas, sb=5)
        # 35 (fechas) + 4*2 (suerte) + 5 (mes) = 48
        self.assertGreaterEqual(pop, 40.0)
        self.assertLessEqual(pop, 100.0)

    def test_popularidad_consecutivos_y_progresion(self):
        """Combinaciones aritméticas (5-10-15-20-25) o consecutivas (1-2-3-4-5)."""
        comb_prog = [5, 10, 15, 20, 25]
        pop_prog = calcular_popularidad(comb_prog, sb=16)
        # 35 (todos <=31) + 30 (progresion dif=5) + 10 (max<=25) = 75
        self.assertGreaterEqual(pop_prog, 65.0)

        comb_cons = [1, 2, 3, 4, 5]
        pop_cons = calcular_popularidad(comb_cons, sb=16)
        # 35 + 4*12 (consecutivos) + 30 (prog dif=1) + 4 (suerte 3) + 10 (max<=25) = 100 (clamp)
        self.assertEqual(pop_cons, 100.0)

    def test_popularidad_baja(self):
        """Combinación dispersa con números altos (>31) y sin números de suerte ni mes."""
        comb_alta = [8, 19, 33, 38, 42]
        pop = calcular_popularidad(comb_alta, sb=15)
        # Solo 2 números <= 31, sin consecutivos, sin progresión, sin números de suerte, SB > 12
        self.assertEqual(pop, 0.0)

    def test_similitud_botes_vacio(self):
        """Sin historial de botes debe devolver 0.0."""
        self.assertEqual(calcular_similitud_botes([1, 2, 3, 4, 5], 10, []), 0.0)

    def test_similitud_botes_rango(self):
        """Con botes sintéticos, la similitud debe estar acotada entre 0 y 100."""
        botes_sinteticos = [
            ([8, 16, 19, 35, 41], 13),
            ([5, 6, 14, 26, 31], 11),
            ([8, 9, 19, 23, 38], 14),
        ]
        sim1 = calcular_similitud_botes([8, 19, 14, 35, 41], 13, botes_sinteticos)
        sim2 = calcular_similitud_botes([1, 2, 3, 4, 7], 2, botes_sinteticos)

        self.assertGreaterEqual(sim1, 0.0)
        self.assertLessEqual(sim1, 100.0)
        self.assertGreaterEqual(sim2, 0.0)
        self.assertLessEqual(sim2, 100.0)
        # La que comparte balotas (8, 19, 14, 35, 41) y SB alta debe tener mayor similitud
        self.assertGreater(sim1, sim2)


if __name__ == "__main__":
    unittest.main()
