"""Picking the crevice by hand, on the survey's own frames.

The automatic search starts from a seed: the phone's lock-on, the point the cameras were
aimed at, or the cube. On boulder rubble every one of them can miss, or land on the wrong
hollow. `pick.html` shows a handful of the survey's frames with what was measured drawn on
them. Clicking a frame gives the point on the rock under the cursor, in cube millimetres,
because each frame carries a map from its pixels to the surface the camera saw there. One
click on the deepest part of the crevice makes a seed; several clicks round the opening make a
traced mouth. The page writes
the `measure` command to run with either.

The page is one self-contained file, with nothing fetched, so it opens straight from the
run folder in any browser.
"""
from __future__ import annotations
import base64
import json
from pathlib import Path
import cv2
import numpy as np
from . import measure, ply
from .frames import read_pixels
IMAGE_EDGE = 960
MAP_EDGE = 320
MISSING = -32768

def load_views(out: Path) -> list[dict]:
    """frames-mm.json, with each frame's lens and pose. Runs made before frames-mm.json
    carried them read them from the COLMAP model and the cube scale."""
    ...

def to_camera(view: dict, points: np.ndarray) -> np.ndarray:
    ...

def to_pixels(camera: dict, cam: np.ndarray) -> np.ndarray:
    """COLMAP's projection for the lens models the pipeline uses; (0, 0) is the corner of the
    first pixel."""
    ...

def rock_map(view: dict, points: np.ndarray, edge: int=MAP_EDGE) -> np.ndarray:
    """rows x cols x 3 int16: the nearest point of the cloud behind each map pixel, in cube mm,
    MISSING where the camera saw none. The map covers the frame at `edge` px on its long side."""
    ...

def _turn(path: Path, raw: np.ndarray) -> int | None:
    """The cv2.rotate code that shows a frame upright, from its EXIF orientation; None if upright."""
    ...

def _turn_points(uv: np.ndarray, turn: int | None, w: float, h: float) -> np.ndarray:
    ...

def _visible(view: dict, point: np.ndarray) -> bool:
    ...

def choose(views: list[dict], target: np.ndarray | None, count: int) -> list[dict]:
    """`count` frames spread through the survey, from those that show `target` well inside
    the picture, or from all of them when none do."""
    ...

def frame_data(out: Path, view: dict, points: np.ndarray, marks: dict[str, np.ndarray]) -> dict | None:
    ...

def write_page(out: Path, count: int=8, cloud: Path | None=None) -> Path:
    """Write out/pick.html for the run folder `out`."""
    ...
