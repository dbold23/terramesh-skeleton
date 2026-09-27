"""ALIKED keypoints matched with LightGlue, written into a COLMAP database.

COLMAP 4.2 can run ALIKED and LightGlue itself, but only in builds with ONNX Runtime, and
the pycolmap wheels on PyPI (Linux and macOS) are built without it. So this module runs
COLMAP's own released ONNX exports of both networks through the `onnxruntime` package and
hands COLMAP the keypoints and matches. Geometric verification and mapping stay in COLMAP.

The weights are downloaded once into a model cache and checked against a pinned SHA-256.
"""
from __future__ import annotations
import hashlib
import os
import urllib.request
from dataclasses import dataclass
from pathlib import Path
import cv2
import numpy as np

@dataclass(frozen=True)
class Model:
    name: str
    file: str
    url: str
    sha256: str
    licence: str
    source: str

    def to_json(self) -> dict:
        ...

def model_cache() -> Path:
    ...

def fetch(model: Model, cache: Path | None=None) -> Path:
    """Path to the verified weights, downloading them on first use."""
    ...

def _sha256(path: Path) -> str:
    ...

@dataclass
class Features:
    keypoints: np.ndarray
    descriptors: np.ndarray
    size: tuple[int, int]
    scale: float

class Matcher:

    def __init__(self, max_keypoints: int=2048, max_side: int=1600, min_score: float=0.2, cache: Path | None=None):
        ...

    def extract(self, image: np.ndarray) -> Features:
        """`image` is BGR as read by OpenCV."""
        ...

    def match(self, a: Features, b: Features) -> np.ndarray:
        """M x 2 indices into a and b."""
        ...

def colmap_keypoints(f: Features) -> np.ndarray:
    """Network pixels -> original-image COLMAP coordinates (pixel centres at +0.5)."""
    ...
