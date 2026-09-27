"""Runs the worker in-process on a synthetic survey, with a stand-in encoder so no weights are
needed. The stand-in makes the photographs look equally like two sea stars, so only the location
prior can separate them: that is the behaviour under test."""
import hashlib
import json
import math
import os
import sys
from pathlib import Path
import numpy as np
import pytest
from PIL import Image
from terramesh_bioclip_rerank import cli, geocube, kit
from terramesh_bioclip_rerank.openset import BACKGROUNDS, family_hint, kingdom_agreement, kingdom_verdict
MONTEREY = (36.6, -121.9)
MARCH_2026 = 1772668800000

class FakeEncoder:
    logit_scale = 50.0

    def __init__(self, weights: Path):
        ...

    def encode_texts(self, texts):
        ...

    def encode_images(self, images):
        ...

def write_snapshot(root: Path, *, placed=True, hard_cases=False) -> Path:
    ...

def write_cube(cache: Path) -> Path:
    ...

def run_worker(tmp_path, monkeypatch, params=None, cube=True, **snapshot_options):
    ...

def test_location_prior_decides_between_look_alikes(tmp_path, monkeypatch, capsys):
    ...

def test_crop_follows_the_tapped_point(tmp_path, monkeypatch):
    ...

def test_without_location_ranks_on_photographs_alone(tmp_path, monkeypatch):
    ...

def test_snapshot_is_never_written(tmp_path, monkeypatch):
    ...

def test_missing_cube_is_bad_input(tmp_path, monkeypatch, capsys):
    ...

def test_layer_passes_station_validation(tmp_path, monkeypatch):
    ...

def test_scene_context_and_man_made_crops_are_not_identified(tmp_path, monkeypatch, capsys):
    ...

def test_subject_gate_matches_the_phone():
    ...

def test_no_name_for_mulch_or_for_a_kingdom_the_phone_did_not_see(tmp_path, monkeypatch, capsys):
    ...

def test_kingdom_check_matches_the_phone():
    ...
