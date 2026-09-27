"""Umeyama similarity fit and a RANSAC gate.

The fit answers one question only: what single similarity best maps one set of
camera centres onto another.  Its RMSE describes agreement between two pose
sets, not accuracy against ground truth.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

class DegenerateInput(ValueError):
    """The correspondences do not span enough of space to define a similarity."""

@dataclass
class FitResult:
    s: float
    R: np.ndarray
    t: np.ndarray
    matrix_column_major: list
    inliers: np.ndarray
    rmse: float
    median_err: float
    max_err: float
    matched: int
    rejected: int

    @property
    def inlier_count(self) -> int:
        ...

def _as_points(a, name):
    ...

def _rank(points: np.ndarray) -> int:
    """Effective dimensionality of a point set, scale-invariant."""
    ...

def umeyama(src, dst, with_scale: bool=True):
    """Least-squares similarity mapping ``src`` onto ``dst``.

    Returns ``(s, R, t)`` with ``dst ~= s * R @ src + t``.  ``R`` is always a
    proper rotation: when the covariance is degenerate in the reflecting sense
    the sign of the smallest singular value is flipped (Umeyama 1991, eq. 39),
    so a mirrored correspondence set is fitted as the best *rotation*, never as
    a reflection.
    """
    ...

def residuals(src, dst, s, R, t) -> np.ndarray:
    ...

def to_matrix(s, R, t) -> np.ndarray:
    """4x4 homogeneous matrix (row-major numpy) for the similarity."""
    ...

def column_major(matrix: np.ndarray) -> list:
    """Flatten a row-major 4x4 to the column-major 16 the package stores."""
    ...

def from_column_major(values) -> np.ndarray:
    ...

def _report(src, dst, s, R, t, inliers, matched) -> FitResult:
    ...

def fit_ransac(src, dst, threshold: float, iterations: int=500, with_scale: bool=True, seed: int=0) -> FitResult:
    """RANSAC over 3-point minimal sets, refitted on the consensus set.

    ``threshold`` is a distance in the units of ``dst``.  The returned errors and
    RMSE are computed on the inliers of the refitted model.
    """
    ...

def path_length(points) -> float:
    """Length of the polyline through ``points`` in their own units."""
    ...
