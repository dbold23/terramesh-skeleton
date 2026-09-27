"""Runs the scorers over one view: embed, shortlist, then local matching on the shortlist."""
from __future__ import annotations
from pathlib import Path
from typing import Callable
import numpy as np
from .scoring import Calibration, Pair, shortlist

def score_view(view: str, queries: list[Path], catalog: list[Path], embedder, matchers, size: int, calibration: Calibration | None, *, exclude: np.ndarray | None=None, extra_pairs: list[tuple[int, int]]=(), symmetric: bool=False, report: Callable[[str], None]=lambda _: None) -> list[Pair]:
    """Scores query images against catalogue images of the same view.

    `exclude` marks pairs that must never be scored (the same encounter when calibrating).
    `extra_pairs` are scored even when the shortlist misses them (every same-individual pair when
    calibrating, so the calibration sees hard positives as well as easy ones). With `symmetric`
    (queries and catalogue are the same list) each unordered pair is scored once.
    """
    ...
