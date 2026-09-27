"""The anchor bottom: a sealed ballast pocket, a cord loop, and the tags where the spec says.

Skipped when OpenSCAD is not installed."""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import numpy as np
from test_scad_matches_spec import inside, read_ascii_stl

def scad_constant(name: str) -> float:
    ...

@unittest.skipUnless(shutil.which('openscad'), 'OpenSCAD not installed')
class Anchor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ...

    def test_pocket_is_sealed_and_holds_shot_below_the_pause(self):
        ...

    def test_cord_loop_is_open_through(self):
        ...

    def test_side_and_top_tags_unchanged(self):
        ...
