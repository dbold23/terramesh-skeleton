"""Audit one COLMAP model without changing it or claiming metric accuracy.

Run with the project's PyCOLMAP environment. The COLMAP model is loaded by
PyCOLMAP; residual/track/angle distributions use temporary disk-backed arrays,
and the complete finite colored point cloud is written incrementally.
"""
from __future__ import annotations
import argparse
import collections
import json
import math
import os
from pathlib import Path
import random
import tempfile
from urllib.parse import quote
import numpy as np
import pycolmap

class Distribution:
    """Exact finite-value quantiles with disk-backed storage, bounded by input."""

    def __init__(self, path: Path, capacity: int):
        ...

    def append(self, value: float):
        ...

    def summary(self):
        ...

def safe_json(value):
    ...

def write_json(path: Path, value):
    ...

def selected_indices(length: int, limit: int):
    ...

def reservoir_add(items, value, seen: int, limit: int, rng):
    ...

def frame_lookup(path: Path | None):
    ...

def image_reference(name: str, image_root: Path, output: Path):
    ...

def analyze(model_dir: Path, images_dir: Path, output_dir: Path, manifest_path: Path | None=None, max_points: int=50000):
    ...

def self_test():
    """Deterministic small model: exact counts and deliberately unequal errors."""
    ...

def main():
    ...
