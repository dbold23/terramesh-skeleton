"""The tiled cube must put every tag exactly where cube-spec.json says, fit together, and key
each tile to one face one way round. Skipped when OpenSCAD is not installed."""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import numpy as np
from test_scad_matches_spec import inside, read_ascii_stl

def render(part: str, out: Path) -> subprocess.CompletedProcess:
    ...

@unittest.skipUnless(shutil.which('openscad'), 'OpenSCAD not installed')
class TiledCube(unittest.TestCase):

    def test_tags_sit_where_the_spec_says(self):
        ...

    def test_tiles_fit_the_core(self):
        ...

    def test_each_tile_fits_one_face_one_way(self):
        ...
