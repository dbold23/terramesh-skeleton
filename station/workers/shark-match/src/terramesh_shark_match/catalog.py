"""The reference catalogue a job compares an encounter against.

A catalogue is a folder on the Mac, one per species, that only people change:

    <catalog>/
      catalog.json        {"schema": 1, "species": "Notorynchus cepedianus", "mission": "oseaShark"}
      images.csv          image,individual,view,encounter,addedAt,reviewer,source
      images/<individual>/<file>.jpg
      calibration.json    written by `terramesh-worker calibrate`, optional

Every row is a person's statement that the image shows that individual. A Station job only reads
the catalogue. Adding an encounter (`catalog add`) or importing an existing photo-ID collection
(`catalog import`) is a separate command a person runs after reviewing.
"""
from __future__ import annotations
import csv
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageOps
from .snapshot import SPECIES, VIEWS, Encounter, crop_box, mask_people

class CatalogError(Exception):
    ...

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
    species: str
    mission: str
    images: list[CatalogImage]

    @property
    def individuals(self) -> list[str]:
        ...

    def for_view(self, view: str) -> list[CatalogImage]:
        ...

    def digest(self) -> str:
        """Changes whenever a row or an image changes, so a calibration can be tied to it."""
        ...

def file_sha256(path: Path) -> str:
    ...

def species_for(mission: str) -> str:
    ...

def check_individual(individual: str) -> str:
    ...

def load_catalog(root: Path, mission: str | None=None) -> Catalog:
    ...

def init_catalog(root: Path, mission: str) -> Catalog:
    ...

def _append_rows(catalog: Catalog, rows: list[dict]) -> None:
    ...

def _now() -> str:
    ...

def add_encounter(catalog: Catalog, encounter: Encounter, individual: str, reviewer: str) -> list[str]:
    """Copies a reviewed encounter's confirmed stills into the catalogue under `individual`.

    The reviewer is the person who confirmed the identity. Stills are cropped to the body box
    exactly as the matcher saw them, so later comparisons see the same evidence.
    """
    ...

def import_table(catalog: Catalog, table: Path, reviewer: str, source: str) -> int:
    """Imports an existing photo-ID collection from a CSV with image,individual,view,encounter.

    `image` paths are relative to the CSV. Images are copied in; the originals are left alone.
    """
    ...
