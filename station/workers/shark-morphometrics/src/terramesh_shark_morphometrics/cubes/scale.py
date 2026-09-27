"""Put a structure-from-motion model into cube millimetres.

SfM recovers the scene up to an unknown similarity: any rotation, translation
and scale fit the images equally well. The cube's tag corners are points whose
millimetre coordinates we know. Triangulating them in the SfM frame and fitting
a similarity to their known positions fixes all seven unknowns at once, and the
fit residual is a direct, per-capture measure of how far to trust the scale.

Several cubes can share a scene (along a long crevice, round a shark on a deck). Nobody
measures where they sit relative to each other, so each gets its own rotation and
translation, but they all share the one scale: a joint Umeyama fit. Each cube's own scale is
also fitted alone; with three or more cubes, one that disagrees with the rest by more than
CUBE_SCALE_TOLERANCE_PCT (misprinted, the wrong caliper reading, knocked mid-sweep) is left out
of the scale, and with two, a disagreement is flagged. The output frame is the frame of the
cube with the most corners seen.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .cube import FIELD_CUBE_IDS, Cube
from .markers import Detection
CUBE_SCALE_TOLERANCE_PCT = 1.0

@dataclass
class View:
    K: np.ndarray
    R: np.ndarray
    t: np.ndarray
    detection: Detection

@dataclass
class Similarity:
    """cube_mm = scale * R @ sfm + t"""
    scale: float
    R: np.ndarray
    t: np.ndarray

    def apply(self, points: np.ndarray) -> np.ndarray:
        ...

    def as_matrix(self) -> np.ndarray:
        ...

@dataclass
class CubeFit:
    """One printed cube's part in the solve."""
    index: int
    tags: list[int]
    points: int
    transform: Similarity
    own_scale_pct: float
    rms_mm: float
    centre_mm: np.ndarray
    in_scale: bool
    frame_from_cube: np.ndarray | None = None

    def to_json(self) -> dict:
        ...

@dataclass
class ScaleReport:
    transform: Similarity
    tags_used: list[int]
    points_used: int
    rms_mm: float
    max_mm: float
    scale_spread_pct: float
    warnings: list[str]
    frame_cube: int = 0
    cubes: list[CubeFit] | None = None

    @property
    def trustworthy(self) -> bool:
        ...

    def to_json(self) -> dict:
        ...

def triangulate(views: list[tuple[np.ndarray, np.ndarray]], min_angle_deg: float=2.0) -> np.ndarray | None:
    """Linear multi-view triangulation. `views` holds (3x4 projection, pixel) pairs.
    Returns None when the rays are too close to parallel to fix depth."""
    ...

def umeyama(src: np.ndarray, dst: np.ndarray) -> Similarity:
    """Least-squares similarity taking src to dst (Umeyama 1991)."""
    ...

def umeyama_shared(groups: list[tuple[np.ndarray, np.ndarray]]) -> list[Similarity]:
    """Least-squares fit of one scale and a rotation and translation per group, taking each
    group's src to its dst. With one group it is `umeyama`."""
    ...

def fit(keys: list[tuple[int, int]], sfm: np.ndarray, cube: Cube) -> ScaleReport:
    """Fit cube millimetres to cube corners already located in some other frame.

    `keys` are (tag id, corner 0-3) and `sfm` the matching points in that frame (any units).
    This is the whole solve for anyone with their own triangulation (the shark worker with
    ARKit poses); `solve` triangulates from views first."""
    ...

def _wrong_size_tags(keys: list[tuple[int, int]], sfm: np.ndarray, cube: Cube, tolerance: float=1.4) -> dict[int, float]:
    """Tags whose edge, in the triangulation's units per printed millimetre, is more than
    `tolerance` times off the median of the tags: {tag id: how many times too big}."""
    ...

def _pose_at_scale(src: np.ndarray, dst: np.ndarray, scale: float) -> tuple[np.ndarray, np.ndarray]:
    ...

def solve(views: list[View], cube: Cube) -> ScaleReport:
    ...
