import csv
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path
import numpy as np
import pytest
import synthetic
from terramesh_shark_match import NAME, VERSION
from terramesh_shark_match.cli import DEFAULTS
from terramesh_shark_match.scoring import Calibration, Pair, decide, fit_calibration, rank_individuals, shortlist
from terramesh_shark_match.snapshot import SnapshotError, load_encounter

def worker(*args, env=None, check=True):
    ...

def test_worker_toml_matches_code():
    ...

def test_pinned_weights_match_worker_toml():
    ...

def test_describe():
    ...

def test_reads_confirmed_views_and_crops_from_journal(tmp_path):
    ...

def test_without_journal_matches_whole_frame_and_says_so(tmp_path):
    ...

def test_rejects_other_missions(tmp_path):
    ...

def test_shortlist_respects_exclusions():
    ...

def calibration(accept=0.8, new=0.3):
    ...

def ranked(*scores):
    ...

def test_open_set_decisions():
    ...

def test_calibration_thresholds_sit_above_impostors():
    ...

def test_calibration_refuses_a_thin_catalogue():
    ...

@pytest.fixture(scope='module')
def catalog(tmp_path_factory):
    ...

def run_job(tmp_path, catalog, individual, seed, **params):
    ...

def test_resighting_is_proposed_not_assigned(tmp_path, catalog):
    ...

def test_new_animal_is_not_proposed_as_a_resighting(tmp_path, catalog):
    ...

def test_missing_catalogue_input_fails_cleanly(tmp_path, catalog):
    ...

def test_threshold_cannot_be_lowered(tmp_path, catalog):
    ...

def test_review_fills_the_wildbook_individual(tmp_path, catalog):
    ...

def test_catalog_add_needs_a_reviewer_and_rejects_duplicates(tmp_path, catalog):
    ...

def test_operator_details_reach_the_wildbook_row(tmp_path):
    ...

def handler_mask(export: Path, frame_id: str, box: tuple[float, float, float, float], size=(400, 300)) -> Path:
    """A person mask as the phone would write it: white where a handler is, smaller than the still."""
    ...

def test_handlers_are_greyed_out_before_matching(tmp_path):
    ...

def test_an_unreadable_mask_changes_nothing(tmp_path):
    ...

def test_a_view_confirmed_under_hands_is_noted(tmp_path):
    ...
import importlib.util

def walk_export(folder: Path, individual: str, seed: int, place: int, landmarks: Path | None=None):
    ...

@pytest.fixture(scope='module')
def twin_catalog(tmp_path_factory):
    """A catalogue built only from walk rounds: each shark walked three times, filed from its body maps."""
    ...

def run_walk_job(tmp_path, catalog, snapshot, landmarks=None):
    ...

def test_catalogue_is_filed_from_body_maps_with_a_known_side(twin_catalog):
    ...

def test_a_walk_round_finds_the_shark_it_walked_round(tmp_path, twin_catalog):
    ...

def test_without_landmarks_both_flanks_are_tried_and_nothing_is_filed(tmp_path, twin_catalog):
    ...
