import json
import math
import os
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image
import spotted
import synthetic
from terramesh_shark_morphometrics import bodymap
from terramesh_shark_morphometrics.cameras import load_stills

def correlation(a: np.ndarray, b: np.ndarray) -> float:
    """Grey-level correlation over the pixels both maps saw."""
    ...

def best_shifted(a, b, most: int=150) -> float:
    """The best correlation with `a` slid along the body by up to `most` columns either way: a
    frame estimated from the walk alone can place the snout a few centimetres out."""
    ...

def run_worker(tmp_path: Path, export: Path, picks: dict | None) -> Path:
    ...

def test_a_map_puts_the_skin_where_it_is_on_the_animal(tmp_path):
    ...

def test_the_walk_alone_finds_the_axis_but_not_the_head(tmp_path):
    ...

def test_the_same_shark_gives_the_same_maps_from_different_walks(tmp_path):
    ...

def test_handlers_are_never_in_a_map(tmp_path):
    ...

def test_a_masked_still_gives_way_to_the_next_best(tmp_path):
    ...
