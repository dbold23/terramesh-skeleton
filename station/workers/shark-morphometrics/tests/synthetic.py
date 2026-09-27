"""A synthetic handled shark photographed by the arc pass, shaped like the app's export.

The shark's landmarks are known points in ARKit's world. Each arc still is a pinhole camera on a
ring round the animal at three heights, stored as the app stores it: landscape pixels with EXIF
orientation 6, ARKit's camera-to-world transform and intrinsics, column-major.
"""
from __future__ import annotations
import hashlib
import json
import math
import uuid
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw
from terramesh_shark_morphometrics.cubescale import all_cubes
WIDTH, HEIGHT = (1920, 1440)
FOCAL = 1380.0

def world_points(body: dict) -> dict[str, np.ndarray]:
    ...

def arkit_transform(centre: np.ndarray, target: np.ndarray) -> np.ndarray:
    """world_from_camera with ARKit's camera axes (x right, y up, looking down -z)."""
    ...

def project(transform: np.ndarray, K: np.ndarray, point: np.ndarray) -> tuple[np.ndarray, float]:
    ...

def arc_cameras(centre: np.ndarray, azimuths=range(-80, 81, 16), heights=(-0.2, 0.25, 0.8), standoff=1.6):
    ...

def cube_frame(yaw_degrees: float) -> np.ndarray:
    """World-from-cube rotation for a cube sitting flat: its tagged top (+z) faces up."""
    ...

def tag_texture(tag_id: int, cell: int=24) -> np.ndarray:
    """A cube face: the 8 x 8 cell tag inside a one-cell white margin, as printed."""
    ...

def draw_tags(pixels: np.ndarray, transform: np.ndarray, K: np.ndarray, corners: dict, normals: dict, rotation: np.ndarray, origin: np.ndarray, printed: float=1.0, from_above_only: bool=False) -> None:
    """Paints tags (corners in mm in their set's frame) into the still, in perspective, each with a
    one-cell white margin. `from_above_only` hides tags facing down, as a deck or a pole would."""
    ...

def draw_cube(pixels: np.ndarray, transform: np.ndarray, K: np.ndarray, index: int, centre: np.ndarray, yaw_degrees: float, printed: float=1.0) -> None:
    """Paints cube `index`'s visible faces into the still, in perspective. `printed` is the
    size it came off the printer at."""
    ...

def draw_bar(pixels: np.ndarray, transform: np.ndarray, K: np.ndarray, origin: np.ndarray) -> None:
    """Paints the scale bar lying along the animal (+x), top tags up; the tags under the plates
    face the deck and are not seen."""
    ...

def make_export(folder: Path, *, seed: int, mission: str='oseaShark', stored_scale: float=1.0, phone_total_length: float | None=None, azimuths=range(-80, 81, 16), size: tuple[int, int]=(WIDTH, HEIGHT), focal: float=FOCAL, arkit_scale: float=1.0, pose_noise_mm: float=0.0, cubes=(), moved: dict | None=None, printed: dict | None=None, bar: tuple | None=None) -> dict:
    """Writes the export. Returns {"survey": id, "frames": [...], "truth": {landmark: point},
    "K": stored-pixel intrinsics} for making picks.

    `arkit_scale` stretches the camera positions the export records, as a wrong ARKit scale
    would; the pictures and picks stay true. `pose_noise_mm` jitters the recorded positions.
    `cubes` is (index, offset from the snout in metres, yaw degrees) for cubes on the deck;
    `moved` maps a cube index to a new offset from the second half of the pass on, and `printed`
    to the size it was printed at. `bar` is the scale bar's origin (plate A's tag centre) as an
    offset from the snout; the bar lies along the animal."""
    ...

def picks_for(export: dict, landmarks=None, *, noise_px: float=1.0, every: int=3, seed: int=0, picker: str='Test') -> dict:
    """A landmarks file as pick.html saves it: each landmark picked on every `every`-th still
    that sees it, with Gaussian pick error."""
    ...

def add_snapshot_json(folder: Path) -> None:
    """What Station adds when it unpacks an export (WORKERS.md section 4)."""
    ...
