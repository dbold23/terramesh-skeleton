"""Runs the worker end to end on a synthetic survey export, with the test-only tone model in place of
Perch and BirdNET. It checks the contract (layer.json last, artefacts hashed, progress as JSON lines),
the phone's journal rules (last line wins, cut-off parts skipped, hashes checked) and the windowing
the phone uses (windows on each run's clock, never across a gap)."""
from __future__ import annotations
import csv
import hashlib
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path
import numpy as np
import soundfile
RATE = 48000
START_MS = 1790000000000

def tone(frequency: float, seconds: float, level: float=0.3) -> np.ndarray:
    ...

def noise(seconds: float, level: float=0.02, seed: int=1) -> np.ndarray:
    ...

def sha256(path: Path) -> str:
    ...

def make_snapshot(root: Path, parts: list[dict], *, tamper: str | None=None, trimmed: tuple[int, ...]=()) -> Path:
    """Writes an unpacked export with snapshot.json the way Station builds one (station/WORKERS.md section 4)."""
    ...

def run_worker(tmp_path: Path, snapshot: Path, params: dict | None=None) -> tuple[subprocess.CompletedProcess, Path]:
    ...

def read_windows(out: Path) -> list[dict]:
    ...

def test_scores_windows_across_a_part_boundary_and_writes_a_valid_layer(tmp_path):
    ...

def test_never_scores_across_a_cut_off_part(tmp_path):
    ...

def test_a_file_that_no_longer_matches_its_hash_is_not_scored(tmp_path):
    ...

def test_near_misses_go_to_the_review_sheet(tmp_path):
    ...

def test_parts_the_phone_deleted_after_scoring_are_skipped_quietly(tmp_path):
    ...

def test_a_fully_trimmed_walk_finishes_with_nothing_to_score(tmp_path):
    ...

def test_a_survey_without_sound_is_bad_input(tmp_path):
    ...

def test_describe_matches_worker_toml():
    ...

def test_a_species_not_expected_at_the_place_is_scored_but_not_suggested(tmp_path):
    ...

def test_perch_windows_are_centred_and_scaled_like_hoplite():
    ...

def test_birdnet_labels_keep_output_order_and_names(tmp_path):
    ...

def test_every_real_model_is_declared_in_worker_toml():
    """Station's validator rejects a layer naming a model worker.toml does not declare."""
    ...

def test_every_model_names_a_revision():
    """worker.toml is part of Station's job ID, so a pinned revision makes a new model a new job."""
    ...

def test_birdnet_preview_is_non_commercial():
    """Its terms of use limit the V3.0 developer preview to research and evaluation."""
    ...

def test_perch_sound_event_classes_are_not_scientific_names():
    ...
