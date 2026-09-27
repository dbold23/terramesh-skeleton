"""The reference catalogue of known individuals, one folder per group, that only people change.

    <catalogue folder>/<group>/          group: seaTurtle, whaleFluke or taggedPlant
      catalog.json        {"schema": 1, "group": "seaTurtle", "createdAt": ...}
      images.csv          image,individual,view,encounter,addedAt,reviewer,source
      tags.csv            individual,tag,addedAt,reviewer,source
      images/<individual>/<file>.jpg
      calibration.json    written by `terramesh-worker calibrate`, optional

Every row is a person's statement: this photo shows that individual, that individual carries this
tag. A Station job only reads the catalogue. The layout is shark-match's, with a tag table added,
so the scoring and calibration code is shared.
"""
from __future__ import annotations
import csv
import hashlib
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from terramesh_shark_match.catalog import COLUMNS, CatalogError, check_individual, file_sha256
from .groups import GROUPS
from .sightings import Sighting, crop
from .tags import normalise
__all__ = ['Catalog', 'CatalogError', 'load_catalog', 'init_catalog', 'import_table', 'add_sighting']

@dataclass(frozen=True)
class CatalogImage:
    path: Path
    image: str
    individual: str
    view: str
    encounter: str

@dataclass
class Catalog:
    root: Path
    group: str
    images: list[CatalogImage]
    tags: list[tuple[str, str]]

    @property
    def individuals(self) -> list[str]:
        ...

    def for_view(self, view: str) -> list[CatalogImage]:
        ...

    def tags_of(self, individual: str) -> list[str]:
        ...

    def digest(self) -> str:
        """Changes whenever a row or an image changes, so a calibration can be tied to it."""
        ...

def _now() -> str:
    ...

def _require_reviewer(reviewer: str) -> str:
    ...

def load_catalog(root: Path, group: str | None=None) -> Catalog:
    ...

def init_catalog(root: Path, group: str) -> Catalog:
    ...

def _append(path: Path, columns: list[str], rows: list[dict]) -> None:
    ...

def _tag_row(catalog: Catalog, individual: str, tag: str, reviewer: str, source: str) -> dict | None:
    """A tags.csv row, or None when the pair is already recorded. A tag already on another
    individual is refused: one physical tag cannot be on two animals or plants."""
    ...

def import_table(catalog: Catalog, table: Path, reviewer: str, source: str) -> tuple[int, int]:
    """Imports an existing photo-ID or tag register: a CSV with image,individual,view,encounter and
    an optional tag column. A row may have a tag and no image (a plant known only by its tag).
    `image` paths are relative to the CSV and are copied in. Returns (images, tags) added."""
    ...

def add_sighting(catalog: Catalog, sighting: Sighting, survey_id: str, individual: str, reviewer: str, crop_fraction: float) -> list[str]:
    """Copies a reviewed sighting's compared photos into the catalogue under `individual`, cropped
    exactly as the matcher saw them, and records its tag. The reviewer is the person who decided."""
    ...
