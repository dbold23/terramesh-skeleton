"""Find the calibration cube in a frame and, given intrinsics, its metric pose."""
from __future__ import annotations
from dataclasses import dataclass, field
import cv2
import numpy as np
from .cube import Cube

@dataclass
class Detection:
    """Cube tags seen in one frame. Corners are pixels in OpenCV order."""

    @property
    def tag_count(self) -> int:
        ...

    def tag_edge_px(self) -> float:
        """Mean tag edge length in pixels, the capture guide's closeness signal."""
        ...

@dataclass
class CubePose:
    rvec: np.ndarray
    tvec: np.ndarray
    reprojection_rms_px: float
    tags_used: int

    @property
    def distance_mm(self) -> float:
        ...

def _detector() -> cv2.aruco.ArucoDetector:
    ...

def detect(image: np.ndarray, cube: Cube, enhance: bool=True) -> Detection:
    """Detect the cube's tags. `enhance` retries with local contrast
    equalisation, which recovers tags in the shade of a crevice mouth."""
    ...

def _run(detector: cv2.aruco.ArucoDetector, gray: np.ndarray, cube: Cube) -> Detection:
    ...

def estimate_pose(detection: Detection, cube: Cube, K: np.ndarray, dist: np.ndarray | None=None) -> CubePose | None:
    """Metric pose of the cube in the camera frame from every visible corner."""
    ...

def glare_fraction(image: np.ndarray, detection: Detection, threshold: int=250) -> float:
    """Share of tag pixels that are clipped. Wet rock and wet tags glare; above
    a few percent the corners are no longer trustworthy."""
    ...
