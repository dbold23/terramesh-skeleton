"""Minimal PLY vertex reader and writer (ASCII and binary little-endian).

Only vertex positions and optional 8-bit colours; faces are ignored, so a
mesh is read as its vertex cloud. Enough for COLMAP, OpenMVS, VGGT and
MapAnything exports without adding a mesh library.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np

def read(path: Path) -> tuple[np.ndarray, np.ndarray | None]:
    ...

def _read_binary_with_lists(data: bytes, offset: int, count: int, props: list) -> dict[str, np.ndarray]:
    """Binary vertices with list properties, such as the view indices and weights OpenMVS writes.

    Rows vary in length, so this walks them once to find where each starts, then reads the
    fixed-size properties that come before the first list. The lists themselves are skipped.
    """
    ...

def write(path: Path, xyz: np.ndarray, rgb: np.ndarray | None=None, comment: str='') -> None:
    ...
