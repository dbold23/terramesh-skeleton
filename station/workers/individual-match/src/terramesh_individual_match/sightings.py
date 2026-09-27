"""Reads the individuals a person marked in a survey: records whose `individual` field says "this
is a sea turtle / a whale's fluke / a tagged plant I want re-found", with each photograph filed
under a view.

The phone writes `observation.individual` (TerraMeshCore `IndividualSighting`):

    {"group": "seaTurtle",
     "photos": [{"frameID": "<evidence frame id>", "view": "leftHead"}, ...],
     "tag": "AB1234", "tagSource": "typed" | "readFromPhoto", "tagFrameID": "<frame id>",
     "fieldName": "what the observer calls it, if anything"}

Each photo is cropped to a square around the point that was tapped when it was taken, so a
turtle's head or a fluke fills most of what is compared. Where and when a sighting was made is
never read: this worker writes no position at all, so its layer cannot place an animal.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from pathlib import Path
from PIL import Image
from .groups import GROUPS
from .kit import Job
from .tags import normalise

@dataclass
class SightingPhoto:
    frame_id: str
    view: str
    relative_path: str
    path: Path
    pixel: tuple[float, float] | None

@dataclass
class Sighting:
    observation_id: str
    group: str
    label: str
    photos: list[SightingPhoto]
    tag: str | None
    tag_source: str | None
    field_name: str | None

    def views(self) -> list[str]:
        ...

def is_confidential(observation: dict) -> bool:
    """`Observation.isConfidential`: never read, and not in an export anyway."""
    ...

def read_sightings(job: Job, manifest: dict) -> tuple[list[Sighting], list[str]]:
    ...

def tapped_pixel(evidence: dict, frame: dict | None) -> tuple[float, float] | None:
    ...

def crop(photo: SightingPhoto, fraction: float) -> Image.Image:
    """A square of `fraction` of the shorter side, centred on the tapped point and kept inside the
    picture, turned upright. A fraction of 1 or more keeps the whole picture.

    The tapped point is in stored pixels, so the box is chosen there and the crop turned after, as
    bioclip-rerank does: by its EXIF orientation when it has one, else a quarter clockwise for
    ARKit's landscape sensor frames (the app is portrait-only)."""
    ...

def _finite(value) -> bool:
    ...
