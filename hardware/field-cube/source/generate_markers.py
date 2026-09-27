"""Generate Field Cube marker artwork, OpenSCAD cells, and nominal corner data.

Requires Python 3, NumPy, and Pillow. Upstream assets are cached in markers/upstream;
subsequent runs are offline. Do not resize a printed calibration target without
updating its measured dimensions. SVGs specify millimetres; print at 100%.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from urllib.request import urlopen
import numpy as np
from PIL import Image, ImageDraw, ImageFont
TAG_MM = 64.0
CELL_MM = 8.0
LABEL_MM = 80.0
TILE_MM = 84.0

def cache(name: str, url: str) -> Path:
    ...

def svg_cells(cells: list[list[int]], margin: float) -> str:
    ...

def write_artwork(tag_id: int, cells: list[list[int]], size_mm: float, suffix: str) -> None:
    ...

def nominal_config() -> dict:
    ...

def main() -> None:
    ...
