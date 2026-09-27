"""A deterministic stand-in model for tests: it "hears" a pure tone near 2 kHz as one species and a
tone near 5 kHz as another, by measuring spectral energy. It never ships in a layer Station keeps:
the worker only loads it when TERRAMESH_AUDIO_ID_FAKE=1."""
from __future__ import annotations
from pathlib import Path
import numpy as np
from . import Label

class FakeBackend:
    commercial_use = True
    sample_rate = 32000
    window_seconds = 5.0

    def __init__(self, *, cache: Path) -> None:
        ...

    def score(self, batch: np.ndarray) -> np.ndarray:
        ...
