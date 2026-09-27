"""Sparse reconstruction with pycolmap, then the cube scale solve on its poses.

Features default to ALIKED keypoints matched with LightGlue (`features.py`), which hold up
better than SIFT on wet rock, low light and the large viewpoint changes of a sweep into a
crevice. SIFT remains available. When the app recorded ARKit camera positions for each
frame, they go into COLMAP as pose priors: they pick which frames to match and they hold
the incremental mapper to one consistent model, which is what keeps a sweep from breaking
into pieces. The cube still sets the scale. ARKit's own metric scale is only compared
against it, as an independent check.

Everything here runs on a Mac CPU. Dense reconstruction is in `dense.py`.
"""
from __future__ import annotations
from collections.abc import Callable
from pathlib import Path
import cv2
import numpy as np
from .cube import Cube
from .frames import read_pixels
from .markers import Detection, detect
from .scale import ScaleReport, View, solve, umeyama

def _quiet(fraction: float, stage: str, detail: str='') -> None:
    ...

def select_pairs(names: list[str], priors: dict | None, window: int=6, neighbours: int=10, max_angle_deg: float=60.0) -> list[tuple[str, str]]:
    """Neighbours in time, plus, with ARKit poses, the nearest cameras that look the same way."""
    ...

def reconstruct(frames_dir: Path, work_dir: Path, intrinsics: tuple[float, float, float, float] | None=None, priors: dict | None=None, features: str='aliked', prior_sigma_m: float=0.03, max_keypoints: int=2048, progress: Progress=_quiet, random_seed: int | None=None, fix_intrinsics: bool=False):
    """Returns (model, info).

    `intrinsics` (fx, fy, cx, cy) seeds the camera, e.g. from the ARKit clip record. COLMAP
    still refines focal length and distortion, unless `fix_intrinsics`: then the focal length
    and principal point stay at ARKit's and only radial distortion is refined. `priors` maps an
    image name to its `export.FramePose`; only frames ARKit tracked normally are used."""
    ...

def prior_agreement(model, priors: dict, mm_per_unit: float) -> dict | None:
    """How well ARKit's own positions and scale agree with the cube-scaled model.

    ARKit's world is in metres, so a perfect ARKit scale would be 1000 mm per ARKit metre."""
    ...

def _centre(image) -> np.ndarray:
    ...

def cube_views(model, frames_dir: Path, cube: Cube) -> tuple[list[View], dict[str, int]]:
    """Detect the cube in every registered frame, undistorting corners through
    the COLMAP camera so the solve uses the same lens model as the poses."""
    ...

def camera_centres(model) -> np.ndarray:
    ...

def camera_views(model) -> list[tuple[str, np.ndarray, np.ndarray]]:
    """(frame name, centre, unit viewing direction) for every registered frame, in model units."""
    ...

def frame_cameras(model, transform) -> dict[str, dict]:
    """Each registered frame's camera in the cube frame: `cam_from_cube`, a 3 x 4 [R | t] taking
    cube millimetres to camera millimetres, and the COLMAP lens (`camera`: model name, size and
    parameters), so a point in the cube frame can be drawn on the frame it was seen in."""
    ...

def scale_model(model, frames_dir: Path, cube: Cube) -> tuple[ScaleReport, dict[str, int]]:
    ...

def points(model) -> tuple[np.ndarray, np.ndarray]:
    ...
