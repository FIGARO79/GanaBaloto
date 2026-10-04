"""Prueba de integración end-to-end para el flujo de pronóstico completo."""

import os
import sys
import unittest

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from pronostico.config import Config
from pronostico.datos import cargar_datos, obtener_info_sorteo
from pronostico.candidatas import obtener_mejores_jugadas
from pronostico.auditoria import auditoria_cualitativa
from pronostico.rueda import construir_rueda_optima


class TestIntegracion(unittest.TestCase):
    def test_flujo_completo_baloto_y_revancha(self):
        """Ejecuta el pipeline completo de obtención de jugadas y auditoría."""
        data_json = cargar_datos()
        info = obtener_info_sorteo(data_json, fecha_str="2026-10-05")
        cfg = Config(peso_sim=0.20, peso_pop=0.10, n_top=5, n_pool=30)

        # 1. Baloto
        res_b = obtener_mejores_jugadas("Baloto", data_json, info, cfg)
        self.assertEqual(len(res_b.jugadas), 5)
        top1_b = res_b.jugadas[0]
        self.assertGreater(top1_b.indice, 0.0)
        self.assertGreater(top1_b.indice_ajustado, 0.0)

        # 2. Revancha
        res_r = obtener_mejores_jugadas("Revancha", data_json, info, cfg)
        self.assertEqual(len(res_r.jugadas), 5)

        # 3. Auditoría de Top 1
        audit_b = auditoria_cualitativa(top1_b, res_b, info)
        self.assertIn("desc_suma", audit_b)
        self.assertIn("desc_entr", audit_b)
        self.assertIn("desc_jax", audit_b)
        self.assertIn("desc_sb", audit_b)

        # 4. Rueda
        rueda = construir_rueda_optima(data_json, info)
        self.assertEqual(len(rueda["tiquetes"]), 10)

        # 5. Serialización JSON (to_dict)
        dict_b = res_b.to_dict()
        self.assertIn("jugadas", dict_b)
        self.assertEqual(len(dict_b["jugadas"]), 5)
        self.assertEqual(dict_b["jugadas"][0]["comb"], top1_b.comb)


if __name__ == "__main__":
    unittest.main()
