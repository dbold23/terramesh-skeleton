"""The WGS84 tangent plane and segment re-basing."""
import math
import unittest
import numpy as np
from tests.support import PHOTOGRAMMETRY
from twinlib import earth

class TestEastNorth(unittest.TestCase):

    def test_a_point_on_the_reference_is_the_origin(self):
        ...

    def test_matches_the_local_metres_per_degree(self):
        """One arcsecond north is about 30.8 m at this latitude; check both axes."""
        ...

    def test_round_trips_through_coordinate(self):
        ...

    def test_refuses_an_invalid_or_distant_coordinate(self):
        ...

class TestRebase(unittest.TestCase):
    """Two segments 50 m apart must land 50 m apart in the site frame."""

    def setUp(self):
        ...

    def test_the_offset_is_recovered_to_a_micrometre(self):
        ...

    def test_rebasing_shifts_the_second_segment_by_that_offset(self):
        ...

    def test_rebasing_keeps_the_segment_rotation(self):
        ...

    def test_refuses_a_segment_beyond_the_tangent_plane(self):
        ...
