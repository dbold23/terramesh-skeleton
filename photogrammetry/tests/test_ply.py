"""PLY header parsing, streaming round trips and the splat LOD writer.

The 59-property header is not invented here: it is read from the real trained
splat at ``runs/curb-02/splat/splat.ply``, so a change in what the trainer emits
breaks these tests rather than passing silently.
"""
import os
import tempfile
import unittest
import numpy as np
from tests.support import SPLAT_PLY, lfs_file_present
from twinlib import ply
import build_twin

def curb02_properties():
    ...

class TestHeader(unittest.TestCase):

    def setUp(self):
        ...

    def test_reads_the_curb02_splat_header(self):
        ...

    def test_streams_in_chunks_without_reading_the_whole_file(self):
        ...

class TestRoundTrip(unittest.TestCase):

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def test_subsample_of_the_real_header_round_trips_exactly(self):
        ...

    def test_ascii_round_trips_through_the_streaming_reader(self):
        ...

    def test_streaming_writer_patches_its_own_count(self):
        ...

    def test_refuses_an_unsupported_format(self):
        ...

    def test_refuses_a_file_that_is_not_ply(self):
        ...

class TestSplatLod(unittest.TestCase):
    """The LOD writer, exercised on a small file with the real 59-property header."""

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def test_writes_a_standard_3dgs_ply_within_budget(self):
        ...

    def test_is_deterministic(self):
        ...

    def test_respects_the_per_cell_cap(self):
        """One dense cell must not be allowed to spend the whole budget."""
        ...
