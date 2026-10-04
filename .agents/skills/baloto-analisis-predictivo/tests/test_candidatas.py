"""Pruebas unitarias para selección diversa y candidatas."""

import os
import sys
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from pronostico.candidatas import seleccion_diversa


class TestCandidatas(unittest.TestCase):
    def test_seleccion_diversa_max_solape(self):
        """Verifica que seleccion_diversa previene solapes superiores a max_solape."""
        # 4 combinaciones sintéticas:
        # C0 y C1 comparten 4 balotas (1,2,3,4) -> solape = 4
        # C2 es independiente (10, 11, 12, 13, 14) -> solape = 0
        # C3 comparte solo 2 con C0 (1, 2, 20, 21, 22) -> solape = 2
        cand = [
            ([1, 2, 3, 4, 5], 10, 0.15, 75.0),    # Item 0
            ([1, 2, 3, 4, 6], 10, 0.15, 74.0),    # Item 1 (solape 4 con Item 0)
            ([10, 11, 12, 13, 14], 12, 0.14, 73.0), # Item 2 (solape 0)
            ([1, 2, 20, 21, 22], 14, 0.14, 72.0), # Item 3 (solape 2 con Item 0)
        ]

        # Con max_solape=2 y n_top=3:
        # diversas debe tomar Item 0, rechazar Item 1 (solape 4), tomar Item 2 (solape 0), tomar Item 3 (solape 2)
        resultado = seleccion_diversa(cand, n_top=3, max_solape=2)
        top3 = resultado[:3]

        self.assertEqual(top3[0][0], [1, 2, 3, 4, 5])
        self.assertEqual(top3[1][0], [10, 11, 12, 13, 14])
        self.assertEqual(top3[2][0], [1, 2, 20, 21, 22])

        # Verificar que el par (top3[0], top3[1]) y (top3[0], top3[2]) tienen solape <= 2
        for i in range(len(top3)):
            for j in range(i + 1, len(top3)):
                solape = len(set(top3[i][0]) & set(top3[j][0]))
                self.assertLessEqual(solape, 2)

    def test_seleccion_diversa_relleno_si_faltan(self):
        """Si no hay suficientes combinaciones diversas, debe incluir las restantes para no dejar vacíos."""
        cand = [
            ([1, 2, 3, 4, 5], 10, 0.15, 75.0),
            ([1, 2, 3, 4, 6], 10, 0.15, 74.0),
        ]
        # Pide n_top=5 pero solo hay 2 candidatas y ambas solapan
        resultado = seleccion_diversa(cand, n_top=5, max_solape=2)
        self.assertEqual(len(resultado), 2)
        self.assertIn(cand[0], resultado)
        self.assertIn(cand[1], resultado)


if __name__ == "__main__":
    unittest.main()
