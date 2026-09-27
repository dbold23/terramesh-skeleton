"""A ray-cast 3D scene for end-to-end runs: a textured rock face with a slot crevice and
the calibration cube sitting on it, filmed along a handheld-like arc.

World frame is millimetres, rock face z = 0 facing +z. The cube sits on the face with its
centre at (0, 0, 20), axes aligned with the world, so cube frame = world - (0, 0, 20).
The slot mouth is SLOT_W along x and SLOT_H along y, centred at SLOT_CENTRE, and runs
SLOT_D into the rock.
"""
from __future__ import annotations
import numpy as np
from synthetic import SPEC, face_texture, look_at
SLOT_W, SLOT_H, SLOT_D = (120.0, 40.0, 90.0)

class Noise:
    """Smooth 3D value noise over the scene box, a sum of octaves, trilinear."""

    def __init__(self, seed=0, lo=(-500, -500, -100), hi=(500, 500, 5), cells=(10.0, 4.0, 2.0)):
        ...

    def __call__(self, p: np.ndarray) -> np.ndarray:
        ...

def _patches():
    """(origin, axis_u, axis_v, normal, extent_u, extent_v, kind) for every surface."""
    ...

def _trace(K: np.ndarray, R: np.ndarray, t: np.ndarray, size) -> tuple:
    """Nearest hit along every pixel's ray: (depth along the optical axis, patch index, patch uv, points)."""
    ...

def render_depth(K: np.ndarray, R: np.ndarray, t: np.ndarray, size=(256, 192)) -> np.ndarray:
    """Depth along the optical axis in mm (inf where the ray hits nothing), like ARKit scene depth."""
    ...

def render(K: np.ndarray, R: np.ndarray, t: np.ndarray, size=(1280, 960)) -> np.ndarray:
    """BGR image from an OpenCV camera (camera_from_world R, t in mm)."""
    ...

def sweep(frames: int, target=np.array([70.0, 0.0, -15.0])) -> list[tuple[np.ndarray, np.ndarray]]:
    """camera_from_world (R, t) along an arc over the cube and the slot mouth."""
    ...
