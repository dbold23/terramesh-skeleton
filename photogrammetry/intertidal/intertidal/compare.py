"""Compare two visits to the same crevice.

Both records are in their own crevice frames, which already agree to within a few
millimetres and degrees because both are built from the mouth. The second visit is then
aligned to the first on the rock that should not have changed: the face around the mouth and
the first few millimetres of its walls, never the deep interior, which is what we want to
measure. The alignment residual is the floor under every change reported.

Changes are measured on the first visit's mouth grid, over cells that both visits saw:
a negative depth change means the surface behind that cell came closer to the mouth
(sediment, cobble, growth); a positive one means it moved back.
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
import cv2
import numpy as np
from . import measure, ply
from .record import depth_map
STABLE_DEPTH_MM = 10.0
SAMPLES = 20000

@dataclass
class Visit:
    folder: Path
    record: dict
    xyz: np.ndarray
    outline: np.ndarray

    @classmethod
    def load(cls, folder: Path) -> 'Visit':
        ...

@dataclass
class Alignment:
    R: np.ndarray
    t: np.ndarray
    rms_mm: float
    inlier_share: float
    pairs: int

    def apply(self, points: np.ndarray) -> np.ndarray:
        ...

def stable_points(visit: Visit) -> np.ndarray:
    """Rock that infill should not touch: everything shallower than STABLE_DEPTH_MM."""
    ...

def _normals(points: np.ndarray, tree, k: int=12) -> np.ndarray:
    ...

def icp(source: np.ndarray, target: np.ndarray, R: np.ndarray, t: np.ndarray, iterations: int=50, max_distance: float=8.0) -> Alignment:
    """Point-to-plane ICP taking `source` onto `target`, from the starting guess (R, t)."""
    ...

def align(first: Visit, second: Visit, seed: int=0) -> Alignment:
    """Take `second` into `first`'s crevice frame, trying both directions of the long axis."""
    ...
AGREEMENT_MM = 3.0
AGREEMENT_MARGIN_MM = 30.0
MATCH_AGREEMENT = 0.75
MATCH_RMS_MM = 2.0
AMBIGUOUS_AGREEMENT = 0.05

def shape_agreement(first: Visit, moved: np.ndarray, samples: int=SAMPLES, seed: int=0) -> float:
    """How much of the opening and the rock round it `moved` (another visit, already aligned
    into `first`'s frame) shares with `first`: the mean, over both clouds, of the share of
    points within AGREEMENT_MM of the other. Flat rock aligns well with any flat rock, so the
    alignment residual alone can't tell two crevices apart; the opening's shape can."""
    ...

def identify(record_dir: Path, library: Path) -> dict:
    """Which crevice in `library` a record is, from the shape of the rock and the opening.

    Each crevice's latest other visit is aligned to the record on the rock, as for a
    comparison, and scored by `shape_agreement`. The phone's GPS and photos pick the crevice
    in the field; this confirms it, or catches a record filed under the wrong ID."""
    ...

def compare(first_dir: Path, second_dir: Path, out: Path | None=None) -> dict:
    ...

def colour_change(change: np.ndarray, mask: np.ndarray, threshold: float, span_mm: float=30.0) -> np.ndarray:
    """Brown where the surface came closer (infill), blue where it moved back, pale within the threshold."""
    ...

def _visit_summary(visit: Visit) -> dict:
    ...

def _matrix(alignment: Alignment) -> np.ndarray:
    ...

def _round(value, places: int=2):
    ...
