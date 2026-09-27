"""Sound models behind one small interface, so the worker's windowing, bookkeeping and reporting
never depend on which framework a model needs."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
import numpy as np

@dataclass(frozen=True)
class Label:
    index: int
    label: str
    scientific_name: str | None
    common_name: str | None

class Backend(Protocol):
    key: str
    name: str
    version: str
    licence: str
    commercial_use: bool
    source: str
    sample_rate: int
    window_seconds: float
    score_kind: str
    labels: list[Label]
    weights: Path

    def score(self, batch: np.ndarray) -> np.ndarray:
        """`batch` is (windows, samples) float32 at `sample_rate`. Returns (windows, labels) raw scores."""
        ...

def load(key: str, *, cache: Path, device: str) -> Backend:
    ...

def onnx_session(path: Path, device: str):
    """An ONNX Runtime session. Core ML is tried first on a Mac unless the job asked for the CPU;
    ONNX Runtime falls back to the CPU for any operator Core ML cannot run."""
    ...

def output_width(session, index: int) -> int | None:
    ...
