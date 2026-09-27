"""The encounter's posed stills: every arc-pass still and every confirmed view.

Each still is an ordinary frame record with ARKit's camera-to-world transform (metres,
column-major, camera looking down -z with y up) and intrinsics for the sensor's landscape pixels.
The JPEG keeps those landscape pixels and carries an EXIF orientation so photo viewers show it
upright. Everything here works in the stored pixels, never the turned picture, because that is
what the intrinsics describe. Picks are stored in the same pixels.
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from PIL import Image

class SnapshotError(Exception):
    ...

@dataclass
class Still:
    frame_id: str
    path: Path
    reason: str
    captured_at: float
    width: int
    height: int
    orientation: int
    K: np.ndarray
    R: np.ndarray
    t: np.ndarray
    azimuth: float | None = None
    band: str | None = None

    @property
    def centre(self) -> np.ndarray:
        ...

    @property
    def P(self) -> np.ndarray:
        ...

    @property
    def label(self) -> str:
        ...

    def project(self, point: np.ndarray) -> tuple[np.ndarray, float]:
        ...

def column_major(values, size: int) -> np.ndarray | None:
    ...

def orientation_of(image: Image.Image) -> int:
    ...

def load_stills(snapshot: Path, every_frame: bool=False) -> tuple[list[Still], list[str]]:
    """Every usable posed still, in capture order, and sentences about any that were skipped.

    `every_frame` takes every posed frame that has an image, not only the arc stills and confirmed
    views: the calibration cubes can be found in any of them."""
    ...

def ray_angle_degrees(stills: list[Still], point: np.ndarray) -> float:
    """The widest angle between any two of these cameras' rays to `point`."""
    ...
