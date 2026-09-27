"""The printed tags must match cube-spec.json cell for cell.

Renders the "ink" part with OpenSCAD, then ray-casts a point under the centre of
every cell of every tag to check that black cells are solid and white cells are
empty. Skipped when OpenSCAD is not installed.
"""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import numpy as np

def read_ascii_stl(path: Path) -> np.ndarray:
    ...

def inside(triangles: np.ndarray, point: np.ndarray) -> bool:
    """Odd number of crossings along a skewed ray means the point is inside."""
    ...

@unittest.skipUnless(shutil.which('openscad'), 'OpenSCAD not installed')
class ScadMatchesSpec(unittest.TestCase):

    def test_every_cell(self):
        ...
