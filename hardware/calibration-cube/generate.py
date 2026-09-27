"""Generate the tag geometry for the TerraMesh intertidal calibration cube.

This script is the single source of truth for where every AprilTag corner sits
on the cube. It writes three files that must stay in sync:

  tag_bits.scad      bit patterns + face frames consumed by calibration_cube.scad
  cube-spec.json     metric 3D corner coordinates consumed by the scale solver
                     (photogrammetry/intertidal) and the phone app
  stickers.svg       1:1 sticker sheet for printing the tags on waterproof vinyl
                     instead of (or as well as) inlaying them in the print

Cube frame: origin at the cube centre, +Z out of the top face, millimetres.
The bottom face (-Z) carries either the handle socket or a sixth tag. Its tag id
comes from a separate block (500 + cube index), so cube 0's bottom tag never
collides with cube 1's side tags. The spec always lists it: a cube printed with
the socket simply never shows it.

Corner order matches OpenCV's ArUco/AprilTag detector: top-left, top-right,
bottom-right, bottom-left, as the tag is seen from outside the cube with its
"up" edge towards the face's w axis.

Usage:
  python3 generate.py                     # cube 0, 40 mm edge, 4 mm cells
  python3 generate.py --cube-index 1      # second cube: tags 5..9, bottom 501
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import cv2
import numpy as np
TAG_CELLS = 8
TAGS_PER_CUBE = 5
BOTTOM_TAG_BASE = 500

def bottom_tag_id(cube_index: int) -> int:
    ...

def tag_bits(tag_id: int) -> np.ndarray:
    """8x8 array, 1 = black cell, row 0 at the top of the tag."""
    ...

def build_spec(edge_mm: float, cell_mm: float, cube_index: int) -> dict:
    ...

def write_scad(spec: dict, path: Path) -> None:
    ...

def write_svg(spec: dict, path: Path) -> None:
    """A4 sheet, 1 SVG unit = 1 mm, with a 50 mm check bar to verify print scale."""
    ...

def main() -> None:
    ...
