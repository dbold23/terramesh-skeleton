"""Read a TerraMesh survey export (the ZIP from "Export survey", or its unpacked folder).

The intertidal mission records its sweep through the app's timed clip recorder. Each clip
is a line in `clips.jsonl` with `purpose == "intertidalSweep"` and a movie at
`clips/<id>.mov`, written in the camera's native landscape orientation, so the ARKit
intrinsics in the record apply to the movie's pixels unchanged.

Newer builds also write `clips/<id>.poses.jsonl`: one line per frame in the movie, in
order, with ARKit's camera-to-world transform (metres) and intrinsics for that frame.
Frame n of the movie is line n, because the recorder only writes a pose for a frame it
actually encoded. On LiDAR phones they also write `clips/<id>.depth`, ARKit's scene depth for
every few frames (see lidar.py for its layout).

Builds with the torch button say whether the phone's torch lit each clip (`torch`: on, off or
mixed) and each still (`torch`: true or false). A light that moves with the camera changes the
shading and the glare on wet rock from frame to frame; see the README.

A survey whose sweep was never started still has the mission's stills: `frames.jsonl`,
one line per ARKit frame, some with an `images/<id>.jpg` in the same landscape pixels as
its intrinsics. `survey_stills` reads those so the survey can be reconstructed anyway.
"""
from __future__ import annotations
import json
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

@dataclass
class FramePose:
    frame: int
    time_s: float
    world_from_camera: np.ndarray
    intrinsics: tuple[float, float, float, float] | None
    tracking: str

    @property
    def centre(self) -> np.ndarray:
        ...

    @property
    def forward(self) -> np.ndarray:
        ...

def _intrinsics(k) -> tuple[float, float, float, float] | None:
    ...

def read_poses(path: Path) -> list[FramePose]:
    ...

@dataclass
class SweepClip:
    id: str
    movie: Path | None
    duration_s: float
    width: int
    height: int
    intrinsics: tuple[float, float, float, float] | None
    poses: list[FramePose] | None = None
    survey_id: str | None = None
    started_at_ms: float | None = None
    depth_track: Path | None = None
    crevice_guide: dict | None = None
    torch: str | None = None

    def pose_for(self, frame: int) -> FramePose | None:
        ...

def unpack(export: Path, into: Path) -> Path:
    """Return a folder holding the export, extracting a ZIP safely if needed."""
    ...

def has_sweep_clip(folder: Path) -> bool:
    ...

@dataclass
class Still:
    image: Path
    pose: FramePose

def crevice_id(folder: Path) -> str | None:
    """The crevice the observer chose or named on the phone, if it is one the library accepts."""
    ...

def survey_stills(folder: Path) -> tuple[SweepClip, list[Still]]:
    """The survey's saved stills with their ARKit poses, and a SweepClip describing them
    (no movie) so the rest of from-export can treat them like a sweep."""
    ...

def _torch_use(lit: set) -> str | None:
    """"on", "off" or "mixed" from whether the torch was lit on each still; None when unrecorded."""
    ...

def sweep_clips(folder: Path, clip_id: str | None=None) -> list[SweepClip]:
    ...

def _crevice_guide(value) -> dict | None:
    """The phone's guide summary, when it is well formed: a lock-on point in ARKit metres."""
    ...

def visit(folder: Path, clip: SweepClip, margin_s: float=120.0) -> dict:
    """When and where a sweep was filmed: the clip's start time and the survey's GPS fixes
    from around it (the median of the ones within `margin_s`, with the best accuracy among them)."""
    ...

def mesh_tile(manifest: dict, coarse: bool) -> dict | None:
    """The survey's tile on the worldwide grid (an H3 cell id), at the level it may be shown.

    The phone files each survey under a tile (`meshTile`: street, neighbourhood and region cells,
    and the level it publishes at). Only the published cell is kept, and a crevice survey is never
    kept finer than a neighbourhood (about 5 km²), matching the kilometre rounding of its GPS."""
    ...
