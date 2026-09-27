"""`terramesh-worker`: the Station entry point plus the catalogue commands a person runs.

Station runs `describe` and `run` (station/WORKERS.md). The other commands change a catalogue, so
they are run by hand after a person has reviewed, and never by a Station job:

    terramesh-worker catalog init   --catalog DIR --group seaTurtle
    terramesh-worker catalog import --catalog DIR --csv register.csv --reviewer NAME --source TEXT
    terramesh-worker catalog add    --catalog DIR --snapshot SURVEY --observation ID --individual ID --reviewer NAME
    terramesh-worker calibrate      --catalog DIR --model-cache DIR

Matching is shark-match's, imported rather than copied: the MiewID shortlist, ALIKED and DISK with
LightGlue on the shortlist, per-scorer logistic calibration and the same open-set thresholds.
"""
from __future__ import annotations
import argparse
import csv
import json
import random
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from terramesh_shark_match.cli import LocalContext, open_snapshot
from terramesh_shark_match.matching import score_view
from terramesh_shark_match.models import global_embedder, local_matchers, test_backend
from terramesh_shark_match.scoring import CALIBRATION_FILE, Calibration, decide, fit_calibration, rank_individuals, save_calibration
from . import NAME, VERSION
from .catalog import Catalog, CatalogError, add_sighting, import_table, init_catalog, load_catalog
from .decision import DECISIONS, combine, tag_evidence, weigh_mirrored
from .groups import GROUPS, MIRRORED, VIEW_TITLES
from .kit import EXIT_BAD_INPUT, EXIT_OK, Job, WorkerError, main as kit_main
from .sightings import Sighting, crop, read_sightings

def resolve_params(given: dict) -> dict:
    ...

def stack_for(params: dict, embedder) -> list[str]:
    ...

def usable_calibration(catalog: Catalog, stack: list[str], warn) -> Calibration | None:
    ...

class Scorers:
    """Loads MiewID and the local matchers once, and only if something needs comparing."""

    def __init__(self, job, params):
        ...

    def get(self):
        ...

def thresholds(calibration: Calibration | None, params: dict) -> tuple[float | None, float | None]:
    ...

def match_sighting(job: Job, sighting: Sighting, catalog: Catalog | None, scorers: Scorers, params: dict, calibrations: dict) -> dict:
    ...

def tag_match(individual: str, tag: dict | None) -> str | None:
    ...

def candidate_record(entry: dict, catalog: Catalog, crops: dict, targets: dict, tag: dict | None) -> dict:
    ...

def run(job: Job) -> None:
    ...

def write_outputs(job: Job, manifest: dict, results: list[dict], catalogs: dict, skipped: int) -> None:
    ...

class Folder:
    """The parts of a Job that read_sightings uses, over an unpacked export."""

    def __init__(self, root: Path):
        ...

    def has(self, relative: str) -> bool:
        ...

    def path(self, relative: str) -> Path:
        ...

    def jsonl(self, relative: str):
        ...

def calibrate(catalog: Catalog, params: dict, model_cache: Path | None=None) -> dict:
    """shark-match's calibration over this group's compared views: every same-individual pair from
    different records, plus the shortlist's different-individual pairs."""
    ...

def human_main(argv: list[str]) -> int:
    ...

def main() -> None:
    ...
