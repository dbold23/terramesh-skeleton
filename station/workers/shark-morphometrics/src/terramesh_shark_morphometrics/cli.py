"""`terramesh-worker`: the Station entry point, plus `pick` for use without Station.

Station runs `describe` and `run` (station/WORKERS.md). A run always writes `pick.html`, the page
for placing landmarks on the encounter's stills. When the shark-landmarks input holds picks for
this survey, the run also measures from them:

    terramesh-worker pick --snapshot SURVEY(.zip) --out DIR [--landmarks FILE] [--picker NAME]
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import sys
import tempfile
import zipfile
from pathlib import Path
import numpy as np
from . import NAME, VERSION, bodymap, pickpage
from .cameras import SnapshotError, Still, load_stills
from .cubescale import Scale, cube_scale
from .kit import EXIT_BAD_INPUT, EXIT_OK, Job, WorkerError, main as kit_main
from .landmarks import BY_ID, SPECIES, landmarks_for, measurements_for
from .triangulate import Fit, TriangulationError, distance, triangulate
DISAGREEMENT = 4.0

def resolve_params(given: dict) -> dict:
    ...

def survey_of(snapshot: Path) -> dict:
    ...

def find_landmarks(folder: Path | None, survey_id: str) -> Path | None:
    ...

def read_picks(path: Path | None, survey_id: str, mission: str, stills: dict[str, Still], warn) -> tuple[list[dict], str]:
    """The picks in a landmarks file, checked against this survey. Returns (picks, picker)."""
    ...

def fit_landmarks(picks: list[dict], stills: dict[str, Still], mission: str, params: dict, warn) -> tuple[dict[str, Fit], dict[str, dict]]:
    ...

def phone_lengths(snapshot: Path) -> dict[str, dict]:
    """The app's own LiDAR lengths, latest successful attempt of each kind."""
    ...

def measure(fits: dict[str, Fit], status: dict[str, dict], mission: str, scale: Scale) -> tuple[list[dict], list[dict]]:
    ...

def phone_check(rows: list[dict], phone: dict[str, dict], warn) -> list[dict]:
    ...

def scale_json(scale: Scale, fits: dict[str, Fit]) -> dict:
    """The scale block, with each cube placed against the nearest landmark so a reader can see
    which cube lay by the head and which by the tail."""
    ...

def write_csv(path: Path, rows: list[dict]) -> None:
    ...

def run(job: Job) -> None:
    ...

def pick_command(args) -> int:
    ...

def main(argv: list[str] | None=None) -> None:
    ...
