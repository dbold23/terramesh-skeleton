"""Shortlist, fusion, calibration and the open-set decision.

This follows WildFusion (Cermak et al. 2024, the method in wildlife-tools): a cheap global
similarity picks the `shortlist` most similar catalogue images for each query image, the local
matchers score only those pairs, and each scorer's raw output is mapped through its own
calibration before the mean is taken. Calibration is fitted on the catalogue's own labelled pairs
(`terramesh-worker calibrate`) and is logistic here, so it is stored as two numbers per scorer.

A calibrated score estimates, from this catalogue's past pairs, how often a pair scoring this
high showed the same individual. It is not a probability that this shark is that shark, and a
thin catalogue makes it a poor estimate. Nothing here names an individual: the decision is a
proposal a person reviews.
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

def sigmoid(value):
    ...

def transform(name: str, raw):
    """Global similarity is used as is; match counts are compressed, as they grow without bound."""
    ...

@dataclass
class Calibration:
    pipelines: dict[str, dict]
    accept: float
    new: float
    catalog_digest: str
    stack: list[str]

    def predict(self, name: str, raw) -> np.ndarray:
        ...

    def fuse(self, scores: dict[str, float]) -> float:
        ...

    @classmethod
    def load(cls, path: Path) -> 'Calibration | None':
        ...

def shortlist(similarity: np.ndarray, size: int, exclude: np.ndarray | None=None) -> list[tuple[int, int]]:
    """Top-`size` catalogue columns per query row. `exclude` masks pairs that must not be scored."""
    ...

@dataclass
class Pair:
    view: str
    query: int
    catalog: int
    scores: dict[str, float]
    fused: float | None

    def raw_key(self) -> tuple:
        """Uncalibrated ordering: total local matches, then global similarity."""
        ...

    def key(self) -> tuple:
        ...

def rank_individuals(pairs: list[Pair], individual_of) -> list[dict]:
    """Best pair per individual per view, individuals ordered by their best pair overall."""
    ...

def decide(ranked: list[dict], calibration: Calibration | None, accept: float, new: float) -> tuple[str, list[str]]:
    ...

def fit_calibration(rows: list[dict], stack: list[str], catalog_digest: str, *, min_positive: int=10, min_negative: int=30, seed: int=0) -> Calibration:
    """Fits one logistic map per scorer on labelled catalogue pairs and sets the open-set thresholds
    from out-of-fold fused scores, so a pair never sets the threshold it is judged by.

    accept: just above every different-individual pair seen (at least 0.5). If a different-individual
            pair scored above 0.99, accept is set to 1.0 and nothing can pass until that is resolved.
    new:    the lower of the 5th percentile of same-individual pairs (so about 1 in 20 true resightings
            like the catalogue's fall below it) and just above the 99th percentile of
            different-individual pairs (so "likely new" means "scored like a different animal").
            Between new and accept is "needs review".
    """
    ...

def save_calibration(calibration: Calibration, path: Path, models: list[dict]) -> dict:
    ...

def finite(value) -> float | None:
    ...
