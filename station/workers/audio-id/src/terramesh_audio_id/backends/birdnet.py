"""BirdNET+ V3.0 (developer preview 3.1, 11K species; K. Lisa Yang Center for Conservation
Bioacoustics and Chemnitz University of Technology), run from its ONNX file with ONNX Runtime.
The URLs, sizes and hashes are the ones the `birdnet` package (1.1.1) pins. BirdNET 2.4 is never
used: its model is licensed CC BY-NC-SA 4.0."""
from __future__ import annotations
import csv
import io
from pathlib import Path
import numpy as np
from . import Label, onnx_session, output_width
from ..download import Remote, fetch

class BirdNETBackend:
    commercial_use = False
    sample_rate = 32000
    window_seconds = 3.0

    def __init__(self, *, cache: Path, device: str) -> None:
        ...

    def score(self, batch: np.ndarray) -> np.ndarray:
        ...

def read_labels(path: Path) -> list[Label]:
    """A `;`-separated CSV in output order, with `sci_name` and `com_name` columns."""
    ...
