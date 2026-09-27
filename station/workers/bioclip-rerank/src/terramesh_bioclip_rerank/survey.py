"""Reads what the re-ranker needs from a survey snapshot: which observations to rank, their
photographs and the point that was tapped in each, and where and when each was made.

Everything here reads the app's own export formats (`manifest.json`, `frames.jsonl`,
`observations-earth.geojson`) and tolerates fields it does not know.
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass, field
from .kit import Job
PHONE_CROP_FRACTION = 0.55
MAXIMUM_FIX_GAP_SECONDS = 900
MAXIMUM_FIX_UNCERTAINTY_M = 2000

@dataclass
class EvidencePhoto:
    image_path: str
    pixel: tuple[float, float] | None
    frame_size: tuple[int, int] | None

@dataclass
class Place:
    latitude: float
    longitude: float
    source: str
    uncertainty_m: float | None

@dataclass
class ObservationToRank:
    id: str
    label: str
    created_at_ms: float | None
    original: dict | None
    place: Place | None = None
    skipped_photos: int = 0

def is_confidential(observation: dict) -> bool:
    """`Observation.isConfidential` in TerraMeshCore."""
    ...

def is_biological(observation: dict) -> bool:
    ...

def is_scene_context(observation: dict) -> bool:
    """`Observation.isSceneContext` in TerraMeshCore: a sampled region of the scene (grass, foliage,
    a fence), not a subject anyone pointed at."""
    ...

def is_manufactured_object(observation: dict) -> bool:
    """`Observation.isManufacturedObject` in TerraMeshCore: the phone ranked a man-made object first."""
    ...

def is_candidate_subject(observation: dict) -> bool:
    """`Observation.isCandidateSubject`. BioCLIP has no "no organism" answer: shown a patch of grass
    it still names the likeliest species, often an animal, with a high score. Only subjects are
    re-ranked."""
    ...

def original_identification(observation: dict) -> dict | None:
    """The name the phone saved: the observation's own, else its first photograph's."""
    ...

def earth_places(job: Job) -> dict[str, Place]:
    ...

def location_fixes(job: Job, manifest: dict) -> list[dict]:
    """Every usable fix from the manifest and the complete journal, sorted by time, de-duplicated."""
    ...

def nearest_fix(fixes: list[dict], at_ms: float | None) -> Place | None:
    ...

def observations_to_rank(job: Job, manifest: dict, *, include_non_biological: bool) -> tuple[list[ObservationToRank], dict]:
    ...

def crop_boxes(image_size: tuple[int, int], photo: EvidencePhoto, fractions: list[float]) -> list[tuple[int, int, int, int]]:
    """Square boxes centred on the tapped point, one per fraction of the shorter side, kept inside
    the image. The tapped point is scaled from the frame record's size to the JPEG's."""
    ...

def _finite(value) -> bool:
    ...

def _valid_coordinate(latitude, longitude) -> bool:
    ...
