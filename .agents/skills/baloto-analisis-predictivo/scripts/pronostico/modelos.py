"""Modelos de datos tipados del pronóstico."""

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Jugada:
    comb: list
    sb: int
    suma: int
    indice: float
    similitud: float
    popularidad: float
    indice_ajustado: float
    jax: float
    gauss: float
    entropia: float
    bayes: float
    hazard: float
    ising: float
    es_optimo: bool
    tiene_adn: bool
    tiene_anclaje: bool
    coinc_fecha: list = field(default_factory=list)
    coinc_lag8: list = field(default_factory=list)
    es_espejo: bool = False
    tiene_salto: bool = False
    tiene_ising: bool = False

    def to_dict(self):
        return asdict(self)


@dataclass
class ResultadoSorteo:
    sorteo: str
    score_meta: float
    total_sorteos: int
    ultimo_sorteo: Any
    ultima_sb: int
    df_gap_analysis: Any
    main_counts_dict: dict
    sb_counts_dict: dict
    regime_info: dict
    jugadas: list

    def to_dict(self, incluir_gaps=False):
        d = {k: v for k, v in self.__dict__.items() if k != "jugadas"}
        if not incluir_gaps:
            d.pop("df_gap_analysis")
        d["jugadas"] = [j.to_dict() for j in self.jugadas]
        return d
