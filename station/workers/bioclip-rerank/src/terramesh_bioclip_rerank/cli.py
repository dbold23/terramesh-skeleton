from __future__ import annotations
import math
import sys
import numpy as np
from . import NAME, VERSION, geocube
from .kit import EXIT_UNSUPPORTED, Job, WorkerError, main as kit_main
from .openset import BACKGROUNDS, family_hint, kingdom_verdict
from .survey import crop_boxes, observations_to_rank
NOT_RECORDED_NEARBY = 0.05

def make_encoder(job: Job):
    """Replaced in tests by an encoder that needs no weights."""
    ...

def run(job: Job) -> None:
    ...

def checked_params(given: dict) -> dict:
    ...

def load_cube(job: Job) -> geocube.OccurrenceCube:
    """The one `.tmgc` file in the gbif-cube input folder. Station hashes that folder into the job
    ID, so a rebuilt cube gives a new job rather than a stale cached layer."""
    ...

def record_models(job: Job, encoder, cube) -> None:
    ...

def load_crops(job: Job, photo, fractions):
    ...

def _apply_orientation(crop, image):
    ...

def geo_prior(cube: geocube.OccurrenceCube, observation, enabled: bool):
    ...

def vision_scores(bank: np.ndarray, query: np.ndarray, logit_scale: float) -> np.ndarray:
    """Temperature softmax over cosine similarity, as `SpeciesEmbeddingBank.softmaxScores`."""
    ...

def open_set_check(query: np.ndarray, bank: np.ndarray, backgrounds: np.ndarray, top: dict, scene_labels: list[str], params: dict) -> dict:
    """Whether to withhold the top name (see `openset`). The similarities are reported whatever the
    outcome, so the margin can be tuned on real walks. Uses the photographs alone: the location
    prior must never talk a patch of mulch into being a butterfly."""
    ...

def taxa_index(taxa: list[dict], candidate: dict) -> int:
    ...

def top_candidates(taxa, scores, parts, k: int) -> list[dict]:
    ...

def agreement_with(original: dict | None, top: dict) -> str:
    ...

def summarise_original(original: dict | None) -> dict | None:
    ...

def normalise(vector: np.ndarray) -> np.ndarray:
    ...

def json_line(value) -> str:
    ...

def main() -> None:
    ...
