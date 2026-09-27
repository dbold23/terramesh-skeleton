"""Landmarks in metres from picks on several posed stills.

Each pick is a ray from its still's camera. The rays' least-squares meeting point starts a
Gauss-Newton fit that minimises reprojection error in pixels. Its covariance, scaled by the
larger of the stated pick error and the error the picks actually show, gives each landmark's
uncertainty; a measurement's uncertainty adds both ends' along the line between them, and then
ARKit's own scale uncertainty in quadrature.

ARKit's world is metric because its tracking fuses the IMU with the camera, so no reference
object is needed for a number, but its scale is only good to a couple of percent. That term
dominates anything longer than a head length, which is why calibration cubes on the deck, when
the frames show them, replace it with a measured scale (cubescale.py).
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
import numpy as np
from .cameras import Still, ray_angle_degrees

@dataclass
class Fit:
    point: np.ndarray
    covariance: np.ndarray
    rms_px: float
    residuals_px: list[float]
    angle_degrees: float
    sigma_px: float

class TriangulationError(Exception):
    ...

def ray(still: Still, xy: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ...

def midpoint(rays: list[tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
    ...

def jacobian(still: Still, point: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Projected pixel and its 2x3 derivative with respect to the world point."""
    ...

def triangulate(observations: list[tuple[Still, np.ndarray]], sigma_px: float, iterations: int=15) -> Fit:
    ...

@dataclass
class Distance:
    value: float
    pick_sigma: float
    scale_sigma: float
    sigma: float

def distance(a: Fit, b: Fit, scale_uncertainty: float, factor: float=1.0) -> Distance:
    """Real metres between two landmarks. `factor` is real metres per ARKit metre (1 when ARKit's
    own scale is trusted, or what the calibration cubes measured), `scale_uncertainty` its
    uncertainty as a fraction."""
    ...
