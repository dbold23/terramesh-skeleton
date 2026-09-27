import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path
import pytest
from PIL import Image
import fixtures
from terramesh_individual_match import NAME, VERSION
from terramesh_individual_match.catalog import CatalogError, add_sighting, init_catalog, load_catalog
from terramesh_individual_match.cli import DEFAULTS, Folder
from terramesh_individual_match.decision import combine, tag_evidence, weigh_mirrored
from terramesh_individual_match.groups import GROUPS
from terramesh_individual_match.sightings import SightingPhoto, crop, read_sightings
from terramesh_individual_match.tags import compare, normalise

def worker(*args, env=None, check=True):
    ...

def test_worker_toml_matches_code():
    ...

def test_models_are_shark_match_s():
    """The scorers are shark-match's, so the declared weights must be too."""
    ...

def test_groups_match_the_phone():
    ...

def test_tag_numbers_compare_exactly_or_as_near_misses():
    ...

def test_tag_evidence_and_decisions():
    ...

def test_a_flipped_comparison_never_decides_alone():
    ...

def test_reads_marked_records_and_skips_the_rest(tmp_path):
    ...

def test_crops_turn_landscape_sensor_frames_upright(tmp_path):
    ...

@pytest.fixture(scope='module')
def catalogue(tmp_path_factory):
    ...

def run_job(tmp_path, catalogue, records, seed, **params):
    ...

def test_a_beach_walk_with_three_kinds_of_individual(tmp_path, catalogue):
    ...

def test_a_left_side_finds_a_turtle_known_only_from_its_right(tmp_path, catalogue):
    ...

def test_no_position_leaves_the_worker(tmp_path, catalogue):
    """An individual's sightings are a map to find it: nothing written may place the survey."""
    ...

def test_turtle_with_a_known_flipper_tag(tmp_path, catalogue):
    ...

def test_missing_catalogue_input_fails_cleanly(tmp_path):
    ...

def test_threshold_cannot_be_lowered(tmp_path, catalogue):
    ...

def test_catalog_add_copies_photos_and_the_tag(tmp_path):
    ...
