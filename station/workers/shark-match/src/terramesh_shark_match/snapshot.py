"""Reads one guided shark encounter out of a Station snapshot.

The snapshot is the phone's export ZIP unpacked read-only (station/WORKERS.md, section 4). The
evidence a matcher can use is the operator-confirmed view stills: `frames.jsonl` lines whose
`captureReason` is `confirmedView:<view>`, each with its JPEG under `images/`. The encounter
journal `shark-encounter/frames.jsonl` holds the same confirmed frame with the body box the
phone's segmentation model drew on it, so a still is cropped to that box when the two can be
paired by view and camera pose.

Handlers hold the animal down during a workup, so their hands, arms and gloves are often inside
that box. When the export carries a person mask for a still (`shark-encounter/masks/<frame
id>.png`, white where a person is, in the upright still's frame at any resolution), the matcher
greys those pixels out, so a glove or a wetsuit seen in two encounters can never make two
animals look alike.
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageFilter
MAX_HAND_OBSTRUCTION = 0.15

class SnapshotError(Exception):
    """The snapshot cannot be matched: wrong mission, unreadable files. Exit code 2."""

@dataclass
class ViewImage:
    """One confirmed still of one view. `region` is the journal's normalised, upright body box."""
    frame_id: str
    view: str
    path: Path
    relative_path: str
    captured_at: datetime | None
    detail: bool
    region: dict | None = None
    person_mask: Path | None = None
    side_assumed: bool = False
    photo: Path | None = None

@dataclass
class Encounter:
    survey_id: str
    survey_name: str
    mission: str
    genus: str
    epithet: str
    common_name: str
    started_at: datetime | None
    location: dict | None
    total_length: dict | None
    images: list[ViewImage]
    warnings: list[str]
    details: dict | None = None

    @property
    def species(self) -> str:
        ...

    def views(self) -> list[str]:
        ...

def parse_date(value) -> datetime | None:
    """The app encodes dates as milliseconds since 1970; tolerate ISO strings too."""
    ...

def read_jsonl(path: Path) -> list[dict]:
    ...

def safe_child(root: Path, relative: str) -> Path:
    """Resolves a path the export names, refusing anything outside the snapshot."""
    ...

def pose_distance(a, b) -> float:
    ...

def crop_box(region: dict | None, width: int, height: int, margin: float=0.08) -> tuple[int, int, int, int] | None:
    """Pixel box for a normalised top-left-origin region, widened by `margin` of its size per side."""
    ...

def best_location(manifest: dict) -> dict | None:
    """The fix with the best stated horizontal accuracy. A negative accuracy means invalid."""
    ...

def total_length(snapshot: Path, manifest: dict) -> dict | None:
    """The encounter's total-length measurement, if the phone made one, with its own uncertainty."""
    ...

def encounter_details(snapshot: Path, warnings: list[str]) -> dict | None:
    """The operator's record of the animal (the app's SharkEncounterDetails), or None."""
    ...

def load_encounter(snapshot: Path, views: list[str], include_detail: bool=False) -> Encounter:
    ...
PERSON_FILL = (128, 128, 128)

def mask_people(picture: Image.Image, mask_path: Path | None) -> Image.Image:
    """The still with the handlers greyed out: flat grey gives the keypoint matchers nothing to
    find and the embedder nothing to match. The mask is widened by about 1% of the picture so a
    glove's edge does not survive. A mask that cannot be read changes nothing."""
    ...
