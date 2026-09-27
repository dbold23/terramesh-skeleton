"""Which species to expect at a place and week, from BirdNET's geomodel (V3.0.4, 14K species, weights
Apache-2.0). It only narrows what is suggested: every window is still scored against every label, and
a label the geomodel does not know (a frog in Perch, say) is never filtered out."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
from .download import Remote, fetch

@dataclass
class GeoFilter:
    name: str
    version: str
    licence: str
    commercial_use: bool
    source: str
    weights: Path
    known: set[str]

    def expected(self, latitude: float, longitude: float, week: int, minimum: float) -> set[str]:
        ...

    def allowed(self, labels, expected: set[str]) -> np.ndarray:
        """True for each label that is expected here or that the geomodel knows nothing about."""
        ...

def load(cache: Path, device: str, *, fake: bool=False) -> GeoFilter:
    ...
