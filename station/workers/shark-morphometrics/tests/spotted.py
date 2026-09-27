"""A synthetic spotted shark on the generic body, photographed by a walk round, for body-map tests.

The animal's spots are fixed in body coordinates (s along precaudal length, phi round the body),
so the same individual can be laid anywhere in the world, pointing any way, and photographed from
a different walk each encounter. Stills are stored as the app stores them: landscape pixels with
EXIF orientation 6, ARKit's camera-to-world transform and intrinsics, column-major.
"""
from __future__ import annotations
import hashlib
import json
import math
import uuid
from pathlib import Path
import numpy as np
from PIL import Image
from terramesh_shark_morphometrics.bodymap import PCL_OF_TOTAL, BodyFrame

def arkit_transform(centre: np.ndarray, target: np.ndarray) -> np.ndarray:
    """world_from_camera with ARKit's camera axes (x right, y up, looking down -z)."""
    ...

def project(transform: np.ndarray, K: np.ndarray, point: np.ndarray) -> tuple[np.ndarray, float]:
    ...
WIDTH, HEIGHT = (1280, 960)
FOCAL = 1000.0

def spot_pattern(individual: str, count: int=160) -> np.ndarray:
    """(s, phi degrees, radius in PCL) for each spot, over the whole body."""
    ...

def skin(individual: str, s: np.ndarray, phi: np.ndarray, pcl_depth_scale: float=0.08) -> np.ndarray:
    """RGB of the skin at body coordinates, spots as dark discs measured on the surface."""
    ...

def body_frame(snout, heading_degrees: float, pcl: float, mission: str='oseaShark') -> BodyFrame:
    ...

def surface_samples(individual: str, frame: BodyFrame):
    """Dense points on the body with their normals and skin colour, computed once per walk."""
    ...

def photograph(samples, transform: np.ndarray, K: np.ndarray, size: tuple[int, int], background: tuple[int, int, int]) -> np.ndarray:
    """Splats the body's visible surface into a still, nearest surface first per pixel."""
    ...

def walk_cameras(centre: np.ndarray, facing_degrees: float, azimuths=range(-70, 71, 14), heights=(0.1, 0.55, 1.0), standoff=1.7):
    ...

def make_walk(folder: Path, individual: str, *, seed: int, snout=(-0.7, 0.3, 0.1), heading: float=0.0, pcl: float=1.3, facing: float=0.0, mission: str='oseaShark', total_length: float | None=None, masks: dict[int, tuple[float, float, float, float]] | None=None) -> dict:
    """Writes a phone export of one walk round `individual`. The animal lies with its snout at
    `snout`, pointing along `heading` degrees (0 = +x), and the photographer walks round the side
    at `facing` degrees (0 = +z, the animal's right when heading is 0). `masks` maps a still's
    index to a normalised upright box written as that still's person mask."""
    ...

def picks_for(folder: Path, walk: dict, every: int=2) -> dict:
    """A pick.html landmarks file for the walk's snout, caudal origin and dorsal apex."""
    ...

def truth_map(individual: str, view: str, width: int=1024, height: int=320) -> np.ndarray:
    """The skin drawn straight into a view's map coordinates, for comparing with a rendered map."""
    ...
