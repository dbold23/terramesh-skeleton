"""COLMAP model reader, in the camera convention the twin package stores.

COLMAP stores ``cam_from_world`` in the OpenCV convention (+X right, +Y down,
+Z forward).  The package stores ``camera_to_world`` in the ARKit convention
(+X right, +Y up, -Z forward), so every camera-to-world is post-multiplied by a
180 degree rotation about X.  Camera centres are identical in both conventions,
which is why registration fits centres.

COLMAP frames carry no metric scale.  Nothing here invents one; scale arrives
only from a fit against an ARKit or RealityKit trajectory.
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
import numpy as np

@dataclass
class CameraPose:
    name: str
    image_id: int
    centre: np.ndarray
    camera_to_world: np.ndarray
    camera_id: int
    width: int
    height: int
    fx: float
    fy: float
    cx: float
    cy: float
    model: str

@dataclass
class Model:
    path: str
    piece: str
    poses: dict
    point_count: int
    image_count: int
    mean_reprojection_error: float | None = None

    def names(self) -> list:
        ...

    def centres(self, names=None) -> np.ndarray:
        ...

def _intrinsics(camera):
    """(fx, fy, cx, cy) for the camera models this project produces."""
    ...

def read_model(path, piece: str | None=None) -> Model:
    """Read a COLMAP model directory (``cameras.bin``/``images.bin``/``points3D.bin``)."""
    ...

def read_points(path):
    """``points3D`` as ``(xyz float32 (n,3), rgb uint8 (n,3))``."""
    ...

def find_models(sparse_dir) -> list:
    """Sorted model sub-directories under a ``sparse/models`` directory."""
    ...
