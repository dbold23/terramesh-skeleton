"""python3 -m unittest discover -s station/experience"""
from __future__ import annotations
import os
import sys
import tempfile
import unittest
import experience_readout as er

class ReadoutTests(unittest.TestCase):

    def setUp(self):
        ...

    def test_reads_lines_and_skips_a_cut_line(self):
        ...

    def test_flags_a_cube_seen_but_never_recorded(self):
        ...

    def test_slow_still_saves_are_timed_and_flagged(self):
        ...

    def test_summary_has_rates_and_battery(self):
        ...

    def test_html_is_self_contained(self):
        ...

    def test_taps_are_counted_and_misses_flagged(self):
        ...

    def test_boxes_never_tapped_is_flagged(self):
        ...

    def test_missing_end_line_is_flagged(self):
        ...

    def test_a_live_cube_miss_is_not_hidden_by_a_sweep_save(self):
        ...

    def test_five_to_name_answers_are_split_by_organism_and_leave_the_duration_alone(self):
        ...

    def test_main_writes_html_only_when_asked(self):
        ...
