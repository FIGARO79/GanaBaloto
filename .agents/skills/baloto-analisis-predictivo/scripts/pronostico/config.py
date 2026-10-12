"""Configuración, rutas y parámetros del pronóstico (sin estado global mutable)."""

import os
import sys
from dataclasses import dataclass

# Raíz del proyecto (5 niveles arriba de este archivo) disponible en sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

RUTA_JSON = os.path.join(PROJECT_ROOT, "baloto.json")


@dataclass(frozen=True)
class Config:
    """Parámetros del ranking final y del tamaño de la salida."""

    peso_sim: float = 0.05  # Calibrado de 0.20 a 0.05 para priorizar Índice Compuesto/JAX y momentum actual
    peso_pop: float = 0.00  # peso de la penalización por Popularidad (0.0 para no penalizar y maximizar aciertos)
    max_solape: int = 2  # balotas máximas compartidas entre jugadas del Top
    n_top: int = 5
    n_pool: int = 150  # Aumentado a 150 para mayor amplitud de muestreo estocástico JAX
    perfil_activo: str = "B"  # Perfil B: Cazador de Ruptura por Atraso Extremo (Compromiso de inversión $18.000 COP)
    presupuesto_total_cop: int = 18000
    costo_tiquete_dual_cop: int = 9000
