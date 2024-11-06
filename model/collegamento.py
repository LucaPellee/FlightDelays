from dataclasses import dataclass
from model.airport import Airport

@dataclass
class Collegamento:
    v0: Airport
    v1: Airport
    qta: int