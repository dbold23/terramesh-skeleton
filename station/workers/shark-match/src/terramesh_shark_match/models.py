"""The two kinds of scorer WildFusion combines.

- A global embedder ranks every catalogue image of a view by cosine similarity. It is cheap, so
  it builds the shortlist. MiewID-msv3 is the real one.
- Local matchers compare only the shortlisted pairs: ALIKED or DISK keypoints, matched by
  LightGlue, counted above a match-confidence threshold. They look at the spot pattern itself.

Weights are downloaded on first use (`network = "models"` in worker.toml) through HF_HOME and
TORCH_HOME, which Station sets inside its model cache, and every loaded file is hashed into
layer.json.

`TERRAMESH_SHARK_MATCH_TEST_BACKEND=1` swaps both for tiny deterministic stand-ins (a grey
thumbnail embedding and ORB keypoints) so the pipeline can be tested without downloads;
`=global` swaps only MiewID, for machines that can reach GitHub but not Hugging Face. A layer
made that way says so in its models and warnings, and is useless for identification.
"""
from __future__ import annotations
import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps
from .kit import EXIT_TEMPORARY, EXIT_UNSUPPORTED, WorkerError, sha256_file

def test_backend() -> str:
    """"" normally; "1" for both stand-ins; "global" for the stand-in embedder only."""
    ...

def load_rgb(path: Path) -> Image.Image:
    ...

def normalise(vectors: np.ndarray) -> np.ndarray:
    ...

def torch_device(requested: str) -> str:
    ...

class MiewID:

    def __init__(self, job, repo: str, revision: str):
        ...

    def embed(self, paths: list[Path]) -> np.ndarray:
        ...

class LightGlueCounts:
    """Counts LightGlue matches above `threshold` between shortlisted pairs (wildlife-tools)."""

    def __init__(self, job, features: str, max_keypoints: int, image_size: int, threshold: float=0.5):
        ...

    def slim(self, features):
        """Keeps keypoints and descriptors only. The extractor also returns dense maps sized like
        each image, which cannot be batched when crops differ in shape and are not used."""
        ...

    def counts(self, queries: list[Path], catalog: list[Path], pairs: list[tuple[int, int]]) -> np.ndarray:
        ...

class ThumbnailEmbedder:
    """Test stand-in: a 24 x 12 grey thumbnail, mean-centred. Not an identifier."""

    def __init__(self, job):
        ...

    def embed(self, paths: list[Path]) -> np.ndarray:
        ...

class OrbCounts:
    """Test stand-in: ORB keypoints with a ratio test and a RANSAC homography, inliers counted."""

    def __init__(self, job, name: str):
        ...

    def counts(self, queries: list[Path], catalog: list[Path], pairs: list[tuple[int, int]]) -> np.ndarray:
        ...

def global_embedder(job, params):
    ...

def local_matchers(job, params):
    ...
