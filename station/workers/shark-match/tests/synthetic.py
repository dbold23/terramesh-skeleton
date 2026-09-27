"""Synthetic spotted sharks and phone exports shaped like the app's, for tests.

Each individual has its own spot pattern per view. Each encounter photographs it with a
different pose, scale, light and background, so the same animal is never the same picture.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
import uuid
import zipfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
WIDTH, HEIGHT = (960, 720)

def spots(individual: str, view: str) -> np.ndarray:
    ...

def photograph(individual: str, view: str, encounter_seed: int) -> tuple[Image.Image, dict]:
    """Returns the image and the normalised body box, as the phone's journal would record it."""
    ...

def make_catalog_photos(folder: Path, individuals: list[str], encounters: int, views: list[str]) -> Path:
    """Writes photos plus the import CSV `catalog import` reads. Returns the CSV path."""
    ...

def pose(seed: int) -> list[float]:
    ...

def make_export(folder: Path, individual: str, views: list[str], *, seed: int, mission: str='oseaShark', journal: bool=True) -> Path:
    """Writes an unpacked export: manifest, frames.jsonl, images/ and shark-encounter/frames.jsonl."""
    ...

def add_snapshot_json(folder: Path) -> None:
    """What Station adds when it unpacks an export (WORKERS.md section 4)."""
    ...

def zip_export(folder: Path, target: Path) -> Path:
    ...
