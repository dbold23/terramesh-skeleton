"""The registration gates and the tag-report significance rule.

These are the two places where the package decides what it is allowed to claim,
so they are tested on their own rather than only through a build.
"""
import json
import os
import shutil
import tempfile
import unittest
import numpy as np
from tests.support import PHOTOGRAMMETRY
from twinlib import arkit, similarity
import build_twin
import register_twin

class FakeFrame:
    """Just enough of twinlib.arkit.Frame for the reference-centre helper."""

    def __init__(self, name, centre, tracking='normal'):
        ...

    @property
    def centre(self):
        ...

    @property
    def is_normal(self):
        ...

def walk(count=20, spacing=0.5, wobble=0.3):
    """A short walk that is not a straight line, so a similarity is determined."""
    ...

class TestGates(unittest.TestCase):

    def test_too_few_matches_is_unregistered_with_a_reason(self):
        ...

    def test_a_good_fit_is_registered_and_carries_its_numbers(self):
        ...

    def test_a_bad_fit_is_refused_above_three_percent(self):
        ...

    def test_frames_without_normal_tracking_are_dropped(self):
        ...

    def test_the_join_is_exact_not_fuzzy(self):
        ...

    def test_collinear_cameras_are_refused_with_a_clear_reason(self):
        ...

    def test_icp_refuses_to_pretend(self):
        ...

    def test_control_points_need_three_pairs(self):
        ...

    def test_control_points_fit_rigidly_when_both_visits_are_metric(self):
        ...

    def test_a_segment_without_a_placement_is_unregistered(self):
        ...

    def test_a_placed_segment_keeps_its_vertical_unresolved(self):
        ...

class TestTagReport(unittest.TestCase):
    """The significance rule, on a package small enough to write by hand."""

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def write_package(self, uncertainty_b=0.02):
        ...

    def report(self):
        ...

    def test_a_large_change_is_significant(self):
        ...

    def test_a_missing_uncertainty_gives_no_verdict(self):
        ...

    def test_different_method_versions_are_never_subtracted(self):
        ...
