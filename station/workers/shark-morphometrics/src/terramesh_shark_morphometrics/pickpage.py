"""`pick.html`: the page a person uses to place landmarks on the encounter's stills.

The page opens from the layer folder in any browser, with nothing fetched. It shows a spread of
arc-pass stills and the confirmed views, upright and downsized, with each still's camera. Once a
landmark is picked on one still, the others show the line it must lie on; once it is picked on
two, they show where it should be, so a wrong pick stands out. "Save landmarks" downloads
`<survey id>.json`, which goes in Station's shark-landmarks input folder; the next run measures
from it.

Picks are stored in the stored (unturned, full size) pixels, because that is what the phone's
intrinsics describe. Each view carries its display camera and the map back to stored pixels.
"""
from __future__ import annotations
import html
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps
from .cameras import Still
from .landmarks import landmarks_for, measurements_for

def upright_map(orientation: int, width: int, height: int) -> tuple[np.ndarray, tuple[int, int]]:
    """3x3 map from stored pixel coordinates to upright ones (PIL's exif_transpose), and the
    upright size. Coordinates are continuous: (0, 0) is the corner of the first pixel."""
    ...

def choose(stills: list[Still], picked: set[str], count: int) -> list[Still]:
    """Every still that already has a pick, every confirmed view, then arc stills spread evenly
    round the animal until there are `count`."""
    ...

def write(out: Path, *, survey_id: str, survey_name: str, mission: str, species: str, stills: list[Still], picks: list[dict], picker: str, sigma_px: float, display_edge: int) -> list[str]:
    """Writes pick.html and pick/NN.jpg. Returns the frame IDs shown."""
    ...
