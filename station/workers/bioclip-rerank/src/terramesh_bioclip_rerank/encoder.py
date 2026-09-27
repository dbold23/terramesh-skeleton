"""BioCLIP through open_clip: image and text embeddings, and the cached text bank for a vocabulary.

torch and open_clip are imported only here and only when a real model is loaded, so the rest of
the worker (and its tests) runs without them.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import numpy as np
from .kit import EXIT_TEMPORARY, EXIT_UNSUPPORTED, Job, WorkerError, sha256_file
PROMPT_VERSION = 1

def taxonomic_name(taxon: dict) -> str:
    """BioCLIP's taxonomic string: kingdom to family, then the binomial."""
    ...

def prompts(taxon: dict) -> list[str]:
    """The text ensemble for one species. The taxonomic form is what BioCLIP was trained on; the
    plain binomial and common name help where the higher ranks are missing or disagree."""
    ...

class BioCLIPEncoder:
    """Loads one pinned Hugging Face revision of an open_clip model into the model cache and runs
    it from there, so every job with the same worker.toml uses exactly the same weights."""

    def __init__(self, job: Job, repo: str, revision: str) -> None:
        ...

    def encode_images(self, images) -> np.ndarray:
        ...

    def encode_texts(self, texts: list[str]) -> np.ndarray:
        ...

def text_bank(job: Job, encoder, taxa: list[dict], *, batch_size: int=64, progress_span=(0.05, 0.35)) -> np.ndarray:
    """One L2-normalised text embedding per taxon (the mean of its prompt ensemble), cached in the
    model cache by weights, vocabulary and prompt version."""
    ...

def background_bank(job: Job, encoder) -> np.ndarray:
    """One embedding per `openset.BACKGROUNDS` entry, for the check that withholds a name when the
    photograph looks more like mulch or a pot than like any species."""
    ...

def prompt_bank(job: Job, encoder, groups: list[list[str]], *, tag: str, what: str, batch_size: int=64, progress_span=(0.05, 0.35)) -> np.ndarray:
    """One L2-normalised embedding per prompt group (the mean of the group), cached in the model
    cache by weights and the exact prompts."""
    ...

def _normalise(matrix: np.ndarray) -> np.ndarray:
    ...
