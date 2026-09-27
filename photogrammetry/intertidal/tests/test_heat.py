"""Heat on the shore: a hot midday low tide flags the high bands, a cool day or a high tide does not."""
import argparse
import csv
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
import slough
from intertidal import heat, waterline
from intertidal.__main__ import cmd_heat

def week():
    """Hourly weather for a week from the start of the station's record: sunny days, one of them hot."""
    ...

class HeatTests(unittest.TestCase):

    def setUp(self):
        ...

    def midday_low_day(self):
        """The local day in the week whose daylight low tide is lowest, and the other days."""
        ...

    def test_a_hot_midday_low_tide_is_flagged_for_the_band_it_leaves_out(self):
        ...

    def test_waves_keep_a_band_wet(self):
        ...

    def test_the_command_reads_a_reef_and_a_forecast(self):
        ...
