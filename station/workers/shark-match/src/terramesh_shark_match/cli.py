"""`terramesh-worker`: the Station entry point plus the catalogue commands a person runs.

Station runs `describe` and `run` (station/WORKERS.md). The other commands change the catalogue
or turn a review into a Wildbook sheet, so they are run by hand and never by a Station job:

    terramesh-worker catalog init   --catalog DIR --mission oseaShark
    terramesh-worker catalog import --catalog DIR --csv photos.csv --reviewer NAME --source TEXT
    terramesh-worker catalog add    --catalog DIR --snapshot SURVEY --individual ID --reviewer NAME
    terramesh-worker calibrate      --catalog DIR
    terramesh-worker wildbook       --snapshot SURVEY --review review.csv --out DIR
"""
from __future__ import annotations
import argparse
import csv
import json
import os
import random
import sys
import tempfile
import zipfile
from pathlib import Path
import numpy as np
from . import NAME, VERSION
from .catalog import Catalog, CatalogError, add_encounter, import_table, init_catalog, load_catalog
from .kit import EXIT_BAD_INPUT, EXIT_OK, Job, WorkerError, main as kit_main, sha256_file
from .matching import score_view
from .models import global_embedder, load_rgb, local_matchers, test_backend
from .scoring import CALIBRATION_FILE, DECISIONS, Calibration, decide, fit_calibration, rank_individuals, save_calibration
from .snapshot import VIEWS, Encounter, SnapshotError, crop_box, load_encounter, mask_people
from . import wildbook
from .walkround import add_walk_round

def resolve_params(given: dict) -> dict:
    ...

def stack_for(params: dict, embedder) -> list[str]:
    ...

def prepare_queries(encounter: Encounter, folder: Path) -> dict[str, list[tuple[Path, object]]]:
    """Crops each confirmed still to its body box. Returns view -> [(crop path, still)]."""
    ...

def usable_calibration(catalog: Catalog, stack: list[str], warn) -> Calibration | None:
    ...

def run(job: Job) -> None:
    ...

def candidate_record(entry: dict, catalog: Catalog, queries: dict) -> dict:
    ...

def write_outputs(job, params, encounter, catalog, calibration, ranked, queries, decision, reasons, accept, new, stack) -> None:
    ...

class LocalContext:
    """The parts of a Job the scorers use, for commands run outside Station."""

    def __init__(self, model_cache: Path | None=None):
        ...

    def record_model(self, *, name, version, weights, licence, commercial_use, source):
        ...

    def warn(self, message):
        ...

    def log(self, message):
        ...

def open_snapshot(path: Path, stack) -> Path:
    """A survey folder as is, or an export ZIP unpacked into a temporary folder."""
    ...

def calibrate(catalog: Catalog, params: dict, model_cache: Path | None=None) -> dict:
    ...

def review_to_wildbook(snapshot: Path, review: Path, out: Path, params: dict, landmarks: Path | None=None) -> Path:
    ...

def human_main(argv: list[str]) -> int:
    ...

def main() -> None:
    ...
