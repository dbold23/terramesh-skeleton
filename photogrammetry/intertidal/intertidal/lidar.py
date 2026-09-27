"""LiDAR depth from the sweep, as a check on the photo model and a fill for what it missed.

On phones with LiDAR the app writes `clips/<id>.depth`: ARKit's scene depth for every few
frames of the sweep with its confidence: 256 x 144 per frame for the sweep's 16:9 video
(256 x 192 in 4:3 formats; the reader takes any size). The photos and the cube stay
the measurement. LiDAR is coarser (a centimetre-scale footprint, a few millimetres of noise,
weak returns from wet rock) but it is active, so it still returns depth from a dark crevice
interior where the photos find nothing to match. It is used two ways, always reported apart
from the photo numbers:

- **Check.** Every LiDAR point is placed in the cube frame with the phone's own camera path
  and its own metric range, independent of the photo reconstruction. How far it lands from
  the photo surface is an independent check on the dense model and on the cube's scale.
- **Fill.** Mouth cells the photos never saw but LiDAR did give a second coverage figure and
  depth and volume "with LiDAR", clearly labelled.

File layout, all little-endian: the 8 bytes `TMDEPTH1`, then per frame a uint32 video frame
index, uint16 width, uint16 height, width x height float16 depths in metres (row-major, NaN or
0 for none), and width x height uint8 confidences (ARKit's 0 low, 1 medium, 2 high; 255 none).
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from . import measure
from .scale import Similarity, umeyama
MIN_CONFIDENCE = 2
MAX_RANGE_M = 1.2

@dataclass
class DepthFrame:
    frame: int
    depth_m: np.ndarray
    confidence: np.ndarray

def read_track(path: Path) -> list[DepthFrame]:
    ...

def write_track(path: Path, frames: list[DepthFrame]) -> None:
    """The app's format, for tests and tools."""
    ...

def cube_from_arkit(views: list[dict], priors: dict) -> tuple[Similarity, float] | None:
    """Similarity taking ARKit's world (m) to the cube frame (mm), from the frames both placed,
    and the RMS camera-position residual in mm."""
    ...

def points(clip, frames: list[DepthFrame], fit: Similarity, stride: int=1) -> np.ndarray:
    """LiDAR points in the cube frame, mm. Ranges keep their own metric scale: only the
    camera path comes from ARKit through `fit`, so scale here is independent of the cube's."""
    ...

def agreement(lidar_mm: np.ndarray, photo_mm: np.ndarray, near_mm: float=300.0, centre: np.ndarray | None=None) -> dict | None:
    """Distance from each LiDAR point to the photo surface, near the crevice."""
    ...

def fill(photo_mm: np.ndarray, lidar_mm: np.ndarray, outline_mm: np.ndarray, cameras_mm: np.ndarray) -> dict:
    """Mouth coverage, depth and volume when LiDAR fills cells the photos did not see."""
    ...
