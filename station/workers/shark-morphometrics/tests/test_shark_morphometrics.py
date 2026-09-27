import csv
import json
import os
import re
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path
import numpy as np
import pytest
from PIL import Image, ImageOps
import synthetic
from terramesh_shark_morphometrics import NAME, VERSION
from terramesh_shark_morphometrics.cli import DEFAULTS
from terramesh_shark_morphometrics.landmarks import MEASUREMENTS
from terramesh_shark_morphometrics.pickpage import upright_map

def worker(*args, env=None, check=True):
    ...

def run_job(tmp_path, export_kwargs=None, picks=None, params=None, picks_file=None):
    ...

def measured(out):
    ...

def test_worker_toml_matches_code():
    ...

def test_describe():
    ...

def test_every_measurement_joins_known_landmarks():
    ...

@pytest.mark.parametrize('orientation', range(1, 9))
def test_upright_map_matches_exif_transpose(tmp_path, orientation):
    ...

def test_lengths_recovered_from_picks(tmp_path):
    ...

def test_scale_uncertainty_dominates_long_measurements(tmp_path):
    ...

def test_downscaled_stills_keep_their_geometry(tmp_path):
    ...

def test_leopard_shark_has_an_interdorsal_space(tmp_path):
    ...

def test_disagreeing_picks_are_flagged_and_widen_the_error(tmp_path):
    ...

def test_stills_too_close_together_are_not_used(tmp_path):
    ...

def test_phone_lidar_length_is_cross_checked(tmp_path):
    ...

def test_without_landmarks_the_layer_is_the_picking_page(tmp_path):
    ...

def page_config(out):
    ...

def test_picking_page_cameras_agree_with_the_stored_picks(tmp_path):
    ...

def test_other_missions_are_refused(tmp_path):
    ...

def test_landmarks_for_another_survey_are_refused(tmp_path):
    ...

def test_pick_command_reads_a_zip(tmp_path):
    ...

def test_cube_ids_follow_the_printed_cubes():
    ...

def test_vendored_cube_code_matches_the_intertidal_pipeline():
    """The copies stay what they were copied from, when that is in the same checkout."""
    ...

def test_deck_cubes_correct_a_wrong_arkit_scale(tmp_path):
    ...

def test_without_cubes_the_same_pass_keeps_arkits_error(tmp_path):
    ...

def test_a_cube_that_moved_during_the_pass_is_left_out(tmp_path):
    ...

def test_head_mid_body_and_tail_cubes_share_one_scale(tmp_path):
    ...

def test_a_misprinted_cube_among_three_is_left_out_of_the_scale(tmp_path):
    ...
BAR = (-0.05, -0.14, 0.26)

def test_the_scale_bar_sets_the_scale(tmp_path):
    ...

def test_the_scale_bar_overrules_a_misprinted_cube(tmp_path):
    ...
