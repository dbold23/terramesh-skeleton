"""Contract checks for the intertidal-recon worker.

The full reconstruction takes minutes; it runs only with INTERTIDAL_E2E=<survey.zip>, for example
one made by photogrammetry/intertidal/tests/make_export.py.
"""
import hashlib
import json
import os
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path
import pytest

def snapshot(folder: Path, files: dict[str, bytes]) -> Path:
    """A snapshot as station/WORKERS.md section 4 defines it."""
    ...

def worker(*args: str, env: dict | None=None) -> subprocess.CompletedProcess:
    ...

def defaults() -> dict:
    ...

def test_describe_matches_worker_toml():
    ...

def test_survey_without_a_sweep_or_stills_is_bad_input(tmp_path):
    ...

def test_missing_cube_spec_is_bad_input(tmp_path):
    ...

def test_unsafe_crevice_id_is_bad_input(tmp_path):
    ...

def test_malformed_seed_is_bad_input(tmp_path):
    ...

def test_unknown_feature_type_is_bad_input(tmp_path):
    ...

@pytest.mark.skipif(not os.environ.get('INTERTIDAL_E2E'), reason='set INTERTIDAL_E2E to a survey ZIP')
def test_end_to_end(tmp_path):
    ...
