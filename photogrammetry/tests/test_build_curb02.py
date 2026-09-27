"""End to end on the real curb-02 run.

Marked slow: it reads the 284 MB trained splat twice and writes a ~24 MB package
into a temporary directory.  It is the test that would catch a builder that
quietly started claiming metres for a run nothing has ever measured.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from tests.support import CURB02, PHOTOGRAMMETRY, SPLAT_PLY, lfs_file_present, slow
from twinlib import audit, schema
import build_twin
import register_twin

@slow
class TestCurb02Build(unittest.TestCase):
    root = None
    directory = None

    @classmethod
    def setUpClass(cls):
        ...

    @classmethod
    def tearDownClass(cls):
        ...

    def test_the_package_validates(self):
        ...

    def test_the_site_frame_is_local_and_unscaled(self):
        ...

    def test_nothing_claims_metres(self):
        """No transform may be in metres, and none may claim a metric scale source."""
        ...

    def test_the_three_colmap_pieces_are_registered_to_the_realitykit_frame(self):
        ...

    def test_the_site_is_pinned_by_exactly_one_identity(self):
        ...

    def test_the_splat_inherits_the_piece_it_was_trained_on(self):
        ...

    def test_the_mesh_was_copied_with_its_references_rewritten(self):
        ...

    def test_the_audit_chain_verifies_and_matches_the_manifest(self):
        ...

    def test_a_rebuild_without_force_does_nothing(self):
        ...

    def test_two_dry_runs_print_the_same_bytes(self):
        ...
