"""Pruebas unitarias para la rueda combinatoria reducida (wheeling system)."""

import os
import sys
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from pronostico.rueda import verificar_garantia, construir_rueda_optima, BLOQUES_INDICES
from pronostico.datos import cargar_datos, obtener_info_sorteo


class TestRueda(unittest.TestCase):
    def test_garantia_matematica_terna(self):
        """Verifica que los 5 bloques elegidos cubren 100% de las C(7,3)=35 ternas posibles."""
        es_valido, faltantes = verificar_garantia(bloques=BLOQUES_INDICES, n_numeros=7, garantia=3)
        self.assertTrue(es_valido, f"La rueda no cubre todas las ternas. Faltan {faltantes}")
        self.assertEqual(faltantes, 0)

    def test_construir_rueda_optima(self):
        """Verifica la generación de la rueda sobre datos reales de baloto.json."""
        data_json = cargar_datos()
        info = obtener_info_sorteo(data_json, fecha_str="2026-10-05")
        rueda = construir_rueda_optima(data_json, info)

        self.assertEqual(len(rueda["numeros_pool"]), 7)
        self.assertEqual(len(set(rueda["numeros_pool"])), 7)
        self.assertTrue(all(1 <= x <= 43 for x in rueda["numeros_pool"]))

        self.assertEqual(len(rueda["super_balotas"]), 2)
        self.assertTrue(all(1 <= x <= 16 for x in rueda["super_balotas"]))

        self.assertEqual(rueda["total_tiquetes"], 10)
        self.assertEqual(len(rueda["tiquetes"]), 10)

        for t in rueda["tiquetes"]:
            self.assertEqual(len(t["comb"]), 5)
            self.assertEqual(len(set(t["comb"])), 5)
            self.assertTrue(set(t["comb"]).issubset(set(rueda["numeros_pool"])))
            self.assertIn(t["sb"], rueda["super_balotas"])


if __name__ == "__main__":
    unittest.main()
