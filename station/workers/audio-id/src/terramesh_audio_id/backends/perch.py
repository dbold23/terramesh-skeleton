"""Perch 2.0 (Google DeepMind), run from the ONNX conversion that perch-hoplite itself loads
(`load_model_by_name("perch_v2_onnx")`), with hoplite's preprocessing and logit calibration so its
scores match hoplite's and the phone's."""
from __future__ import annotations
import csv
import os
import shutil
from pathlib import Path
import numpy as np
from . import Label, onnx_session, output_width
from ..download import Remote, fetch
TARGET_PEAK = 0.25
LOGIT_SLOPE = 0.97
LOGIT_INTERCEPT = -10.0

class PerchBackend:
    commercial_use = True
    sample_rate = 32000
    window_seconds = 5.0

    def __init__(self, *, cache: Path, device: str) -> None:
        ...

    def score(self, batch: np.ndarray) -> np.ndarray:
        ...

def normalise(batch: np.ndarray) -> np.ndarray:
    """perch_hoplite zoo_interface.normalize_audio: remove each window's mean, then scale its peak to 0.25.
    A silent window stays silent."""
    ...

def scientific_name(label: str) -> str | None:
    """Perch 2.0's labels are 14,597 iNaturalist binomials plus 198 FSD50K sound-event classes
    ("Organ", "Dog", "Waves_and_surf"), which are one word or joined with underscores. Only a
    binomial is a scientific name; a sound class is kept as its label and never offered as a taxon."""
    ...

def read_labels(folder: Path) -> list[str]:
    """labels.csv from the Kaggle model's assets: the namespace on the first row, then one iNaturalist
    scientific name per row in output order. Kept beside the weights once fetched; a copy placed there
    by hand is used as is."""
    ...
