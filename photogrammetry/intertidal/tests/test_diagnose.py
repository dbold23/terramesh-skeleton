"""The sweep diagnosis reads frame timing, motion, the guide and LiDAR from an export alone."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
import numpy as np
import make_export
from intertidal import diagnose
from scene import SLOT_CENTRE, SLOT_D

class DiagnoseTests(unittest.TestCase):

    def test_a_synthetic_sweep_reads_back(self):
        ...

    def test_stalls_show_as_gaps(self):
        ...
