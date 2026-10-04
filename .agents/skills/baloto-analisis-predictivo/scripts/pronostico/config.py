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

    peso_sim: float = 0.20  # peso de la Similitud con botes en el Índice Ajustado
    peso_pop: float = 0.10  # peso de la penalización por Popularidad
    max_solape: int = 2  # balotas máximas compartidas entre jugadas del Top
    n_top: int = 5
    n_pool: int = 120
