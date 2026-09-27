"""Waterlines: a slough's own tide from its taps, hydroperiod, and habitat carried by hydroperiod."""
import unittest
import numpy as np
import slough
from intertidal import tide, waterline

class SiteTideTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ...

    def test_a_slough_shows_its_flood_its_ebb_and_its_floor(self):
        ...

    def test_a_minute_by_minute_watch_with_bad_readings(self):
        ...

    def test_open_rock_stays_a_plain_lag_and_ratio(self):
        ...

    def test_too_few_taps_say_so(self):
        ...

class HydroperiodTests(unittest.TestCase):

    def test_hydroperiod_falls_with_height_and_matches_hours_under(self):
        ...

    def test_a_floor_keeps_everything_below_it_under_water(self):
        ...

class HabitatTests(unittest.TestCase):

    def test_a_band_carries_to_another_site_by_hydroperiod_not_height(self):
        ...

    def test_waves_are_taken_off_and_put_back(self):
        ...

    def test_slough_habitats_now_and_with_the_sea_higher(self):
        ...

    def test_priors_are_hydroperiods_from_the_station(self):
        ...
