from __future__ import annotations
import csv
import itertools
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
import numpy as np
from . import NAME, VERSION, audio, geo
from .backends import Backend, load as load_backend
from .kit import EXIT_TEMPORARY, EXIT_UNSUPPORTED, Job, WorkerError, main as kit_main, milliseconds_to_iso
BATCH = 16

def run(job: Job) -> None:
    ...

def _load(key: str, job: Job) -> Backend:
    ...

def window_record(backend: Backend, window: audio.Window, row: np.ndarray, top: int, allowed, analysed_at: int) -> dict:
    ...

def locator(stretches: list[audio.Stretch], part_of: dict[str, audio.Part]):
    """Maps a window to the file and offset where a person can listen to it."""
    ...

def _key(entry: dict) -> str:
    ...

def collect_suggestions(backends: list[Backend], results: dict[str, list[dict]], params: dict, locate) -> list[dict]:
    ...

def write_review(job: Job, backends: list[Backend], results: dict[str, list[dict]], suggestions: list[dict], params: dict, locate) -> int:
    """review.csv: windows worth a person's listen, loudest reason first. Near misses score between a
    model's review and suggestion cuts; single-model suggestions are labels only one model reached."""
    ...

def survey_place(job: Job) -> tuple[float, float, int] | None:
    """The median GPS fix of the walk and its week of the year (1-48, BirdNET's convention), used only to
    tell a model which species to expect. Never written into the layer."""
    ...

def main() -> None:
    ...
