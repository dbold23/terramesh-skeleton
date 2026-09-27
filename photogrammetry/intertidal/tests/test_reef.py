"""A reef from strips: joins through shared cubes and ARKit, levelling, one tide tie, zone areas."""
import argparse
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
import cv2
import numpy as np
from intertidal import ply, reef
from intertidal.__main__ import cmd_reef
from intertidal.scale import Similarity
MLLW_AT_WORLD_ZERO = 0.9

def rotation(axis, degrees):
    ...

def pose(R, t):
    ...

def surface(x, y):
    """A rock platform, mm: a gentle rise seaward with boulders and gullies."""
    ...

def world_points(x0, x1, y0=0.0, y1=2500.0, step=20.0, seed=0):
    ...

class Scene:
    """Strips, each in the frame of one of its cubes (as a run's scale.json leaves it)."""

    def strip(self, name, x0, x1, cubes, frame_cube, tilt=0.0, arkit_drift=None, tie=None, seed=0, wet_z=None):
        ...

def rock_colours(points, wet_z, seed=0):
    """Grey-brown rock with patchy colour, darker below the wet line (world z, mm)."""
    ...

def placed_error(placed, truths, name, reference):
    """Largest gap, mm, between where the reef puts a strip's points and where they belong."""
    ...

class JoinTests(unittest.TestCase):

    def test_strips_join_through_shared_cubes(self):
        ...

    def test_a_strip_with_no_shared_cube_joins_through_arkit_and_rock(self):
        ...

    def test_a_cube_moved_between_strips_is_left_out(self):
        ...

    def test_strips_that_cannot_be_joined_are_named(self):
        ...

def write_run(folder: Path, strip: reef.Strip, captured: datetime):
    ...

class ReefCommandTests(unittest.TestCase):

    def test_reef_is_levelled_tied_to_the_tide_and_zoned(self):
        ...

    def test_dry_strips_only_give_lower_limits(self):
        ...

def station_tide(t):
    """The station's water, m above its MLLW, at unix seconds t."""
    ...

def site_tide(t, ratio=1.12, lag_min=25.0, shift=-0.1):
    ...

def rising_taps(start, count=16, every_min=9.0, noise_m=0.012, seed=0):
    """Taps on a rising tide: (unix seconds, the site's water, m)."""
    ...

class LocalTideTests(unittest.TestCase):

    def setUp(self):
        ...

    def test_lag_and_range_come_back_from_the_taps(self):
        ...

    def test_too_few_or_too_flat_taps_say_what_is_missing(self):
        ...

class ReefLocalTideTests(unittest.TestCase):

    def test_the_reef_uses_its_own_tide_for_its_zones(self):
        ...

class WetLineTests(unittest.TestCase):

    def rock(self, change, seed=0):
        ...

    def test_dark_wet_rock_below_a_line_is_found(self):
        ...

    def test_shade_and_plain_rock_are_not_a_wet_line(self):
        ...

class ZonationTests(unittest.TestCase):

    def test_bands_zones_and_the_wet_line_on_the_reef(self):
        ...

    def test_bands_tapped_out_of_order_are_named(self):
        ...
