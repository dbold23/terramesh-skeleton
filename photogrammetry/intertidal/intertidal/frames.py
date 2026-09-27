"""Pick reconstruction frames out of a capture video.

A handheld video at a crevice mouth is mostly redundant and partly blurred:
the phone is moving, the light is low, and the torch or the sun glints off
wet rock. We keep the sharpest frame in each short window, drop windows whose
best frame is still too soft or too clipped, and record why, so a failed
reconstruction can be traced back to the capture rather than guessed at.
"""
from __future__ import annotations
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
import cv2
import numpy as np

@dataclass
class FrameScore:
    index: int
    time_s: float
    sharpness: float
    clipped: float
    dark: float

def read_pixels(path: Path) -> np.ndarray | None:
    """A frame's pixels as the sensor stored them. The app's stills keep the sensor's landscape
    pixels and carry an EXIF orientation so photo viewers show them upright; OpenCV would apply
    that turn, but COLMAP and ARKit's intrinsics describe the unturned pixels, so every read of
    a reconstruction frame ignores it."""
    ...

def score(image: np.ndarray) -> tuple[float, float, float]:
    ...

def select(video: Path, out_dir: Path, per_second: float=3.0, min_sharpness: float=60.0, max_clipped: float=0.08, max_frames: int=400, prefix: str='frame') -> list[FrameScore]:
    """Write the chosen frames as JPEGs and a `<prefix>s.json` describing every window.

    `prefix` keeps frames from several clips apart in one directory."""
    ...
STILL_SHARPNESS_FLOOR = 15.0
STILL_CLIPPED_CEILING = 0.2

def still_thresholds(scores: list[tuple[float, float]], min_sharpness: float=60.0, max_clipped: float=0.08) -> tuple[float, float]:
    """Sharpness and glare limits for one survey's stills, from their own spread: half the
    median sharpness (never above `min_sharpness`, never below the floor) and one and a half
    times the median clipped share (never below `max_clipped`, never above the ceiling). A
    textured rock survey keeps the fixed limits; a smooth or bright scene relaxes them."""
    ...

def select_stills(images: list[Path], out_dir: Path, min_sharpness: float=60.0, max_clipped: float=0.08, prefix: str='still', adaptive: bool=True) -> list[FrameScore]:
    """The same blur and glare checks for stills the app already saved. Kept stills are
    copied unchanged as `<prefix>_<n>.jpg`, n being the still's position in `images`. With
    `adaptive`, the limits follow the survey's own stills (`still_thresholds`)."""
    ...
