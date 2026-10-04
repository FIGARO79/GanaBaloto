"""Pruebas unitarias para el módulo de datos históricos e información del sorteo."""

import os
import sys
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from pronostico.datos import cargar_datos, obtener_info_sorteo, botes_de, extraer_botes_ganadores


class TestDatos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_json = cargar_datos()

    def test_estructura_datos(self):
        """Verifica que baloto.json contiene las modalidades principales y un historial extenso."""
        self.assertIn("Baloto", self.data_json)
        self.assertIn("Revancha", self.data_json)
        self.assertGreater(len(self.data_json["Baloto"]), 1000)
        self.assertGreater(len(self.data_json["Revancha"]), 900)

    def test_botes_historicos(self):
        """Verifica extracción correcta de botes ganadores del acumulado 5+1."""
        botes_b = botes_de(self.data_json, "Baloto")
        self.assertGreaterEqual(len(botes_b), 20)
        for b in botes_b:
            self.assertGreater(b.get("Premios 5+1", 0), 0)
            self.assertTrue(all(f"B{i}" in b for i in range(1, 6)))
            self.assertIn("SB", b)

        ganadores = extraer_botes_ganadores(self.data_json, "Baloto")
        self.assertEqual(len(ganadores), len(botes_b))
        for comb, sb in ganadores:
            self.assertEqual(len(comb), 5)
            self.assertTrue(all(1 <= x <= 43 for x in comb))
            self.assertTrue(1 <= sb <= 16)

    def test_info_sorteo_fecha_especifica(self):
        """Prueba cálculo de metadatos para fecha fija (2026-10-05, Lunes)."""
        info = obtener_info_sorteo(self.data_json, fecha_str="2026-10-05")

        self.assertEqual(info["fecha"], "2026-10-05")
        self.assertEqual(info["dia"], 5)
        self.assertEqual(info["mes"], 10)
        self.assertEqual(info["suma_dia_mes"], 15)
        self.assertIn("Lunes", info["fecha_legible"])

        self.assertTrue(len(info["anclajes_principales"]) > 0)
        self.assertTrue(all(1 <= x <= 43 for x in info["anclajes_principales"]))

        self.assertIn("Baloto", info["pivotes_botes"])
        self.assertIn("Revancha", info["pivotes_botes"])
        self.assertIn("Baloto", info["sbs_reinas"])
        self.assertIn("Revancha", info["sbs_reinas"])


if __name__ == "__main__":
    unittest.main()
