"""Umeyama and the RANSAC gate."""
import unittest
import numpy as np
from tests.support import PHOTOGRAMMETRY
from twinlib import similarity

def random_rotation(rng):
    ...

class TestUmeyama(unittest.TestCase):

    def test_recovers_a_random_similarity(self):
        ...

    def test_matrix_round_trips_through_column_major(self):
        ...

    def test_rotation_is_never_a_reflection(self):
        """A mirrored correspondence set must not be fitted as a reflection."""
        ...

    def test_collinear_input_is_refused(self):
        ...

    def test_coincident_input_is_refused(self):
        ...

    def test_too_few_points_is_refused(self):
        ...

class TestRansac(unittest.TestCase):

    def test_survives_thirty_percent_outliers(self):
        ...

    def test_is_deterministic_for_a_seed(self):
        ...

    def test_rigid_fit_keeps_unit_scale(self):
        ...

    def test_path_length(self):
        ...
