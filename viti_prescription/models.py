import math
from dataclasses import dataclass, field
from typing import List

@dataclass
class Spot:
    id: int
    x: float
    conf: float

@dataclass
class Environment:
    viento_vel: float  # m/s
    viento_dir: float  # grados (0-360), 0/360 es +X (a favor de hilera), 180 es -X (contra hilera)
    temp: float        # °C
    hum: float         # %

    @property
    def viento_longitudinal(self) -> float:
        # Extrae la componente longitudinal del viento a lo largo de la hilera.
        # cos(0) = 1 (a favor), cos(180) = -1 (en contra), cos(90) = 0 (perpendicular, sin efecto long.)
        rad = math.radians(self.viento_dir)
        return self.viento_vel * math.cos(rad)

@dataclass
class TreatmentZone:
    start: float
    end: float
    risk_max: float
    source_spot_ids: List[int] = field(default_factory=list)
