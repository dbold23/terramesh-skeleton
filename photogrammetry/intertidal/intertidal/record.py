"""A lasting record of one crevice on one visit.

A record is a folder that stands on its own, so it can be kept for years and compared with
the next visit to the same crevice:

  record.json             crevice id, site, when and where, every measurement, the scale check,
                          and the crevice frame (how it sits in the cube frame of that visit)
  crevice-mm.ply          the scaled cloud around the crevice, in the crevice frame, mm
  lidar-mm.ply            the phone's LiDAR points around it, same frame, when it had LiDAR
  mouth-outline.json      the mouth outline in the crevice frame
  depth-map.png           16-bit depth behind each 2 mm cell of the mouth, in 0.1 mm; 0 = not seen
  depth-map.json          how to read the depth map (cell size, origin, units)
  depth-preview.png       the same depth map in colour, for people
  photo.jpg               the frame that looks most squarely into the mouth, to find it again

The crevice frame puts the origin at the centre of the mouth, z into the rock along the
mouth plane's normal, and x along the mouth's long axis. It depends only on the crevice, not
on where the cube happened to sit, so two visits start close to aligned; `compare` finishes
the job on the surrounding rock. The long axis has no preferred direction, so x can come out
reversed between visits, and `compare` tries both.

A library is a folder of records: `<library>/<crevice id>/<visit>/`. Records are only ever
added to it, never changed.
"""
from __future__ import annotations
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np
from . import measure, ply
SCHEMA = 1
CROP_MM = 250.0
CROP_MARGIN_MM = 150.0
VOXEL_MM = 0.5
MAX_VOXEL_MM = 2.0
DEPTH_UNIT_MM = 0.1

def check_crevice_id(crevice_id: str) -> str:
    ...

def crevice_frame(outline_mm: np.ndarray, cameras_mm: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(origin, R) with crevice = R @ (cube - origin). Rows of R are the crevice x, y, z axes."""
    ...

def crop_radius(outline_local: np.ndarray) -> float:
    """How far round the mouth centre a record keeps the rock: 250 mm for an abalone crevice,
    and the mouth's reach plus a margin for a wider one, so the face round a 2 m crevice (and
    the cubes beside it) stays in the record for the next visit's alignment."""
    ...

def record_voxel(crop_mm: float) -> float:
    """The voxel grows with the crop's radius so a wide record stays about as many points."""
    ...

def to_frame(points: np.ndarray, origin: np.ndarray, R: np.ndarray) -> np.ndarray:
    ...

def voxel_downsample(xyz: np.ndarray, rgb: np.ndarray | None, voxel: float) -> tuple[np.ndarray, np.ndarray | None]:
    ...

def depth_map(xyz: np.ndarray, outline_xy: np.ndarray) -> measure.DepthGrid:
    """Depth grid of a cloud already in its crevice frame (z is depth into the rock)."""
    ...

def write_depth_map(grid: measure.DepthGrid, folder: Path, stem: str='depth-map') -> None:
    ...

def colour_depth(grid: measure.DepthGrid, max_depth: float | None=None) -> np.ndarray:
    ...

def pick_photo(run: Path, origin: np.ndarray, R: np.ndarray) -> Path | None:
    """The kept frame whose camera looks most squarely into the mouth from a working distance."""
    ...

def build(run: Path, out: Path, crevice_id: str, site: str | None=None, notes: str | None=None) -> dict:
    """Make a record from a finished run folder (from-export or run)."""
    ...

def visit_name(record: dict) -> str:
    """Folder name of a visit in a library: date, then enough of the survey id to be unique."""
    ...

def _when(record: dict) -> str:
    """When the crevice was filmed, or failing that when the record was made. Records from
    before processed_at call it recorded_at."""
    ...

def add_to_library(record_dir: Path, library: Path) -> Path:
    """Copy a record into the library as the crevice's next visit. The copy's record.json gains
    `visit_index`: 1 for the crevice's first visit, counted in the order they were filmed among
    the visits in the library when it was added. Earlier records are never rewritten, so a
    visit added out of order leaves later ones' indices as they were."""
    ...

def visits(folder: Path) -> list[Path]:
    """The records of one crevice in a library, oldest first."""
    ...

def _captured(folder: Path) -> str:
    ...

def previous_visit(crevice_folder: Path, record: dict) -> Path | None:
    """The latest record in `crevice_folder` from before this record's visit, if any."""
    ...
