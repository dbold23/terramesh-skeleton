"""Reading the phone's sound journal (`audio.jsonl`, `audio/`) back into contiguous stretches.

The phone writes one journal line when a part opens and one when it closes; the last line for an id
wins. Parts of one run share a sample clock; runs do not (see AudioPartRecord in TerraMeshCore). A
stretch here is a maximal run of complete parts with no gap between them, so no window is ever
scored across missing sound.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from math import gcd
from pathlib import Path
import numpy as np
import soundfile
from scipy.signal import resample_poly
from .kit import Job, WorkerError

@dataclass(frozen=True)
class Part:
    id: str
    run_id: str
    index: int
    start_sample: int
    frame_count: int
    sample_rate: float
    relative_path: str
    started_at_ms: float | None
    status: str
    sha256: str | None
    clipped_samples: int
    session_mode: str

    @property
    def end_sample(self) -> int:
        ...

@dataclass
class Stretch:
    """Contiguous complete parts of one run, read as one signal."""
    run_id: str
    start_sample: int
    sample_rate: float

    @property
    def frame_count(self) -> int:
        ...

    @property
    def seconds(self) -> float:
        ...

    def started_at_ms(self) -> float | None:
        ...

def read_parts(job: Job) -> list[Part]:
    """The last journal line for each part, in the order parts were first journalled."""
    ...

def removed_parts(job: Job) -> set[str]:
    """Parts the phone deleted after scoring (`sound-trim.json` removedParts). Only short clips around
    detections are kept (Dan, 2026-09-26), so these files are gone on purpose, not missing."""
    ...

def stretches(job: Job, parts: list[Part], removed: set[str]=frozenset()) -> tuple[list[Stretch], list[str]]:
    """Groups complete, present, unaltered parts into gap-free stretches. Returns the stretches and a
    warning sentence for each part left out. Parts in `removed` are left out without a warning."""
    ...

def resample(signal: np.ndarray, source_rate: int, target_rate: int) -> np.ndarray:
    """Polyphase resampling (scipy.signal.resample_poly) of one window."""
    ...

@dataclass(frozen=True)
class Window:
    run_id: str
    index: int
    start_seconds: float
    duration_seconds: float
    started_at_ms: float | None
    samples: np.ndarray

def iter_windows(job: Job, stretch: Stretch, *, model_rate: int, window_seconds: float, hop_seconds: float, minimum_final_seconds: float):
    """Yields fixed windows over one stretch, reading one part at a time so memory stays bounded by a
    part (five minutes) however long the walk was. Windows are cut on the recording's own sample
    clock and aligned to the run (window k starts at k x hop), exactly as the phone cuts them, then each
    window is resampled on its own. The last window is padded with silence when at least
    `minimum_final_seconds` of sound remain, and dropped otherwise."""
    ...

def count_windows(stretch: Stretch, *, window_seconds: float, hop_seconds: float, minimum_final_seconds: float) -> int:
    """How many windows `iter_windows` will yield, without reading any sound."""
    ...

def _sha256(path: Path) -> str:
    ...
